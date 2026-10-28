from sqlalchemy.orm import Session

from backend.models.device import Device


def get_all_devices(db: Session):
    return db.query(Device).all()


def create_device(db: Session, device_data: dict):
    db_device = Device(**device_data)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device
