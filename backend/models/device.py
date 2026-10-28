from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from backend.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="online")
    connection_type = Column(String, default="wifi")
    battery_level = Column(Float, default=100.0)
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    location = Column(String, default="Unknown")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
