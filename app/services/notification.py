from app.database import supabase


def create_notification(user_id: int, message: str) -> dict:
    data = {"user_id": user_id, "message": message}
    res = supabase.table("notifications").insert(data).execute()
    return res.data[0]


def get_user_notifications(user_id: int) -> list:
    res = supabase.table("notifications").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return res.data
