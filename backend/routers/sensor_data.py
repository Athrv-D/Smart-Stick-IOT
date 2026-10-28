from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.sensor import SensorEventCreate, SensorEventRead
from backend.services.sensor_service import create_sensor_event

router = APIRouter(prefix="/sensor", tags=["sensor"])


@router.post("/data", response_model=SensorEventRead)
def add_sensor_data(event: SensorEventCreate, db: Session = Depends(get_db)):
    return create_sensor_event(db, event.dict())
