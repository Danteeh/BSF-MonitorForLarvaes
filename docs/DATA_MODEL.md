# Modelo de Datos Relacional — BSF MONITOR

La base de datos principal es **PostgreSQL 16**. A continuación se detallan las entidades nucleares del modelo relacional.

```mermaid
erDiagram
    ZONES ||--o{ DEVICES : contains
    ZONES ||--o{ BATCHES : hosts
    DEVICES ||--o{ SENSORS : has
    SENSORS ||--o{ SENSOR_READINGS : produces
    BATCHES ||--o{ FEEDING_RECORDS : logs
    BATCHES ||--o{ BATCH_EVENTS : triggers
    BATCHES ||--o{ MEDIA_FILES : associates
    ZONES ||--o{ MEDIA_FILES : records

    ZONES {
        string id PK "ZONE-REP, ZONE-INC, ZONE-LAR"
        string name
        string description
        string status "ACTIVE, INACTIVE, MAINTENANCE"
        timestamp created_at
    }

    DEVICES {
        string id PK "NODE-REP-001, NODE-LAR-001"
        string zone_id FK
        string name
        string device_type "CONTROLLER, SENSOR_NODE, CAMERA_UNIT"
        string connection_type "RS485, I2C, MQTT, CSI"
        string status "ONLINE, OFFLINE, ERROR"
        timestamp last_seen
    }

    SENSORS {
        string id PK "REP-TEMP-001, LAR-WEIGHT-001"
        string device_id FK
        string zone_id FK
        string variable "ambient_temperature, relative_humidity, substrate_temperature, weight, light_intensity"
        string unit "C, %, kg, lux"
        float min_expected
        float max_expected
        string status "ACTIVE, FAULT, DISCONNECTED"
    }

    SENSOR_READINGS {
        bigserial id PK
        string sensor_id FK
        string zone_id FK
        string device_id FK
        string batch_id FK "nullable"
        string variable
        float value
        string unit
        string source "simulation, hardware"
        string quality "valid, degraded, invalid"
        timestamp recorded_at "timestamp UTC sensor"
        timestamp received_at "timestamp UTC backend"
    }

    BATCHES {
        string id PK "BATCH-2026-001"
        string zone_id FK
        string stage "REPRODUCTION, INCUBATION, LARVAE"
        timestamp start_date
        timestamp end_date
        float initial_quantity
        string substrate_type
        float final_yield
        string status "ACTIVE, COMPLETED, ARCHIVED"
    }

    FEEDING_RECORDS {
        serial id PK
        string batch_id FK
        float food_mass_g
        string food_type
        text notes
        timestamp fed_at
    }

    MEDIA_FILES {
        serial id PK
        string filename
        string filepath
        string media_type "IMAGE, VIDEO"
        string zone_id FK
        string batch_id FK
        integer file_size_bytes
        string resolution
        string source "simulation, hardware, upload"
        timestamp captured_at
    }
```

## Índices Principales Recomendados
- `sensor_readings(sensor_id, recorded_at DESC)`
- `sensor_readings(zone_id, recorded_at DESC)`
- `sensor_readings(recorded_at DESC)`
- `batches(status, stage)`
- `media_files(zone_id, captured_at DESC)`
