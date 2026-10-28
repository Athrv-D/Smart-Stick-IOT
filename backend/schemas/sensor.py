from typing import Optional

from pydantic import BaseModel, ConfigDict


class SensorEventBase(BaseModel):
    device_id: int
    distance_cm: Optional[float] = 0.0
    status: Optional[str] = "clear"
    event_type: Optional[str] = "obstacle_scan"


class SensorEventCreate(SensorEventBase):
    pass


class SensorEventRead(SensorEventBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
