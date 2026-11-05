-- ==============================================================================
-- BSF MONITOR - PostgreSQL Schema Initialization
-- ==============================================================================

-- 1. Zonas de Producción
CREATE TABLE IF NOT EXISTS zones (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Dispositivos / Nodos Adquisidores
CREATE TABLE IF NOT EXISTS devices (
    id VARCHAR(32) PRIMARY KEY,
    zone_id VARCHAR(32) REFERENCES zones(id) ON DELETE SET NULL,
    name VARCHAR(100) NOT NULL,
    device_type VARCHAR(50) NOT NULL, -- CONTROLLER, SENSOR_NODE, CAMERA_UNIT
    connection_type VARCHAR(50) NOT NULL, -- RS485, I2C, MQTT, CSI
    status VARCHAR(32) NOT NULL DEFAULT 'ONLINE', -- ONLINE, OFFLINE, ERROR
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Catálogo de Sensores
CREATE TABLE IF NOT EXISTS sensors (
    id VARCHAR(32) PRIMARY KEY,
    device_id VARCHAR(32) REFERENCES devices(id) ON DELETE CASCADE,
    zone_id VARCHAR(32) REFERENCES zones(id) ON DELETE CASCADE,
    variable VARCHAR(64) NOT NULL, -- ambient_temperature, relative_humidity, substrate_temperature, weight, light_intensity
    unit VARCHAR(16) NOT NULL, -- C, %, kg, lux
    min_expected DOUBLE PRECISION,
    max_expected DOUBLE PRECISION,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE', -- ACTIVE, FAULT, DISCONNECTED
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Lotes de Producción
CREATE TABLE IF NOT EXISTS batches (
    id VARCHAR(64) PRIMARY KEY,
    zone_id VARCHAR(32) REFERENCES zones(id) ON DELETE RESTRICT,
    stage VARCHAR(32) NOT NULL DEFAULT 'LARVAE', -- REPRODUCTION, INCUBATION, LARVAE
    start_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP WITH TIME ZONE,
    initial_quantity DOUBLE PRECISION DEFAULT 0.0,
    substrate_type VARCHAR(100),
    final_yield DOUBLE PRECISION,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE', -- ACTIVE, COMPLETED, ARCHIVED
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Registro de Alimentación
CREATE TABLE IF NOT EXISTS feeding_records (
    id BIGSERIAL PRIMARY KEY,
    batch_id VARCHAR(64) REFERENCES batches(id) ON DELETE CASCADE,
    food_mass_g DOUBLE PRECISION NOT NULL,
    food_type VARCHAR(100) NOT NULL,
    notes TEXT,
    fed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Historial de Mediciones (Telemetría de Sensores)
CREATE TABLE IF NOT EXISTS sensor_readings (
    id BIGSERIAL PRIMARY KEY,
    sensor_id VARCHAR(32) NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    zone_id VARCHAR(32) NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    device_id VARCHAR(32) REFERENCES devices(id) ON DELETE SET NULL,
    batch_id VARCHAR(64) REFERENCES batches(id) ON DELETE SET NULL,
    variable VARCHAR(64) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(16) NOT NULL,
    source VARCHAR(20) NOT NULL DEFAULT 'simulation', -- simulation, hardware
    quality VARCHAR(20) NOT NULL DEFAULT 'valid', -- valid, degraded, invalid
    recorded_at TIMESTAMP WITH TIME ZONE NOT NULL,
    received_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices de alto rendimiento para telemetría
CREATE INDEX IF NOT EXISTS idx_readings_sensor_time ON sensor_readings (sensor_id, recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_readings_zone_time ON sensor_readings (zone_id, recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_readings_recorded_at ON sensor_readings (recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_readings_variable ON sensor_readings (variable);

-- 7. Metadatos de Archivos Multimedia (Cámaras y Fotos)
CREATE TABLE IF NOT EXISTS media_files (
    id BIGSERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(512) NOT NULL,
    media_type VARCHAR(20) NOT NULL DEFAULT 'IMAGE', -- IMAGE, VIDEO
    zone_id VARCHAR(32) REFERENCES zones(id) ON DELETE SET NULL,
    batch_id VARCHAR(64) REFERENCES batches(id) ON DELETE SET NULL,
    file_size_bytes BIGINT NOT NULL DEFAULT 0,
    resolution VARCHAR(32),
    source VARCHAR(20) NOT NULL DEFAULT 'simulation', -- simulation, hardware, upload
    captured_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_media_zone_captured ON media_files (zone_id, captured_at DESC);

-- 8. Alertas del Sistema
CREATE TABLE IF NOT EXISTS alerts (
    id BIGSERIAL PRIMARY KEY,
    zone_id VARCHAR(32) REFERENCES zones(id) ON DELETE CASCADE,
    sensor_id VARCHAR(32) REFERENCES sensors(id) ON DELETE SET NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'WARNING', -- INFO, WARNING, CRITICAL
    title VARCHAR(128) NOT NULL,
    message TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_alerts_unresolved ON alerts (is_resolved, created_at DESC);
