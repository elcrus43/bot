import os
import asyncio
from pathlib import Path
from groq import Groq
from groq import APIError, RateLimitError
from dotenv import load_dotenv
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

load_dotenv()
logger = logging.getLogger(__name__)

# Кэширование API ключа
@lru_cache()
def get_groq_client():
    """Lazy initialization of Groq client with caching."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY должен быть задан в .env файле!")
    return Groq(api_key=api_key)


# Абсолютный путь к knowledge.md рядом с этим файлом
KNOWLEDGE_PATH = Path(__file__).parent / "knowledge.md"


@lru_cache(maxsize=1)
def get_knowledge_base():
    """
    Кэшированное чтение knowledge.md файла.
    Кэш очищается при изменении файла.
    """
    try:
        with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            logger.info(f"Knowledge base loaded: {len(content)} chars")
            return content
    except FileNotFoundError:
        logger.warning(f"Knowledge file not found: {KNOWLEDGE_PATH}")
        return ""
    except Exception as e:
        logger.exception(f"Error reading knowledge file: {e}")
        return ""


def invalidate_knowledge_cache():
    """Очистка кэша базы знаний (для перезагрузки)."""
    get_knowledge_base.cache_clear()
    logger.info("Knowledge cache invalidated")


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((APIError, RateLimitError)),
    reraise=True
)
def _call_groq_sync(messages: list, **kwargs) -> str:
    """
    Синхронный вызов Groq API с retry логикой.
    
    Args:
        messages: Список сообщений для API
        **kwargs: Дополнительные параметры для API
    
    Returns:
        Ответ от AI
    """
    client = get_groq_client()
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1024),
            top_p=kwargs.get("top_p", 1),
            stream=False,
        )
        return response.choices[0].message.content
    
    except RateLimitError as e:
        logger.warning(f"Groq rate limit hit: {e}. Retrying...")
        raise
    except APIError as e:
        logger.error(f"Groq API error: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error calling Groq: {e}")
        raise


async def get_ai_response(user_input: str, history: list) -> str:
    """
    Генерация ответа с использованием Groq AI с retry и кэшированием.
    
    Args:
        user_input: Текст сообщения пользователя
        history: История сообщений (список dict с role и content)
    
    Returns:
        Ответ от AI или сообщение об ошибке
    """
    try:
        knowledge = get_knowledge_base()
        
        system_prompt = (
            "Вы — опытный и вежливый AI-ассистент агентства недвижимости в Кирове. "
            "Ваша цель — помогать клиентам с покупкой, продажей и арендой недвижимости. "
            "Используйте базу знаний ниже для ответов на вопросы. Если информации нет в базе знаний, "
            "отвечайте вежливо, опираясь на общие знания о недвижимости, но предлагайте связаться с риэлтором "
            "для уточнения деталей.\n\n"
            f"БАЗА ЗНАНИЙ:\n{knowledge}\n\n"
            "ПРАВИЛА:\n"
            "1. Будьте кратки и профессиональны (максимум 100 слов).\n"
            "2. Используйте дружелюбный тон.\n"
            "3. Если клиент спрашивает о ценах или услугах, берите данные из базы знаний.\n"
            "4. Всегда предлагайте связаться с риэлтором для деталей.\n"
            "5. Не придумывайте информацию — если не знаете, так и скажите."
        )
        
        messages = [{"role": "system", "content": system_prompt}]
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        if not history or history[-1]["content"] != user_input:
            messages.append({"role": "user", "content": user_input})
        
        logger.debug(f"Calling Groq API with {len(messages)} messages")
        
        # Асинхронный вызов с retry
        response = await asyncio.to_thread(
            _call_groq_sync,
            messages,
            temperature=0.7,
            max_tokens=1024
        )
        
        logger.info(f"Groq API response received: {len(response)} chars")
        return response
        
    except (APIError, RateLimitError) as e:
        logger.exception(f"Groq API failed after retries: {e}")
        return (
            "Извините, я временно не могу обработать ваш запрос из-за технической ошибки. "
            "Пожалуйста, попробуйте ещё раз через минуту или оставьте контакт — риэлтор свяжется с вами."
        )
    except Exception as e:
        logger.exception(f"Unexpected error in get_ai_response: {e}")
        return (
            "Извините, произошла непредвиденная ошибка. "
            "Пожалуйста, повторите попытку или оставьте контакт для связи с риэлтором."
        )


async def check_groq_health() -> bool:
    """
    Проверка доступности Groq API.
    
    Returns:
        True если API доступен, False иначе
    """
    try:
        client = get_groq_client()
        
        def _check():
            return client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
            )
        
        await asyncio.to_thread(_check)
        logger.info("Groq API health check: OK")
        return True
        
    except Exception as e:
        logger.error(f"Groq API health check failed: {e}")
        return False
