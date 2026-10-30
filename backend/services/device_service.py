from sqlalchemy.orm import Session

from backend.models.device import Device


def get_all_devices(db: Session):
    return (
        db.query(Device)
        .filter(Device.is_active.is_(True))
        .order_by(Device.id.asc())
        .limit(1)
        .all()
    )


def create_device(db: Session, device_data: dict):
    db_device = Device(**device_data)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device
