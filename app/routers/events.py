from fastapi import APIRouter, HTTPException
from app.schemas.event import EventCreate, EventResponse
import app.services.event as svc

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventResponse])
def list_events():
    return svc.list_events()


@router.post("", response_model=EventResponse, status_code=201)
def create_event(body: EventCreate):
    return svc.create_event(body.model_dump())


@router.get("/by-station/{station_id}", response_model=list[EventResponse])
def events_by_station(station_id: int):
    return svc.list_events_by_station(station_id)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int):
    data = svc.get_event(event_id)
    if not data:
        raise HTTPException(status_code=404, detail="Event not found")
    return data


from app.schemas.reservation import ReservationCreate, ReservationResponse
import app.services.reservation as res_svc

@router.post("/{event_id}/reservations", response_model=ReservationResponse, status_code=201)
def create_reservation(event_id: int, body: ReservationCreate):
    return res_svc.create_reservation(event_id, body.user_id)

