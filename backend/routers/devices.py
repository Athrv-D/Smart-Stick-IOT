from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.device import Device
from backend.schemas.device import DeviceCreate, DeviceRead
from backend.services.device_service import create_device, get_all_devices

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=list[DeviceRead])
def list_devices(db: Session = Depends(get_db)):
    return get_all_devices(db)


@router.get("/{device_id}", response_model=DeviceRead)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("/", response_model=DeviceRead)
def add_device(device: DeviceCreate, db: Session = Depends(get_db)):
    try:
        return create_device(db, device.dict())
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
