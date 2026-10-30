import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.device import Device
from backend.models.sensor_event import SensorEvent
from backend.schemas.sensor import SensorEventCreate, SensorEventRead
from backend.services.sensor_service import create_sensor_event

router = APIRouter(prefix="/sensor", tags=["sensor"])


@router.post("/data", response_model=SensorEventRead)
def add_sensor_data(event: SensorEventCreate, db: Session = Depends(get_db)):
    try:
        return create_sensor_event(db, event.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/history/{device_id}", response_model=list[SensorEventRead])
def get_sensor_history(device_id: int, limit: int = 20, db: Session = Depends(get_db)):
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 100")
    return db.query(SensorEvent).filter(
        SensorEvent.device_id == device_id
    ).order_by(SensorEvent.timestamp.desc()).limit(limit).all()


@router.get("/history")
def get_current_sensor_history(limit: int = 20, db: Session = Depends(get_db)):
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 100")
    device = db.query(Device).filter(Device.device_id == os.getenv("SMART_STICK_DEVICE_ID", "STICK_001")).first()
    if not device:
        return []
    return db.query(SensorEvent).filter(
        SensorEvent.device_id == device.id
    ).order_by(SensorEvent.timestamp.desc()).limit(limit).all()
