# Especificación de API REST y WebSockets — BSF MONITOR

La API está desarrollada en **FastAPI** bajo el prefijo base `/api/v1`. La documentación OpenAPI interactiva Swagger se expone en `/docs`.

## 1. Endpoints de Sistema y Salud
- `GET /api/v1/system/status`: Retorna estado del backend, broker MQTT, base de datos y modo (`SIMULATION` o `PRODUCTION`).

## 2. Endpoints de Zonas
- `GET /api/v1/zones`: Lista todas las zonas registradas y su resumen de sensores.
- `GET /api/v1/zones/{zone_id}`: Detalle de una zona con última lectura de cada sensor.

## 3. Endpoints de Sensores y Telemetría
- `GET /api/v1/sensors`: Listado general de sensores.
- `GET /api/v1/sensors/{sensor_id}`: Metadata del sensor.
- `GET /api/v1/sensors/{sensor_id}/readings`: Historial temporal del sensor con filtros `start_time`, `end_time` y `limit`.
- `GET /api/v1/readings/latest`: Diccionario con la última lectura de cada sensor activo.
- `POST /api/v1/readings`: Ingesta directa de lecturas (vía HTTP, además de MQTT).

## 4. Endpoints de Lotes y Alimentación
- `GET /api/v1/batches`: Lista lotes con filtro por `status` y `stage`.
- `POST /api/v1/batches`: Crea un nuevo lote de producción.
- `GET /api/v1/batches/{batch_id}`: Detalle de un lote específico.
- `POST /api/v1/feeding`: Registra un evento de alimentación para un lote.
- `GET /api/v1/batches/{batch_id}/feedings`: Historial de alimentación de un lote.

## 5. Endpoints Multimedia
- `GET /api/v1/media`: Galería de archivos multimedia registrados.
- `POST /api/v1/media/upload`: Carga de imagen real con metadata de zona y lote.
- `GET /api/v1/media/{media_id}`: Consulta de metadatos o archivo binario.

## 6. Endpoints de Simulación
- `POST /api/v1/simulator/control`: Pausa, reanuda o cambia la velocidad del motor de simulación.
- `POST /api/v1/simulator/fault`: Inyecta un fallo simulado (ej. sensor desconectado, valor fuera de rango, deriva).

## 7. WebSockets
- `WS /ws/telemetry`: Conexión de streaming en tiempo real.
  - Al conectarse, el servidor envía snapshot inicial del estado de todas las zonas.
  - Publica eventos JSON de telemetría a medida que ingresan por MQTT.
  - Envía pings de latencia periódicos.
