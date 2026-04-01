import os
import asyncio
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Абсолютный путь к knowledge.md рядом с этим файлом
KNOWLEDGE_PATH = Path(__file__).parent / "knowledge.md"

def get_knowledge_base():
    """Reads the knowledge.md file and returns its content."""
    try:
        with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

async def get_ai_response(user_input: str, history: list):
    """
    Generates a response using Groq AI based on history and knowledge base.
    """
    knowledge = get_knowledge_base()
    system_prompt = (
        "Вы — опытный и вежливый AI-ассистент агентства недвижимости в Кирове. "
        "Ваша цель — помогать клиентам с вопросами о покупке, продаже и аренде недвижимости. "
        "Используйте базу знаний ниже для ответов на вопросы. Если информации нет в базе знаний, "
        "отвечайте вежливо, опираясь на общие знания о недвижимости, но предлагайте связаться с риэлтором "
        "для уточнения деталей.\n\n"
        f"БАЗА ЗНАНИЙ:\n{knowledge}\n\n"
        "ПРАВИЛА:\n"
        "1. Будьте кратки и профессиональны.\n"
        "2. Используйте дружелюбный тон.\n"
        "3. Если клиент спрашивает о ценах или услугах, берите данные из базы знаний.\n"
    )
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    if not history or history[-1]["content"] != user_input:
        messages.append({"role": "user", "content": user_input})

    # Groq SDK синхронный — запускаем в отдельном потоке, чтобы не блокировать event loop
    def _call_groq():
        return client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )

    completion = await asyncio.to_thread(_call_groq)
    return completion.choices[0].message.content
