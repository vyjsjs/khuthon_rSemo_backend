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
