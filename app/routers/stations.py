from typing import Optional
from fastapi import APIRouter, HTTPException
from app.schemas.station import StationCreate, StationResponse
import app.services.station as svc

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("", response_model=list[StationResponse])
def list_stations(genre: Optional[str] = None):
    return svc.list_stations(genre)


@router.post("", response_model=StationResponse, status_code=201)
def create_station(body: StationCreate):
    return svc.create_station(body.model_dump())


@router.get("/{station_id}", response_model=StationResponse)
def get_station(station_id: int):
    data = svc.get_station(station_id)
    if not data:
        raise HTTPException(status_code=404, detail="Station not found")
    return data


@router.get("/{station_id}/checkin-count")
def get_checkin_count(station_id: int, genre: Optional[str] = None):
    return svc.get_checkin_count(station_id, genre)


@router.get("/{station_id}/demand")
def get_demand(station_id: int):
    return svc.get_demand_summary(station_id)
