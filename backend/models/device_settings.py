from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class DeviceSettings(Base):
    __tablename__ = "device_settings"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False, unique=True)
    threshold_temperature = Column(Float, default=35.0)
    threshold_vibration = Column(Float, default=12.0)
    threshold_pressure = Column(Float, default=25.0)
    alert_mode = Column(String, default="sms")

    device = relationship("Device")
