from fastapi import APIRouter, Depends, HTTPException
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

    send_alert(
        emergency_type=obj.emergency_type,
        message=f"Emergency alert triggered for device {obj.device_id}",
    )
    return obj


@router.patch("/{emergency_id}")
def resolve_emergency(emergency_id: int, db: Session = Depends(get_db)):
    emergency = db.query(Emergency).filter(Emergency.id == emergency_id).first()
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")

    emergency.resolved = True
    emergency.notification_status = "sent"
    db.commit()
    return emergency
