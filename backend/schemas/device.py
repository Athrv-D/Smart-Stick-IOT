from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceBase(BaseModel):
    device_id: str
    name: str
    status: Optional[str] = "online"
    connection_type: Optional[str] = "wifi"
    battery_level: Optional[float] = 100.0
    location: Optional[str] = "Unknown"
    is_active: Optional[bool] = True


class DeviceCreate(DeviceBase):
    pass


class DeviceRead(DeviceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
