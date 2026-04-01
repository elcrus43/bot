import os
import asyncio
from functools import lru_cache
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging

load_dotenv()
logger = logging.getLogger(__name__)


@lru_cache()
def get_supabase_client() -> Client:
    """
    Lazy initialization of Supabase client with caching.
    Creates client only when needed.
    Uses Service Role Key for full access.
    """
    url = os.getenv("SUPABASE_URL")
    # Используем Service Role Key для полного доступа
    key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise EnvironmentError("SUPABASE_URL и SUPABASE_KEY/SUPABASE_SERVICE_KEY должны быть заданы в .env файле!")

    logger.info(f"Supabase client initialized: {url}")
    return create_client(url, key)


async def save_lead(
    telegram_id: int,
    username: str,
    full_name: str,
    phone: str = None,
    interest: str = None,
    notes: str = None
) -> dict | None:
    """
    Saves or updates a lead in the Supabase 'leads' table.
    
    Returns:
        dict с данными лида или None если ошибка
    """
    try:
        supabase = get_supabase_client()
        
        data = {
            "telegram_id": telegram_id,
            "username": username,
            "full_name": full_name,
            "updated_at": datetime.utcnow().isoformat()
        }
        if phone:
            data["phone"] = phone
        if interest:
            data["interest"] = interest
        if notes:
            data["notes"] = notes

        def _select():
            return supabase.table("leads").select("*").eq("telegram_id", telegram_id).execute()

        def _update():
            return supabase.table("leads").update(data).eq("telegram_id", telegram_id).execute()

        def _insert():
            return supabase.table("leads").insert(data).execute()

        response = await asyncio.to_thread(_select)
        
        if response.data:
            logger.debug(f"Updating existing lead: {telegram_id}")
            update_response = await asyncio.to_thread(_update)
            return update_response.data[0] if update_response.data else None
        else:
            logger.info(f"Creating new lead: {telegram_id}")
            insert_response = await asyncio.to_thread(_insert)
            return insert_response.data[0] if insert_response.data else None
            
    except Exception as e:
        logger.exception(f"Error in save_lead: {e}")
        return None


async def get_lead_by_telegram_id(telegram_id: int) -> dict | None:
    """
    Retrieves a lead by their Telegram ID.
    
    Returns:
        dict с данными лида или None
    """
    try:
        supabase = get_supabase_client()
        
        def _select():
            return supabase.table("leads").select("*").eq("telegram_id", telegram_id).execute()

        response = await asyncio.to_thread(_select)
        return response.data[0] if response.data else None
        
    except Exception as e:
        logger.exception(f"Error in get_lead_by_telegram_id: {e}")
        return None


async def save_message(lead_id: str, role: str, content: str) -> dict | None:
    """
    Saves a chat message in the Supabase 'messages' table.
    
    Returns:
        dict с данными сообщения или None
    """
    try:
        supabase = get_supabase_client()
        
        data = {
            "lead_id": lead_id,
            "role": role,
            "content": content,
            "created_at": datetime.utcnow().isoformat()
        }

        def _insert():
            return supabase.table("messages").insert(data).execute()

        response = await asyncio.to_thread(_insert)
        return response.data[0] if response.data else None
        
    except Exception as e:
        logger.exception(f"Error in save_message: {e}")
        return None


async def get_messages_for_lead(lead_id: str, limit: int = 20) -> list:
    """
    Retrieves recent chat messages for a specific lead.
    
    Args:
        lead_id: ID лида
        limit: Максимальное количество сообщений (по умолчанию 20)
    
    Returns:
        Список сообщений
    """
    try:
        supabase = get_supabase_client()
        
        def _select():
            return (
                supabase.table("messages")
                .select("*")
                .eq("lead_id", lead_id)
                .order("created_at", desc=False)
                .limit(limit)
                .execute()
            )

        response = await asyncio.to_thread(_select)
        return response.data or []
        
    except Exception as e:
        logger.exception(f"Error in get_messages_for_lead: {e}")
        return []


async def count_leads() -> int:
    """
    Подсчитывает общее количество лидов.
    
    Returns:
        Количество лидов
    """
    try:
        supabase = get_supabase_client()
        
        def _count():
            return supabase.table("leads").select("*", count="exact").execute()

        response = await asyncio.to_thread(_count)
        return response.count if hasattr(response, 'count') else len(response.data)
        
    except Exception as e:
        logger.exception(f"Error in count_leads: {e}")
        return 0


async def get_stats() -> dict:
    """
    Получает статистику бота за 24 часа.
    
    Returns:
        dict со статистикой
    """
    try:
        supabase = get_supabase_client()
        
        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)
        
        def _get_leads_count():
            return (
                supabase.table("leads")
                .select("*", count="exact")
                .gte("created_at", yesterday.isoformat())
                .execute()
            )
        
        def _get_messages_count():
            return (
                supabase.table("messages")
                .select("*", count="exact")
                .gte("created_at", yesterday.isoformat())
                .execute()
            )
        
        def _get_interest_stats():
            return (
                supabase.table("leads")
                .select("interest")
                .not_.is_("interest", "null")
                .execute()
            )
        
        # Лиды за 24 часа
        leads_response = await asyncio.to_thread(_get_leads_count)
        leads_24h = leads_response.count if hasattr(leads_response, 'count') else 0
        
        # Сообщения за 24 часа
        messages_response = await asyncio.to_thread(_get_messages_count)
        messages_24h = messages_response.count if hasattr(messages_response, 'count') else 0
        
        # Статистика по интересам
        interest_response = await asyncio.to_thread(_get_interest_stats)
        interest_stats = {"interest_buy": 0, "interest_sell": 0, "interest_rent": 0}
        
        if interest_response.data:
            for lead in interest_response.data:
                interest = lead.get("interest", "")
                if interest == "купить":
                    interest_stats["interest_buy"] += 1
                elif interest == "продать":
                    interest_stats["interest_sell"] += 1
                elif interest == "аренда":
                    interest_stats["interest_rent"] += 1
        
        # Среднее время ответа (примерно)
        avg_response_time = 3.2  # Заглушка, можно вычислять по timestamp сообщений
        
        return {
            "leads_24h": leads_24h,
            "messages_24h": messages_24h,
            "avg_response_time": avg_response_time,
            **interest_stats
        }
        
    except Exception as e:
        logger.exception(f"Error in get_stats: {e}")
        return {
            "leads_24h": 0,
            "messages_24h": 0,
            "avg_response_time": 0,
            "interest_buy": 0,
            "interest_sell": 0,
            "interest_rent": 0
        }
