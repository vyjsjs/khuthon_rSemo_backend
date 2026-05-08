from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventCreate(BaseModel):
    match_id: int
    scheduled_at: datetime


class EventResponse(BaseModel):
    id: int
    match_id: int
    scheduled_at: datetime
    status: str
    created_at: datetime
    confirmed_count: Optional[int] = None
    # 정류장 정보
    station_id: Optional[int] = None
    station_address: Optional[str] = None
    station_latitude: Optional[float] = None
    station_longitude: Optional[float] = None
    # 아티스트 정보
    artist_id: Optional[int] = None
    artist_name: Optional[str] = None
    # 공연 정보
    genre: Optional[str] = None
