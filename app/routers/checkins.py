from typing import Optional
from fastapi import APIRouter
from app.schemas.checkin import CheckinCreate, CheckinResponse
import app.services.checkin as svc

router = APIRouter(prefix="/checkins", tags=["checkins"])


@router.get("/user/{user_id}", response_model=list[CheckinResponse])
def get_user_checkins(user_id: int, station_id: Optional[int] = None):
    return svc.get_user_checkins(user_id, station_id)


@router.post("", response_model=CheckinResponse, status_code=201)
def create_checkin(body: CheckinCreate):
    return svc.create_checkin(body.model_dump())
