import math
import random
from datetime import datetime, timezone
from typing import Optional
from .base import BaseSensor, SensorReadingDTO, SourceEnum, QualityEnum

class VirtualSensor(BaseSensor):
    """
    Sensor virtual configurable capaz de simular ciclos temporales,
    ruido estadístico y fallos deliberados.
    """
    def __init__(
        self,
        sensor_id: str,
        zone_id: str,
        device_id: str,
        variable: str,
        unit: str,
        base_value: float,
        amplitude: float = 1.5,
        noise_std: float = 0.2,
        period_seconds: float = 300.0,
        min_limit: float = 0.0,
        max_limit: float = 100.0,
        batch_id: Optional[str] = None
    ):
        super().__init__(
            sensor_id=sensor_id,
            zone_id=zone_id,
            device_id=device_id,
            variable=variable,
            unit=unit,
            source=SourceEnum.SIMULATION
        )
        self.base_value = base_value
        self.amplitude = amplitude
        self.noise_std = noise_std
        self.period_seconds = period_seconds
        self.min_limit = min_limit
        self.max_limit = max_limit
        self.batch_id = batch_id
        self._last_value = base_value

    async def read(self) -> SensorReadingDTO:
        now = datetime.now(timezone.utc)

        # 1. Simulación de fallo: desconectado
        if not self.is_connected or self.fault_mode == "disconnected":
            return SensorReadingDTO(
                sensor_id=self.sensor_id,
                zone_id=self.zone_id,
                device_id=self.device_id,
                variable=self.variable,
                value=0.0,
                unit=self.unit,
                timestamp=now,
                source=self.source,
                quality=QualityEnum.INVALID,
                batch_id=self.batch_id
            )

        # 2. Simulación de fallo: valor congelado (stuck/frozen)
        if self.fault_mode == "frozen":
            return SensorReadingDTO(
                sensor_id=self.sensor_id,
                zone_id=self.zone_id,
                device_id=self.device_id,
                variable=self.variable,
                value=self._last_value,
                unit=self.unit,
                timestamp=now,
                source=self.source,
                quality=QualityEnum.DEGRADED,
                batch_id=self.batch_id
            )

        # 3. Simulación de fallo: fuera de rango crítico
        if self.fault_mode == "out_of_range":
            return SensorReadingDTO(
                sensor_id=self.sensor_id,
                zone_id=self.zone_id,
                device_id=self.device_id,
                variable=self.variable,
                value=self.max_limit * 1.5,
                unit=self.unit,
                timestamp=now,
                source=self.source,
                quality=QualityEnum.DEGRADED,
                batch_id=self.batch_id
            )

        # 4. Operación nominal con oscilación sinusoidal y ruido gaussiano
        seconds_now = now.timestamp()
        phase = (seconds_now % self.period_seconds) / self.period_seconds * 2.0 * math.pi
        oscillation = math.sin(phase) * self.amplitude
        noise = random.gauss(0, self.noise_std)
        computed_value = self.base_value + oscillation + noise

        # Clamping
        clamped_value = max(self.min_limit, min(self.max_limit, computed_value))
        clamped_value = round(clamped_value, 2)
        self._last_value = clamped_value

        return SensorReadingDTO(
            sensor_id=self.sensor_id,
            zone_id=self.zone_id,
            device_id=self.device_id,
            variable=self.variable,
            value=clamped_value,
            unit=self.unit,
            timestamp=now,
            source=self.source,
            quality=QualityEnum.VALID,
            batch_id=self.batch_id
        )

class VirtualTemperatureSensor(VirtualSensor):
    def __init__(self, sensor_id: str, zone_id: str, device_id: str, base_temp: float = 27.0, batch_id: Optional[str] = None):
        super().__init__(
            sensor_id=sensor_id,
            zone_id=zone_id,
            device_id=device_id,
            variable="ambient_temperature" if "LAR" not in zone_id else "substrate_temperature",
            unit="C",
            base_value=base_temp,
            amplitude=2.0,
            noise_std=0.15,
            min_limit=10.0,
            max_limit=55.0,
            batch_id=batch_id
        )

class VirtualHumiditySensor(VirtualSensor):
    def __init__(self, sensor_id: str, zone_id: str, device_id: str, base_hum: float = 65.0, batch_id: Optional[str] = None):
        super().__init__(
            sensor_id=sensor_id,
            zone_id=zone_id,
            device_id=device_id,
            variable="relative_humidity",
            unit="%",
            base_value=base_hum,
            amplitude=5.0,
            noise_std=0.5,
            min_limit=10.0,
            max_limit=100.0,
            batch_id=batch_id
        )

class VirtualLightSensor(VirtualSensor):
    def __init__(self, sensor_id: str, zone_id: str, device_id: str):
        super().__init__(
            sensor_id=sensor_id,
            zone_id=zone_id,
            device_id=device_id,
            variable="light_intensity",
            unit="lux",
            base_value=8000.0,
            amplitude=7000.0,
            noise_std=50.0,
            period_seconds=600.0,
            min_limit=0.0,
            max_limit=25000.0
        )

class VirtualWeightSensor(VirtualSensor):
    def __init__(self, sensor_id: str, zone_id: str, device_id: str, base_weight: float = 15.0, batch_id: Optional[str] = None):
        super().__init__(
            sensor_id=sensor_id,
            zone_id=zone_id,
            device_id=device_id,
            variable="weight",
            unit="kg",
            base_value=base_weight,
            amplitude=0.3,
            noise_std=0.05,
            period_seconds=1200.0,
            min_limit=0.0,
            max_limit=100.0,
            batch_id=batch_id
        )
