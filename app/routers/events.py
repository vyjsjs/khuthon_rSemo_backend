from fastapi import APIRouter
from app.schemas.event import EventCreate, EventResponse
import app.services.event as svc

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventResponse])
def list_events():
    return svc.list_events()


@router.post("", response_model=EventResponse, status_code=201)
def create_event(body: EventCreate):
    return svc.create_event(body.model_dump())


@router.get("/station/{station_id}", response_model=list[EventResponse])
def events_by_station(station_id: int):
    return svc.list_events_by_station(station_id)
