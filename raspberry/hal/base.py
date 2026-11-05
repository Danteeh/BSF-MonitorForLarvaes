from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class SourceEnum(str, Enum):
    SIMULATION = "simulation"
    HARDWARE = "hardware"
    UPLOAD = "upload"

class QualityEnum(str, Enum):
    VALID = "valid"
    DEGRADED = "degraded"
    INVALID = "invalid"

class SensorReadingDTO(BaseModel):
    sensor_id: str
    zone_id: str
    device_id: str
    variable: str
    value: float
    unit: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: SourceEnum = SourceEnum.SIMULATION
    quality: QualityEnum = QualityEnum.VALID
    batch_id: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BaseSensor(ABC):
    """Contrato abstracto para cualquier sensor (físico o virtual)"""
    def __init__(
        self,
        sensor_id: str,
        zone_id: str,
        device_id: str,
        variable: str,
        unit: str,
        source: SourceEnum = SourceEnum.SIMULATION
    ):
        self.sensor_id = sensor_id
        self.zone_id = zone_id
        self.device_id = device_id
        self.variable = variable
        self.unit = unit
        self.source = source
        self.is_connected = True
        self.fault_mode: Optional[str] = None

    @abstractmethod
    async def read(self) -> SensorReadingDTO:
        """Lee el valor actual y retorna un DTO estandarizado"""
        pass

    def inject_fault(self, fault_type: Optional[str]):
        """Permite inyectar fallos para pruebas del sistema (disconnected, frozen, out_of_range)"""
        self.fault_mode = fault_type
        if fault_type == "disconnected":
            self.is_connected = False
        else:
            self.is_connected = True
