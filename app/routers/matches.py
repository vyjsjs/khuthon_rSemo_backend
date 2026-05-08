from fastapi import APIRouter
from app.schemas.match import MatchResponse, MatchRespondRequest
import app.services.match as svc

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/pending", response_model=list[MatchResponse])
def get_pending_matches():
    return svc.get_pending_matches()


@router.get("/artist/{artist_id}", response_model=list[MatchResponse])
def get_artist_matches(artist_id: int):
    return svc.get_matches_for_artist(artist_id)


@router.patch("/{match_id}/respond", response_model=MatchResponse)
def respond_to_match(match_id: int, body: MatchRespondRequest):
    return svc.respond_to_match(match_id, body.status, body.scheduled_at)
