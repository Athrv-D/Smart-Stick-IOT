from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DeviceCreate(BaseModel):
    device_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=100)
    status: Literal["online", "offline"] = "online"
    connection_type: Literal["wifi", "cellular"] = "wifi"
    battery_level: float = Field(default=100.0, ge=0, le=100)
    location: str = Field(default="Unknown", max_length=200)
    is_active: bool = True


class DeviceHeartbeat(BaseModel):
    device_code: str = Field(min_length=1, max_length=100)
    battery_level: float | None = Field(default=None, ge=0, le=100)
    connection_type: Literal["wifi", "cellular"] = "wifi"
    firmware_version: str | None = Field(default=None, max_length=40)


class DeviceRead(DeviceCreate):
    id: int
    last_seen: datetime | None = None
    created_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
