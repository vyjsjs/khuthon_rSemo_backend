from collections import Counter
from app.database import supabase


def create_station(data: dict) -> dict:
    res = supabase.table("stations").insert(data).execute()
    return res.data[0]


def list_stations() -> list:
    return supabase.table("stations").select("*").eq("is_active", True).execute().data


def get_station(station_id: int) -> dict | None:
    try:
        res = supabase.table("stations").select("*").eq("id", station_id).single().execute()
        return res.data
    except Exception:
        return None


def get_demand_summary(station_id: int) -> list:
    rows = supabase.table("checkins").select("genre").eq("station_id", station_id).execute().data
    counts = Counter(r["genre"] for r in rows)
    return [{"genre": g, "count": c} for g, c in counts.most_common()]
