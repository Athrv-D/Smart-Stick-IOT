from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class DeviceSettings(Base):
    __tablename__ = "device_settings"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False, unique=True)
    obstacle_threshold = Column(Float, default=80.0)
    buzzer_enabled = Column(Boolean, default=True)
    vibration_enabled = Column(Boolean, default=True)
    emergency_contact_number = Column(String, default="+1234567890")
    notification_preferences = Column(String, default="sms")

    device = relationship("Device")
