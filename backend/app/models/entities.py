from sqlalchemy import Column, String, Integer, BigInteger, Double, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.session import Base

def utc_now():
    return datetime.now(timezone.utc)

class Zone(Base):
    __tablename__ = "zones"

    id = Column(String(32), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), default=utc_now)

    devices = relationship("Device", back_populates="zone", cascade="all, delete-orphan")
    sensors = relationship("Sensor", back_populates="zone", cascade="all, delete-orphan")
    batches = relationship("Batch", back_populates="zone")
    readings = relationship("SensorReading", back_populates="zone")
    alerts = relationship("Alert", back_populates="zone")

class Device(Base):
    __tablename__ = "devices"

    id = Column(String(32), primary_key=True)
    zone_id = Column(String(32), ForeignKey("zones.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(100), nullable=False)
    device_type = Column(String(50), nullable=False)
    connection_type = Column(String(50), nullable=False)
    status = Column(String(32), nullable=False, default="ONLINE")
    last_seen = Column(DateTime(timezone=True), default=utc_now)

    zone = relationship("Zone", back_populates="devices")
    sensors = relationship("Sensor", back_populates="device", cascade="all, delete-orphan")

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(String(32), primary_key=True)
    device_id = Column(String(32), ForeignKey("devices.id", ondelete="CASCADE"), nullable=True)
    zone_id = Column(String(32), ForeignKey("zones.id", ondelete="CASCADE"), nullable=False)
    variable = Column(String(64), nullable=False)
    unit = Column(String(16), nullable=False)
    min_expected = Column(Float, nullable=True)
    max_expected = Column(Float, nullable=True)
    status = Column(String(32), nullable=False, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), default=utc_now)

    device = relationship("Device", back_populates="sensors")
    zone = relationship("Zone", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor", cascade="all, delete-orphan")

class Batch(Base):
    __tablename__ = "batches"

    id = Column(String(64), primary_key=True)
    zone_id = Column(String(32), ForeignKey("zones.id", ondelete="RESTRICT"), nullable=False)
    stage = Column(String(32), nullable=False, default="LARVAE")
    start_date = Column(DateTime(timezone=True), default=utc_now)
    end_date = Column(DateTime(timezone=True), nullable=True)
    initial_quantity = Column(Float, default=0.0)
    substrate_type = Column(String(100), nullable=True)
    final_yield = Column(Float, nullable=True)
    status = Column(String(32), nullable=False, default="ACTIVE")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    zone = relationship("Zone", back_populates="batches")
    feedings = relationship("FeedingRecord", back_populates="batch", cascade="all, delete-orphan")
    media = relationship("MediaFile", back_populates="batch")

class FeedingRecord(Base):
    __tablename__ = "feeding_records"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    batch_id = Column(String(64), ForeignKey("batches.id", ondelete="CASCADE"), nullable=False)
    food_mass_g = Column(Float, nullable=False)
    food_type = Column(String(100), nullable=False)
    notes = Column(Text, nullable=True)
    fed_at = Column(DateTime(timezone=True), default=utc_now)

    batch = relationship("Batch", back_populates="feedings")

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sensor_id = Column(String(32), ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False)
    zone_id = Column(String(32), ForeignKey("zones.id", ondelete="CASCADE"), nullable=False)
    device_id = Column(String(32), ForeignKey("devices.id", ondelete="SET NULL"), nullable=True)
    batch_id = Column(String(64), ForeignKey("batches.id", ondelete="SET NULL"), nullable=True)
    variable = Column(String(64), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(16), nullable=False)
    source = Column(String(20), nullable=False, default="simulation")
    quality = Column(String(20), nullable=False, default="valid")
    recorded_at = Column(DateTime(timezone=True), nullable=False)
    received_at = Column(DateTime(timezone=True), default=utc_now)

    sensor = relationship("Sensor", back_populates="readings")
    zone = relationship("Zone", back_populates="readings")

class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(512), nullable=False)
    media_type = Column(String(20), nullable=False, default="IMAGE")
    zone_id = Column(String(32), ForeignKey("zones.id", ondelete="SET NULL"), nullable=True)
    batch_id = Column(String(64), ForeignKey("batches.id", ondelete="SET NULL"), nullable=True)
    file_size_bytes = Column(BigInteger, default=0)
    resolution = Column(String(32), nullable=True)
    source = Column(String(20), nullable=False, default="simulation")
    captured_at = Column(DateTime(timezone=True), default=utc_now)

    batch = relationship("Batch", back_populates="media")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    zone_id = Column(String(32), ForeignKey("zones.id", ondelete="CASCADE"), nullable=False)
    sensor_id = Column(String(32), ForeignKey("sensors.id", ondelete="SET NULL"), nullable=True)
    severity = Column(String(20), nullable=False, default="WARNING")
    title = Column(String(128), nullable=False)
    message = Column(Text, nullable=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    zone = relationship("Zone", back_populates="alerts")
