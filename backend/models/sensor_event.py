from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.database import Base


class SensorEvent(Base):
    __tablename__ = "sensor_events"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    distance_cm = Column(Float, default=0.0)
    water_detected = Column(Boolean, default=False, nullable=False)
    water_value = Column(Integer, nullable=True)
    status = Column(String, default="clear")
    event_type = Column(String, default="obstacle_scan")
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    device = relationship("Device")
