import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.device import Device
from backend.models.emergency import Emergency
from backend.schemas.emergency import EmergencyCreate, EmergencyDeliveryUpdate, EmergencyRead
from backend.services.notification_service import send_alert

router = APIRouter(prefix="/emergencies", tags=["emergencies"])
CONFIGURED_DEVICE_ID = os.getenv("SMART_STICK_DEVICE_ID", "STICK_001")


@router.get("/", response_model=list[EmergencyRead])
def get_emergencies(db: Session = Depends(get_db)):
    return db.query(Emergency).order_by(Emergency.created_at.desc()).all()


@router.post("/", response_model=EmergencyRead)
def create_emergency(emergency: EmergencyCreate, db: Session = Depends(get_db)):
    if emergency.device_code:
        if emergency.device_code != CONFIGURED_DEVICE_ID:
            raise HTTPException(status_code=403, detail="Unknown Smart Stick")
        device = db.query(Device).filter(Device.device_id == emergency.device_code).first()
    elif emergency.device_id:
        device = db.query(Device).filter(Device.id == emergency.device_id).first()
    else:
        raise HTTPException(status_code=422, detail="device_code is required")
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    obj = Emergency(
        device_id=device.id,
        emergency_type=emergency.emergency_type,
        severity=emergency.severity,
        description=emergency.description,
        notification_status="device_pending",
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    # Actual SMS is sent by SIM800L firmware. This backend only records the event.
    return obj


@router.post("/{emergency_id}/delivery", response_model=EmergencyRead)
def update_delivery_status(
    emergency_id: int, payload: EmergencyDeliveryUpdate, db: Session = Depends(get_db)
):
    emergency = db.query(Emergency).filter(Emergency.id == emergency_id).first()
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")
    emergency.notification_status = payload.status
    db.commit()
    db.refresh(emergency)
    return emergency


@router.patch("/{emergency_id}", response_model=EmergencyRead)
def resolve_emergency(emergency_id: int, db: Session = Depends(get_db)):
    emergency = db.query(Emergency).filter(Emergency.id == emergency_id).first()
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")
    emergency.resolved = True
    db.commit()
    db.refresh(emergency)
    return emergency
