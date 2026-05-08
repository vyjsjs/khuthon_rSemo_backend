from fastapi import APIRouter
from app.schemas.checkin import CheckinCreate, CheckinResponse
import app.services.checkin as svc

router = APIRouter(prefix="/checkins", tags=["checkins"])


@router.post("", response_model=CheckinResponse, status_code=201)
def create_checkin(body: CheckinCreate):
    return svc.create_checkin(body.model_dump())
