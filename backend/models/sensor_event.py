from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.database import Base


class SensorEvent(Base):
    __tablename__ = "sensor_events"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    temperature = Column(Float, default=0.0)
    vibration = Column(Float, default=0.0)
    pressure = Column(Float, default=0.0)
    moisture = Column(Float, default=0.0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    device = relationship("Device")
