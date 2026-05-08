from collections import Counter
from app.database import supabase


def create_station(data: dict) -> dict:
    res = supabase.table("stations").insert(data).execute()
    return res.data[0]


def list_stations(genre: str | None = None) -> list:
    stations = supabase.table("stations").select("*").eq("is_active", True).execute().data
    if genre:
        stations = [s for s in stations if genre in (s.get("supported_genres") or "")]
    for s in stations:
        query = supabase.table("checkins").select("id").eq("station_id", s["id"])
        if genre:
            query = query.eq("genre", genre)
        s["current_count"] = len(query.execute().data)
    return stations


def get_station(station_id: int) -> dict | None:
    try:
        res = supabase.table("stations").select("*").eq("id", station_id).single().execute()
        return res.data
    except Exception:
        return None


def get_checkin_count(station_id: int, genre: str | None = None) -> dict:
    query = supabase.table("checkins").select("id").eq("station_id", station_id)
    if genre:
        query = query.eq("genre", genre)
    count = len(query.execute().data)
    return {"station_id": station_id, "genre": genre, "count": count}


def get_demand_summary(station_id: int) -> list:
    rows = supabase.table("checkins").select("genre").eq("station_id", station_id).execute().data
    counts = Counter(r["genre"] for r in rows)
    return [{"genre": g, "count": c} for g, c in counts.most_common()]


def get_recommended_stations(artist_id: int) -> list:
    from app.services.artist import get_artist
    artist = get_artist(artist_id)
    if not artist:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Artist not found")

    main_genre = artist.get("genres", "").split(",")[0].strip()
    if not main_genre:
        return []

    stations = supabase.table("stations").select("*").eq("is_active", True).execute().data
    checkins_res = supabase.table("checkins").select("station_id").eq("genre", main_genre).execute().data
    
    counts = Counter(c["station_id"] for c in checkins_res)
    
    recommended = []
    for s in stations:
        s["current_count"] = counts.get(s["id"], 0)
        recommended.append(s)
        
    recommended.sort(key=lambda x: x["current_count"], reverse=True)
    return recommended
