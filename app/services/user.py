from app.database import supabase


def create_user(role: str) -> dict:
    res = supabase.table("users").insert({"role": role}).execute()
    return res.data[0]


def get_user(user_id: int) -> dict | None:
    try:
        res = supabase.table("users").select("*").eq("id", user_id).single().execute()
        return res.data
    except Exception:
        return None
