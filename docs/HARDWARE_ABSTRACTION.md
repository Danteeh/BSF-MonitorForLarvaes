# Capa de Abstracción de Hardware (HAL) — BSF MONITOR

La capa HAL (**Hardware Abstraction Layer**) se ubica en `raspberry/hal` y desacopla la lógica de negocio y telemetría de las particularidades electrónicas o de bus de comunicación de los sensores y cámaras.

## 1. Contratos Base (Interfaces Abstractas)

Todas las implementaciones heredan de `BaseSensor`:

```python
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime

class BaseSensor(ABC):
    def __init__(self, sensor_id: str, zone_id: str, device_id: str, variable: str, unit: str):
        self.sensor_id = sensor_id
        self.zone_id = zone_id
        self.device_id = device_id
        self.variable = variable
        self.unit = unit

    @abstractmethod
    async def read(self) -> Dict[str, Any]:
        """Retorna una lectura normalizada con keys: sensor_id, zone_id, device_id, variable, value, unit, timestamp, source, quality"""
        pass
```

## 2. Clases Virtuales vs. Clases Físicas

| Tipo | Interfaz | Implementación Virtual (Fase Actual) | Implementación Real (Hardware Futuro) |
|---|---|---|---|
| Temperatura | `TemperatureSensor` | `VirtualTemperatureSensor` | `DS18B20Sensor` (1-Wire) / `SHT31Temp` (I2C) |
| Humedad | `HumiditySensor` | `VirtualHumiditySensor` | `SHT31Hum` (I2C) |
| Luz | `LightSensor` | `VirtualLightSensor` | `BH1750Sensor` (I2C) |
| Peso / Masa | `WeightSensor` | `VirtualWeightSensor` | `HX711LoadCell` (GPIO / RS485) |
| Cámara | `CameraDevice` | `VirtualCameraDevice` | `PiCameraModuleV3` (Picamera2 / CSI) |

## 3. Principio de Inversión de Dependencias
El agente de adquisición y el motor de simulación instancian factorías de sensores (`SensorFactory.create(...)`) pasando la configuración definida en variables de entorno o archivos JSON de topología.
Ninguna vista, router o modelo de base de datos importa bibliotecas nativas de Linux o Raspberry (`smbus`, `RPi.GPIO`, `picamera2`).
