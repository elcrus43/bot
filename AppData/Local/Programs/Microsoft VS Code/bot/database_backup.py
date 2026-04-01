import os
import asyncio
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise EnvironmentError("SUPABASE_URL и SUPABASE_KEY должны быть заданы в .env файле!")

supabase: Client = create_client(url, key)

async def save_lead(telegram_id: int, username: str, full_name: str, phone: str = None, interest: str = None, notes: str = None):
    """
    Saves or updates a lead in the Supabase 'leads' table.
    """
    data = {
        "telegram_id": telegram_id,
        "username": username,
        "full_name": full_name,
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
        update_response = await asyncio.to_thread(_update)
        return update_response.data[0] if update_response.data else None
    else:
        insert_response = await asyncio.to_thread(_insert)
        return insert_response.data[0] if insert_response.data else None

async def get_lead_by_telegram_id(telegram_id: int):
    """
    Retrieves a lead by their Telegram ID.
    """
    def _select():
        return supabase.table("leads").select("*").eq("telegram_id", telegram_id).execute()

    response = await asyncio.to_thread(_select)
    return response.data[0] if response.data else None

async def save_message(lead_id: str, role: str, content: str):
    """
    Saves a chat message in the Supabase 'messages' table.
    """
    data = {
        "lead_id": lead_id,
        "role": role,
        "content": content
    }

    def _insert():
        return supabase.table("messages").insert(data).execute()

    response = await asyncio.to_thread(_insert)
    return response.data[0] if response.data else None

async def get_messages_for_lead(lead_id: str, limit: int = 10):
    """
    Retrieves recent chat messages for a specific lead.
    """
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
    return response.data
