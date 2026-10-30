import os

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.device import Device
from backend.models.device_settings import DeviceSettings

router = APIRouter(prefix="/settings", tags=["settings"])
CONFIGURED_DEVICE_ID = os.getenv("SMART_STICK_DEVICE_ID", "STICK_001")


class SettingsUpdate(BaseModel):
    obstacle_threshold: float = Field(default=80, gt=0, le=500)
    buzzer_enabled: bool = True
    vibration_enabled: bool = True
    emergency_contact_number: str = Field(default="", max_length=20)
    notification_preferences: str = Field(default="sms", pattern="^(sms|app|both)$")


def _get_device(db: Session):
    device = (
        db.query(Device)
        .filter(Device.device_id == CONFIGURED_DEVICE_ID, Device.is_active.is_(True))
        .first()
    )
    if not device:
        raise HTTPException(status_code=404, detail="Smart Stick is not registered")
    return device


@router.get("/")
def get_settings(db: Session = Depends(get_db)):
    device = _get_device(db)
    settings = db.query(DeviceSettings).filter(DeviceSettings.device_id == device.id).first()
    if not settings:
        settings = DeviceSettings(device_id=device.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.put("/")
def update_settings(payload: SettingsUpdate, db: Session = Depends(get_db)):
    device = _get_device(db)
    settings = db.query(DeviceSettings).filter(DeviceSettings.device_id == device.id).first()
    if not settings:
        settings = DeviceSettings(device_id=device.id)
        db.add(settings)

    for key, value in payload.model_dump().items():
        setattr(settings, key, value)

    db.commit()
    db.refresh(settings)
    return settings
