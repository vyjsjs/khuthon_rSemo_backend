from pydantic import BaseModel
from typing import Optional


class StationCreate(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None
    capacity: Optional[int] = 50
    supported_genres: Optional[str] = None
    hourly_cost: Optional[float] = 0.0


class StationResponse(BaseModel):
    id: int
    latitude: float
    longitude: float
    address: Optional[str] = None
    capacity: Optional[int] = None
    supported_genres: Optional[str] = None
    hourly_cost: Optional[float] = None
    is_active: bool
