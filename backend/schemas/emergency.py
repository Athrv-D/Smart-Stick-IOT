from typing import Optional

from pydantic import BaseModel, ConfigDict


class EmergencyBase(BaseModel):
    device_id: int
    emergency_type: str
    severity: Optional[str] = "medium"
    description: Optional[str] = ""
    notification_status: Optional[str] = "pending"
    resolved: Optional[bool] = False


class EmergencyCreate(EmergencyBase):
    pass


class EmergencyRead(EmergencyBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
