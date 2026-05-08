from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class UserCreate(BaseModel):
    role: Literal["resident", "artist"]


class UserResponse(BaseModel):
    id: int
    role: str
    created_at: datetime
