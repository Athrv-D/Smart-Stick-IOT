from typing import Optional

from pydantic import BaseModel


class EmergencyBase(BaseModel):
    device_id: int
    type: str
    severity: Optional[str] = "medium"
    description: Optional[str] = ""
    status: Optional[str] = "open"


class EmergencyCreate(EmergencyBase):
    pass


class EmergencyRead(EmergencyBase):
    id: int

    class Config:
        orm_mode = True
