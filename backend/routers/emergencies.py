from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.emergency import Emergency
from backend.schemas.emergency import EmergencyCreate, EmergencyRead
from backend.services.notification_service import send_alert

router = APIRouter(prefix="/emergencies", tags=["emergencies"])


@router.get("/", response_model=list[EmergencyRead])
def get_emergencies(db: Session = Depends(get_db)):
    return db.query(Emergency).all()


@router.post("/", response_model=EmergencyRead)
def create_emergency(emergency: EmergencyCreate, db: Session = Depends(get_db)):
    obj = Emergency(**emergency.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    send_alert(f"Emergency alert: {obj.type} for device {obj.device_id}")
    return obj
