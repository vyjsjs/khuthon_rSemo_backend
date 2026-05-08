from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal


class MatchResponse(BaseModel):
    id: int
    station_id: int
    artist_id: int
    genre: str
    demand_count: int
    status: str
    responded_at: Optional[datetime] = None
    created_at: datetime


class MatchRespondRequest(BaseModel):
    status: Literal["accepted", "rejected"]
    scheduled_at: Optional[datetime] = None  # 수락 시 공연 예정 시간
