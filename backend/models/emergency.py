from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.database import Base


class Emergency(Base):
    __tablename__ = "emergencies"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    type = Column(String, nullable=False)
    severity = Column(String, default="medium")
    description = Column(String, default="")
    status = Column(String, default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    device = relationship("Device")
