# Especificación de Requisitos — BSF MONITOR

## 1. Requisitos Funcionales (RF)

### RF-01: Monitoreo de Zonas
- **RF-01.1**: El sistema debe monitorear la zona de reproducción (`ZONE-REP`): temperatura ambiental, humedad relativa y nivel de iluminación/fotoperiodo.
- **RF-01.2**: El sistema debe monitorear la zona de incubación (`ZONE-INC`): temperatura ambiental y humedad relativa para eclosión.
- **RF-01.3**: El sistema debe monitorear la zona de larvas (`ZONE-LAR`): temperatura del sustrato, peso/masa y módulo de cámara.

### RF-02: Adquisición y Telemetría
- **RF-02.1**: La telemetría debe recibirse vía broker MQTT (Mosquitto).
- **RF-02.2**: Cada lectura debe registrar `sensor_id`, `zone_id`, `variable`, `value`, `unit`, `timestamp` y `source` (`simulation` o `hardware`).
- **RF-02.3**: Si la calidad de la lectura es dudosa o hay fallo de sensor, debe marcarse como `quality: degraded` o `quality: invalid`.

### RF-03: Visualización en Tiempo Real
- **RF-03.1**: El dashboard web debe mostrar el estado actual de las 3 zonas sin recargar la página (WebSockets).
- **RF-03.2**: La interfaz debe indicar de forma clara e inequívoca si el sistema opera en modo `SIMULATION` o `PRODUCTION`.

### RF-04: Consulta Histórica y Exportación
- **RF-04.1**: Permitir filtrar lecturas por zona, sensor, variable y rango de fechas.
- **RF-04.2**: Permitir exportar series históricas a formato CSV.

### RF-05: Gestión de Lotes y Alimentación
- **RF-05.1**: Registro y seguimiento de lotes (código de lote, fecha de siembra, sustrato inicial, biomasa inicial).
- **RF-05.2**: Registro de eventos de alimentación (tipo de alimento, masa en gramos, observaciones).

### RF-06: Gestión Multimedia
- **RF-06.1**: Registro de fotografías con metadatos asociados (fecha, lote, zona, resolución, ruta).
- **RF-06.2**: Galería para inspección cronológica.

---

## 2. Requisitos No Funcionales (RNF)

- **RNF-01 (Mantenibilidad)**: Arquitectura desacoplada mediante Hardware Abstraction Layer (HAL).
- **RNF-02 (Confiabilidad)**: Operación continua de simulación sin fugas de memoria o pérdidas de conexión desatendidas.
- **RNF-03 (Trazabilidad)**: Prohibición expresa de sobrescribir datos históricos.
- **RNF-04 (Rendimiento)**: Latencia de push WebSocket inferior a 250ms desde la recepción MQTT.
- **RNF-05 (Seguridad)**: Configuración separada de credenciales mediante variables de entorno, sin secretos hardcodeados.
