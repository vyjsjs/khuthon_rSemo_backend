from app.database import supabase


def create_event(data: dict) -> dict:
    res = supabase.table("events").insert(data).execute()
    return res.data[0]


def list_events() -> list:
    return supabase.table("events").select("*").eq("status", "scheduled").execute().data


def list_events_by_station(station_id: int) -> list:
    match_ids = [
        m["id"]
        for m in supabase.table("matches").select("id").eq("station_id", station_id).execute().data
    ]
    if not match_ids:
        return []
    return supabase.table("events").select("*").in_("match_id", match_ids).execute().data
