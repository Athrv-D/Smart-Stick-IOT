from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SensorEventCreate(BaseModel):
    device_id: int = Field(gt=0)
    distance_cm: float = Field(default=0.0, ge=0)
    status: Literal["clear", "obstacle_detected", "water_detected"] = "clear"
    event_type: str = Field(default="obstacle_scan", min_length=1, max_length=50)
    battery_level: float | None = Field(default=None, ge=0, le=100)


class SensorEventRead(BaseModel):
    id: int
    device_id: int
    distance_cm: float
    status: str
    event_type: str
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
