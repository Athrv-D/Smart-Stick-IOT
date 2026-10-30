from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensorEventCreate(BaseModel):
    # Hardware sends the stable device code. device_id remains for older simulator clients.
    device_code: str | None = Field(default=None, min_length=1, max_length=100)
    device_id: int | None = Field(default=None, gt=0)
    distance_cm: float = Field(default=0.0, ge=0, le=1000)
    water_detected: bool = False
    water_value: int | None = Field(default=None, ge=0, le=4095)
    status: str = Field(default="clear", min_length=1, max_length=50)
    event_type: str = Field(default="sensor_scan", min_length=1, max_length=50)
    battery_level: float | None = Field(default=None, ge=0, le=100)


class SensorEventRead(BaseModel):
    id: int
    device_id: int
    distance_cm: float
    water_detected: bool
    water_value: int | None
    status: str
    event_type: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
