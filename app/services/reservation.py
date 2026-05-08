from app.database import supabase


def create_reservation(event_id: int, user_id: int) -> dict:
    data = {"event_id": event_id, "user_id": user_id}
    res = supabase.table("reservations").insert(data).execute()
    return res.data[0]


def get_user_reservations(user_id: int) -> list:
    res = supabase.table("reservations").select("*, events(*)").eq("user_id", user_id).execute()
    return res.data
