from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EmergencyCreate(BaseModel):
    device_id: int = Field(gt=0)
    emergency_type: str = Field(min_length=1, max_length=100)
    severity: Literal["low", "medium", "high"] = "medium"
    description: str = Field(default="", max_length=1000)


class EmergencyRead(EmergencyCreate):
    id: int
    notification_status: str
    resolved: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
