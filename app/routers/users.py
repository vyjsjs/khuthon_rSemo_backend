from typing import Optional
from fastapi import APIRouter, Body, HTTPException
from app.schemas.user import UserCreate, UserResponse
import app.services.user as svc

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=201)
def create_user(body: Optional[UserCreate] = Body(default=None)):
    role = body.role if body else "resident"
    return svc.create_user(role)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    data = svc.get_user(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    return data


from app.schemas.reservation import ReservationResponse
import app.services.reservation as res_svc

@router.get("/{user_id}/reservations", response_model=list[ReservationResponse])
def get_user_reservations(user_id: int):
    return res_svc.get_user_reservations(user_id)


from app.schemas.notification import NotificationResponse
import app.services.notification as notif_svc

@router.get("/{user_id}/notifications", response_model=list[NotificationResponse])
def get_user_notifications(user_id: int):
    return notif_svc.get_user_notifications(user_id)


