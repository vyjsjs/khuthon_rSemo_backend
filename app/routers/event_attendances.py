from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal
import app.services.event_attendance as svc

router = APIRouter(prefix="/event-attendances", tags=["event-attendances"])


class AttendanceRespondRequest(BaseModel):
    status: Literal["confirmed", "declined"]


@router.get("/user/{user_id}")
def get_user_attendances(user_id: int):
    return svc.get_user_attendances(user_id)


@router.patch("/{attendance_id}/respond")
def respond(attendance_id: int, body: AttendanceRespondRequest):
    return svc.respond(attendance_id, body.status)
