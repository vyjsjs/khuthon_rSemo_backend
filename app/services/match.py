from datetime import datetime, timezone
from typing import Optional
from app.database import supabase


def get_matches_for_artist(artist_id: int) -> list:
    return supabase.table("matches").select("*").eq("artist_id", artist_id).execute().data


def get_pending_matches() -> list:
    return supabase.table("matches").select("*").eq("status", "pending").execute().data


def respond_to_match(match_id: int, status: str, scheduled_at: Optional[datetime] = None) -> dict:
    res = supabase.table("matches").update({
        "status": status,
        "responded_at": datetime.now(timezone.utc).isoformat(),
    }).eq("id", match_id).execute()
    match = res.data[0]

    if status == "accepted" and scheduled_at:
        supabase.table("events").insert({
            "match_id": match_id,
            "scheduled_at": scheduled_at.isoformat(),
            "status": "scheduled",
        }).execute()

    return match
