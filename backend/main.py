from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.models import Device, DeviceSettings, Emergency, SensorEvent
from backend.routers.devices import router as devices_router
from backend.routers.emergencies import router as emergencies_router
from backend.routers.sensor_data import router as sensor_router
from backend.routers.settings import router as settings_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Stick IoT API")

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
    return {"message": "Smart Stick IoT API is running"}
