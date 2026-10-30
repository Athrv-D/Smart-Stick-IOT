from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EmergencyCreate(BaseModel):
    # Hardware uses device_code; numeric device_id is retained for old clients.
    device_code: str | None = Field(default=None, min_length=1, max_length=100)
    device_id: int | None = Field(default=None, gt=0)
    emergency_type: str = Field(min_length=1, max_length=100)
    severity: str = Field(default="medium", pattern="^(low|medium|high)$")
    description: str = Field(default="", max_length=1000)


class EmergencyDeliveryUpdate(BaseModel):
    status: str = Field(pattern="^(sent|failed)$")


class EmergencyRead(BaseModel):
    id: int
    device_id: int
    emergency_type: str
    severity: str
    description: str
    notification_status: str
    resolved: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
