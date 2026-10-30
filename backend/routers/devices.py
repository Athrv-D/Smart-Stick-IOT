import os
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.device import Device
from backend.schemas.device import DeviceCreate, DeviceHeartbeat, DeviceRead
from backend.services.device_service import create_device, get_all_devices

router = APIRouter(prefix="/devices", tags=["smart-stick"])
CONFIGURED_DEVICE_ID = os.getenv("SMART_STICK_DEVICE_ID", "STICK_001")


@router.get("/current", response_model=DeviceRead)
def get_current_device(db: Session = Depends(get_db)):
    device = db.query(Device).filter(
        Device.device_id == CONFIGURED_DEVICE_ID, Device.is_active.is_(True)
    ).first()
    if not device:
        raise HTTPException(status_code=404, detail="Smart Stick is not registered")
    return device


@router.get("/", response_model=list[DeviceRead])
def list_devices(db: Session = Depends(get_db)):
    return get_all_devices(db)


@router.post("/heartbeat")
def heartbeat(payload: DeviceHeartbeat, db: Session = Depends(get_db)):
    if payload.device_code != CONFIGURED_DEVICE_ID:
        raise HTTPException(status_code=403, detail="Unknown Smart Stick")
    device = db.query(Device).filter(
        Device.device_id == payload.device_code, Device.is_active.is_(True)
    ).first()
    if not device:
        raise HTTPException(status_code=404, detail="Register the Smart Stick before sending heartbeat")
    device.last_seen = datetime.now(timezone.utc)
    device.status = "online"
    device.connection_type = payload.connection_type
    if payload.battery_level is not None:
        device.battery_level = payload.battery_level
    db.commit()
    return {"ok": True, "device_code": device.device_id, "last_seen": device.last_seen}


@router.get("/{device_id}", response_model=DeviceRead)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("/", response_model=DeviceRead)
def add_device(device: DeviceCreate, db: Session = Depends(get_db)):
    if device.device_id != CONFIGURED_DEVICE_ID:
        raise HTTPException(status_code=400, detail=f"This installation accepts only {CONFIGURED_DEVICE_ID}")
    existing = db.query(Device).filter(Device.device_id == CONFIGURED_DEVICE_ID).first()
    if existing:
        for key, value in device.model_dump().items():
            setattr(existing, key, value)
        existing.last_seen = datetime.now(timezone.utc)
        db.commit()
        db.refresh(existing)
        return existing
    try:
        return create_device(db, device.model_dump())
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not register Smart Stick") from exc
