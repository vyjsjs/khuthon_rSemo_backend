from app.database import supabase


def create_event(data: dict) -> dict:
    res = supabase.table("events").insert(data).execute()
    return res.data[0]


def _attach_detail(events: list) -> list:
    for e in events:
        # 예매 확정 인원
        e["confirmed_count"] = len(
            supabase.table("event_attendances")
            .select("id")
            .eq("event_id", e["id"])
            .eq("status", "confirmed")
            .execute()
            .data
        )
        # match → station, artist, genre 정보 병합
        try:
            match = (
                supabase.table("matches")
                .select("station_id, artist_id, genre")
                .eq("id", e["match_id"])
                .single()
                .execute()
                .data
            )
            e["station_id"] = match["station_id"]
            e["artist_id"] = match["artist_id"]
            e["genre"] = match["genre"]

            station = (
                supabase.table("stations")
                .select("address, latitude, longitude")
                .eq("id", match["station_id"])
                .single()
                .execute()
                .data
            )
            e["station_address"] = station["address"]
            e["station_latitude"] = station["latitude"]
            e["station_longitude"] = station["longitude"]

            artist = (
                supabase.table("artists")
                .select("display_name")
                .eq("user_id", match["artist_id"])
                .single()
                .execute()
                .data
            )
            e["artist_name"] = artist["display_name"]
        except Exception:
            e.setdefault("station_id", None)
            e.setdefault("station_address", None)
            e.setdefault("station_latitude", None)
            e.setdefault("station_longitude", None)
            e.setdefault("artist_id", None)
            e.setdefault("artist_name", None)
            e.setdefault("genre", None)

    return events


def get_event(event_id: int) -> dict | None:
    try:
        event = supabase.table("events").select("*").eq("id", event_id).single().execute().data
        return _attach_detail([event])[0]
    except Exception:
        return None


def list_events() -> list:
    events = supabase.table("events").select("*").eq("status", "scheduled").execute().data
    return _attach_detail(events)


def list_events_by_station(station_id: int) -> list:
    match_ids = [
        m["id"]
        for m in supabase.table("matches").select("id").eq("station_id", station_id).execute().data
    ]
    if not match_ids:
        return []
    events = supabase.table("events").select("*").in_("match_id", match_ids).execute().data
    return _attach_detail(events)
