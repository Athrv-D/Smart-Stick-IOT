from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.device_settings import DeviceSettings

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/{device_id}")
def get_settings(device_id: int, db: Session = Depends(get_db)):
    settings = db.query(DeviceSettings).filter(DeviceSettings.device_id == device_id).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return settings


@router.post("/{device_id}")
def update_settings(device_id: int, payload: dict, db: Session = Depends(get_db)):
    settings = db.query(DeviceSettings).filter(DeviceSettings.device_id == device_id).first()
    if not settings:
        settings = DeviceSettings(device_id=device_id)
        db.add(settings)

    for key, value in payload.items():
        if hasattr(settings, key):
            setattr(settings, key, value)

    db.commit()
    return settings
