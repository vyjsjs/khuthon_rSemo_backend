from app.database import supabase
from app.config import MATCH_THRESHOLD
from app.utils.distance import haversine_km


def get_user_checkins(user_id: int, station_id: int | None = None) -> list:
    query = supabase.table("checkins").select("*").eq("user_id", user_id)
    if station_id:
        query = query.eq("station_id", station_id)
    return query.execute().data


def create_checkin(data: dict) -> dict:
    res = supabase.table("checkins").insert(data).execute()
    checkin = res.data[0]
    _try_create_match(data["station_id"], data["genre"])
    return checkin


def _try_create_match(station_id: int, genre: str) -> None:
    checkins = supabase.table("checkins").select("id").eq("station_id", station_id).eq("genre", genre).execute()
    if len(checkins.data) < MATCH_THRESHOLD:
        return

    existing = (
        supabase.table("matches")
        .select("id")
        .eq("station_id", station_id)
        .eq("genre", genre)
        .eq("status", "pending")
        .execute()
    )
    if existing.data:
        return

    try:
        station = supabase.table("stations").select("latitude,longitude").eq("id", station_id).single().execute()
        s_lat, s_lon = station.data["latitude"], station.data["longitude"]
    except Exception:
        return

    artists = supabase.table("artists").select("*").eq("is_available", True).execute().data

    best_artist = None
    best_dist = float("inf")
    for a in artists:
        if genre not in (a.get("genres") or ""):
            continue
        if a.get("base_latitude") and a.get("base_longitude"):
            dist = haversine_km(s_lat, s_lon, a["base_latitude"], a["base_longitude"])
            radius = a.get("activity_radius_km") or float("inf")
            if dist <= radius and dist < best_dist:
                best_artist = a
                best_dist = dist
        elif best_artist is None:
            best_artist = a

    if not best_artist:
        return

    supabase.table("matches").insert({
        "station_id": station_id,
        "artist_id": best_artist["user_id"],
        "genre": genre,
        "demand_count": len(checkins.data),
        "status": "pending",
    }).execute()
