from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.device import Device
from backend.models.emergency import Emergency
from backend.schemas.emergency import EmergencyCreate, EmergencyRead
from backend.services.notification_service import send_alert

router = APIRouter(prefix="/emergencies", tags=["emergencies"])


@router.get("/", response_model=list[EmergencyRead])
def get_emergencies(db: Session = Depends(get_db)):
    return db.query(Emergency).order_by(Emergency.created_at.desc()).all()


@router.post("/", response_model=EmergencyRead)
def create_emergency(emergency: EmergencyCreate, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == emergency.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    obj = Emergency(**emergency.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)

    try:
        result = send_alert(
            emergency_type=obj.emergency_type,
            message=f"Emergency alert triggered for {device.device_id}",
        )
        obj.notification_status = result.get("status", "unknown")
    except Exception:
        obj.notification_status = "failed"

    db.commit()
    db.refresh(obj)
    return obj


@router.patch("/{emergency_id}", response_model=EmergencyRead)
def resolve_emergency(emergency_id: int, db: Session = Depends(get_db)):
    emergency = db.query(Emergency).filter(Emergency.id == emergency_id).first()
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")

    emergency.resolved = True
    db.commit()
    db.refresh(emergency)
    return emergency
