from app.database import supabase


def get_user_attendances(user_id: int) -> list:
    return (
        supabase.table("event_attendances")
        .select("*")
        .eq("user_id", user_id)
        .eq("status", "pending")
        .execute()
        .data
    )


def respond(attendance_id: int, status: str) -> dict:
    res = supabase.table("event_attendances").update({"status": status}).eq("id", attendance_id).execute()
    return res.data[0]
