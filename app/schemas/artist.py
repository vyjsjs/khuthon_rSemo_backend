from pydantic import BaseModel
from typing import Optional


class ArtistCreate(BaseModel):
    user_id: int
    display_name: str
    genres: Optional[str] = None
    activity_radius_km: Optional[float] = 5.0
    base_latitude: Optional[float] = None
    base_longitude: Optional[float] = None


class ArtistResponse(BaseModel):
    user_id: int
    display_name: str
    genres: Optional[str] = None
    activity_radius_km: Optional[float] = None
    base_latitude: Optional[float] = None
    base_longitude: Optional[float] = None
    is_available: bool


class AvailabilityUpdate(BaseModel):
    is_available: bool
