from sqlalchemy.orm import Session

from backend.models.sensor_event import SensorEvent


def create_sensor_event(db: Session, event_data: dict):
    event = SensorEvent(**event_data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
