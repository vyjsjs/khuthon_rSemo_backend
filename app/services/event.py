from app.database import supabase


def create_event(data: dict) -> dict:
    res = supabase.table("events").insert(data).execute()
    return res.data[0]


def _attach_confirmed_count(events: list) -> list:
    for e in events:
        e["confirmed_count"] = len(
            supabase.table("event_attendances")
            .select("id")
            .eq("event_id", e["id"])
            .eq("status", "confirmed")
            .execute()
            .data
        )
    return events


def get_event(event_id: int) -> dict | None:
    try:
        res = supabase.table("events").select("*").eq("id", event_id).single().execute()
        event = res.data
        return _attach_confirmed_count([event])[0]
    except Exception:
        return None


def list_events() -> list:
    events = supabase.table("events").select("*").eq("status", "scheduled").execute().data
    return _attach_confirmed_count(events)


def list_events_by_station(station_id: int) -> list:
    match_ids = [
        m["id"]
        for m in supabase.table("matches").select("id").eq("station_id", station_id).execute().data
    ]
    if not match_ids:
        return []
    events = supabase.table("events").select("*").in_("match_id", match_ids).execute().data
    return _attach_confirmed_count(events)
