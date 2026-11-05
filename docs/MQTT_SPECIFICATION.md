# Especificación MQTT — BSF MONITOR

El protocolo de telemetría entre nodos/simulador y el backend es **MQTT 3.1.1 / 5.0** a través de **Eclipse Mosquitto**.

## 1. Convención de Tópicos

### Telemetría de Zonas:
```text
bsf/{zone_id}/{variable}
```
Ejemplos:
- `bsf/reproduction/temperature`
- `bsf/reproduction/humidity`
- `bsf/reproduction/light`
- `bsf/incubation/temperature`
- `bsf/incubation/humidity`
- `bsf/larvae/temperature`
- `bsf/larvae/humidity`
- `bsf/larvae/weight`

### Estado de Nodos y Dispositivos:
- `bsf/devices/{device_id}/status`
- `bsf/system/alerts`
- `bsf/camera/{zone_id}/status`

---

## 2. Esquema del Payload JSON

Cada mensaje de telemetría publicado en un tópico `bsf/...` debe cumplir la siguiente estructura:

```json
{
  "device_id": "NODE-LAR-001",
  "sensor_id": "LAR-TEMP-001",
  "zone_id": "ZONE-LAR",
  "variable": "substrate_temperature",
  "value": 28.45,
  "unit": "C",
  "timestamp": "2026-11-05T17:15:00.000Z",
  "source": "simulation",
  "quality": "valid"
}
```

### Campos:
- `device_id`: Identificador del microcontrolador o nodo adquisidor (string, requerido).
- `sensor_id`: Identificador único del sensor físico/virtual (string, requerido).
- `zone_id`: Zona asociada (`ZONE-REP`, `ZONE-INC`, `ZONE-LAR`) (string, requerido).
- `variable`: Variable biológica o física medida (string, requerido).
- `value`: Valor numérico de punto flotante (float, requerido).
- `unit`: Unidad internacional (`C`, `%`, `lux`, `kg`, `g`) (string, requerido).
- `timestamp`: Marca de tiempo UTC en formato ISO 8601 (string, requerido).
- `source`: Origen del dato: `"simulation"` o `"hardware"` (string, requerido).
- `quality`: Estado de la lectura: `"valid"`, `"degraded"`, `"invalid"` (string, requerido).

---

## 3. Políticas de Entrega
- **QoS 1**: Utilizado para lecturas estándar y cambios de estado de dispositivos para asegurar al menos una entrega.
- **Retención (Retain flag)**: Habilitado únicamente para el último estado del dispositivo en `bsf/devices/{device_id}/status`.
- **Last Will and Testament (LWT)**: Configurado en el tópico de estado del nodo para publicar `{"status": "OFFLINE"}` en caso de desconexión imprevista.
