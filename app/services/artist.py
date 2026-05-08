from typing import Optional
from app.database import supabase


def create_artist(data: dict) -> dict:
    res = supabase.table("artists").insert(data).execute()
    return res.data[0]


def get_artist(user_id: int) -> dict | None:
    try:
        res = supabase.table("artists").select("*").eq("user_id", user_id).single().execute()
        return res.data
    except Exception:
        return None


def list_artists(genre: Optional[str] = None) -> list:
    query = supabase.table("artists").select("*").eq("is_available", True)
    if genre:
        query = query.ilike("genres", f"%{genre}%")
    return query.execute().data


def set_availability(user_id: int, is_available: bool) -> dict:
    res = supabase.table("artists").update({"is_available": is_available}).eq("user_id", user_id).execute()
    return res.data[0]
