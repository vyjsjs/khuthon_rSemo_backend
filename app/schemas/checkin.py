from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CheckinCreate(BaseModel):
    user_id: int
    station_id: int
    genre: str
    preferred_timeslot: Optional[str] = None


class CheckinResponse(BaseModel):
    id: int
    user_id: int
    station_id: int
    genre: str
    preferred_timeslot: Optional[str] = None
    created_at: datetime
