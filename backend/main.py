from datetime import timezone

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import Base, engine, get_db
from backend.models import Device, DeviceSettings, Emergency, SensorEvent
from backend.routers.devices import router as devices_router
from backend.routers.emergencies import router as emergencies_router
from backend.routers.sensor_data import router as sensor_router
from backend.routers.settings import router as settings_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Stick Caregiver API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(devices_router)
app.include_router(sensor_router)
app.include_router(emergencies_router)
app.include_router(settings_router)


@app.get("/")
def root():
    return {"message": "Smart Stick API is running", "status": "ok"}


@app.get("/dashboard")
def dashboard_summary(db: Session = Depends(get_db)):
    """Return the status and recent activity for the one configured stick."""
    device_id = __import__("os").getenv("SMART_STICK_DEVICE_ID", "STICK_001")
    device = (
        db.query(Device)
        .filter(Device.device_id == device_id, Device.is_active.is_(True))
        .first()
    )

    if not device:
        return {
            "configured_device_id": device_id,
            "device": None,
            "latest_sensor": None,
            "sensor_events": [],
            "emergencies": [],
            "message": "Register the Smart Stick to begin monitoring.",
        }

    last_seen = device.last_seen
    is_online = False
    if last_seen:
        comparable_last_seen = (
            last_seen.replace(tzinfo=timezone.utc)
            if last_seen.tzinfo is None
            else last_seen
        )
        from datetime import datetime, timedelta
        is_online = datetime.now(timezone.utc) - comparable_last_seen <= timedelta(minutes=2)

    latest_sensor = (
        db.query(SensorEvent)
        .filter(SensorEvent.device_id == device.id)
        .order_by(SensorEvent.timestamp.desc())
        .first()
    )
    sensor_events = (
        db.query(SensorEvent)
        .filter(SensorEvent.device_id == device.id)
        .order_by(SensorEvent.timestamp.desc())
        .limit(8)
        .all()
    )
    emergencies = (
        db.query(Emergency)
        .filter(Emergency.device_id == device.id)
        .order_by(Emergency.created_at.desc())
        .limit(5)
        .all()
    )
    settings = (
        db.query(DeviceSettings)
        .filter(DeviceSettings.device_id == device.id)
        .first()
    )

    return {
        "configured_device_id": device_id,
        "device": {
            "id": device.id,
            "device_id": device.device_id,
            "name": device.name,
            "status": "online" if is_online else "offline",
            "connection_type": device.connection_type,
            "battery_level": device.battery_level,
            "location": device.location,
            "last_seen": last_seen,
        },
        "latest_sensor": latest_sensor,
        "sensor_events": sensor_events,
        "emergencies": emergencies,
        "settings": settings,
    }
