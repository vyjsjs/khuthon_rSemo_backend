from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.schemas.event import EventResponse

class ReservationCreate(BaseModel):
    user_id: int


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    created_at: datetime
    events: Optional[EventResponse] = None

