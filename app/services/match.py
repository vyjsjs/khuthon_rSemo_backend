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
        event = supabase.table("events").insert({
            "match_id": match_id,
            "scheduled_at": scheduled_at.isoformat(),
            "status": "scheduled",
        }).execute().data[0]

        # 해당 정류장+장르에 체크인했던 유저들에게 관람 의사 확인 레코드 생성
        checkins = (
            supabase.table("checkins")
            .select("user_id")
            .eq("station_id", match["station_id"])
            .eq("genre", match["genre"])
            .execute()
            .data
        )
        unique_user_ids = list({c["user_id"] for c in checkins})
        if unique_user_ids:
            supabase.table("event_attendances").insert([
                {"event_id": event["id"], "user_id": uid, "status": "pending"}
                for uid in unique_user_ids
            ]).execute()

            supabase.table("notifications").insert([
                {"user_id": uid, "message": f"공연이 확정되었어요! '{match['genre']}' 공연 일정을 확인해보세요."}
                for uid in unique_user_ids
            ]).execute()

    return match
