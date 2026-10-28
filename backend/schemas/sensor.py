from typing import Optional

from pydantic import BaseModel


class SensorEventBase(BaseModel):
    device_id: int
    temperature: Optional[float] = 0.0
    vibration: Optional[float] = 0.0
    pressure: Optional[float] = 0.0
    moisture: Optional[float] = 0.0


class SensorEventCreate(SensorEventBase):
    pass


class SensorEventRead(SensorEventBase):
    id: int

    class Config:
        orm_mode = True
