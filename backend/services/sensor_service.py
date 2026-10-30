from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.models.device import Device
from backend.models.sensor_event import SensorEvent


def create_sensor_event(db: Session, event_data: dict):
    device_code = event_data.pop("device_code", None)
    legacy_device_id = event_data.pop("device_id", None)
    query = db.query(Device)
    if device_code:
        device = query.filter(Device.device_id == device_code, Device.is_active.is_(True)).first()
    elif legacy_device_id:
        device = query.filter(Device.id == legacy_device_id).first()
    else:
        raise ValueError("device_code is required")

    if not device:
        raise ValueError("Device not found")

    battery_level = event_data.pop("battery_level", None)
    if battery_level is not None:
        device.battery_level = battery_level

    event = SensorEvent(device_id=device.id, **event_data)
    device.last_seen = datetime.now(timezone.utc)
    device.status = "online"

    db.add(event)
    db.commit()
    db.refresh(event)
    return event
