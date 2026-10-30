from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.models.device import Device
from backend.models.sensor_event import SensorEvent


def create_sensor_event(db: Session, event_data: dict):
    device = db.query(Device).filter(Device.id == event_data["device_id"]).first()
    if not device:
        raise ValueError("Device not found")

    battery_level = event_data.pop("battery_level", None)
    if battery_level is not None:
        device.battery_level = battery_level

    event = SensorEvent(**event_data)
    device.last_seen = datetime.now(timezone.utc)
    device.status = "online"

    db.add(event)
    db.commit()
    db.refresh(event)
    return event
