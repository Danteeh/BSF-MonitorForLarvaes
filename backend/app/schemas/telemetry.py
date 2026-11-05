from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SensorReadingCreate(BaseModel):
    sensor_id: str
    zone_id: str
    device_id: Optional[str] = None
    batch_id: Optional[str] = None
    variable: str
    value: float
    unit: str
    source: str = "simulation"
    quality: str = "valid"
    recorded_at: datetime = Field(default_factory=datetime.utcnow)

class SensorReadingResponse(BaseModel):
    id: int
    sensor_id: str
    zone_id: str
    device_id: Optional[str]
    batch_id: Optional[str]
    variable: str
    value: float
    unit: str
    source: str
    quality: str
    recorded_at: datetime
    received_at: datetime

    class Config:
        from_attributes = True

class SensorResponse(BaseModel):
    id: str
    device_id: Optional[str]
    zone_id: str
    variable: str
    unit: str
    min_expected: Optional[float]
    max_expected: Optional[float]
    status: str
    latest_reading: Optional[SensorReadingResponse] = None

    class Config:
        from_attributes = True

class DeviceResponse(BaseModel):
    id: str
    zone_id: Optional[str]
    name: str
    device_type: str
    connection_type: str
    status: str
    last_seen: Optional[datetime]

    class Config:
        from_attributes = True

class ZoneResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str
    sensors: List[SensorResponse] = []

    class Config:
        from_attributes = True

class SystemStatusResponse(BaseModel):
    mode: str
    status: str
    backend_version: str
    active_zones: int
    active_sensors: int
    mqtt_connected: bool
    database_connected: bool
    timestamp: datetime

class AlertResponse(BaseModel):
    id: int
    zone_id: str
    sensor_id: Optional[str]
    severity: str
    title: str
    message: str
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True

class SimulatorControlRequest(BaseModel):
    action: str = Field(description="pause, resume, set_speed")
    tick_rate_seconds: Optional[int] = None

class FaultInjectionRequest(BaseModel):
    sensor_id: str
    fault_type: str = Field(description="disconnected, frozen, out_of_range, clear")
