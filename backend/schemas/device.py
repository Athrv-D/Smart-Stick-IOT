from typing import Optional

from pydantic import BaseModel


class DeviceBase(BaseModel):
    name: str
    device_id: str
    status: Optional[str] = "online"
    battery_level: Optional[float] = 100.0
    location: Optional[str] = "Unknown"
    is_active: Optional[bool] = True


class DeviceCreate(DeviceBase):
    pass


class DeviceRead(DeviceBase):
    id: int

    class Config:
        orm_mode = True
