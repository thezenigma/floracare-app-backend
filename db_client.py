from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user_plants(user_id: str, plant_ids: list = None):
    query = supabase.table("plants").select("*").eq("user_id", user_id)
    if plant_ids:
        query = query.in_("id", plant_ids)
    return query.execute().data

def get_recent_journals(user_id: str, plant_ids: list = None, limit: int = 5):
    query = supabase.table("journal_entries").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit)
    if plant_ids:
        query = query.in_("plant_id", plant_ids)
    return query.execute().data

def save_care_memory(user_id: str, plant_id: str, memory_type: str, content: str, session_id: str):
    data = {
        "user_id": user_id,
        "plant_id": plant_id,
        "memory_type": memory_type,
        "content": content,
        "source_session_id": session_id
    }
    return supabase.table("care_memories").insert(data).execute()

def ensure_chat_session(session_id: str, user_id: str, initial_message: str):
    # Check if session exists
    res = supabase.table("chat_sessions").select("id").eq("id", session_id).execute()
    if not res.data:
        # Create session with the first message as the title (truncated)
        title = initial_message[:40] + "..." if len(initial_message) > 40 else initial_message
        supabase.table("chat_sessions").insert({
            "id": session_id,
            "user_id": user_id,
            "title": title
        }).execute()

def save_message(session_id: str, role: str, content: str):
    supabase.table("messages").insert({
        "session_id": session_id,
        "role": role,
        "content": content
    }).execute()
