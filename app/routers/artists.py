from typing import Optional
from fastapi import APIRouter, HTTPException
from app.schemas.artist import ArtistCreate, ArtistResponse, AvailabilityUpdate
import app.services.artist as svc

router = APIRouter(prefix="/artists", tags=["artists"])


@router.post("", response_model=ArtistResponse, status_code=201)
def create_artist(body: ArtistCreate):
    return svc.create_artist(body.model_dump())


@router.get("", response_model=list[ArtistResponse])
def list_artists(genre: Optional[str] = None):
    return svc.list_artists(genre)


@router.get("/{user_id}", response_model=ArtistResponse)
def get_artist(user_id: int):
    data = svc.get_artist(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Artist not found")
    return data


@router.patch("/{user_id}/availability", response_model=ArtistResponse)
def update_availability(user_id: int, body: AvailabilityUpdate):
    return svc.set_availability(user_id, body.is_available)
