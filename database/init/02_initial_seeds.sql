-- ==============================================================================
-- BSF MONITOR - Seed Data Initialization
-- ==============================================================================

-- 1. Zonas
INSERT INTO zones (id, name, description, status) VALUES
    ('ZONE-REP', 'Zona de Reproducción', 'Módulo de adultos reproductores, fotoperiodo y oviposición', 'ACTIVE'),
    ('ZONE-INC', 'Zona de Incubación', 'Cámara de eclosión y cuidado de paquetes de huevos', 'ACTIVE'),
    ('ZONE-LAR', 'Zona de Larvas (Biorreactor)', 'Biorreactor de conversión de sustrato y monitoreo larvario', 'ACTIVE')
ON CONFLICT (id) DO NOTHING;

-- 2. Dispositivos Nodos
INSERT INTO devices (id, zone_id, name, device_type, connection_type, status) VALUES
    ('NODE-REP-001', 'ZONE-REP', 'Controlador Nodo Reproducción', 'SENSOR_NODE', 'RS485', 'ONLINE'),
    ('NODE-INC-001', 'ZONE-INC', 'Controlador Nodo Incubación', 'SENSOR_NODE', 'RS485', 'ONLINE'),
    ('NODE-LAR-001', 'ZONE-LAR', 'Controlador Nodo Biorreactor Larvas', 'SENSOR_NODE', 'RS485', 'ONLINE'),
    ('NODE-CAM-001', 'ZONE-LAR', 'Unidad de Cámara Digital Larvas', 'CAMERA_UNIT', 'CSI', 'ONLINE')
ON CONFLICT (id) DO NOTHING;

-- 3. Sensores
INSERT INTO sensors (id, device_id, zone_id, variable, unit, min_expected, max_expected, status) VALUES
    -- ZONE-REP
    ('REP-TEMP-001', 'NODE-REP-001', 'ZONE-REP', 'ambient_temperature', 'C', 18.0, 42.0, 'ACTIVE'),
    ('REP-HUM-001',  'NODE-REP-001', 'ZONE-REP', 'relative_humidity', '%', 30.0, 95.0, 'ACTIVE'),
    ('REP-LUX-001',  'NODE-REP-001', 'ZONE-REP', 'light_intensity', 'lux', 0.0, 25000.0, 'ACTIVE'),

    -- ZONE-INC
    ('INC-TEMP-001', 'NODE-INC-001', 'ZONE-INC', 'ambient_temperature', 'C', 20.0, 38.0, 'ACTIVE'),
    ('INC-HUM-001',  'NODE-INC-001', 'ZONE-INC', 'relative_humidity', '%', 40.0, 98.0, 'ACTIVE'),

    -- ZONE-LAR
    ('LAR-TEMP-001', 'NODE-LAR-001', 'ZONE-LAR', 'substrate_temperature', 'C', 20.0, 48.0, 'ACTIVE'),
    ('LAR-HUM-001',  'NODE-LAR-001', 'ZONE-LAR', 'relative_humidity', '%', 30.0, 95.0, 'ACTIVE'),
    ('LAR-WEIGHT-001', 'NODE-LAR-001', 'ZONE-LAR', 'weight', 'kg', 0.0, 100.0, 'ACTIVE')
ON CONFLICT (id) DO NOTHING;

-- 4. Lote de Demostración Inicial
INSERT INTO batches (id, zone_id, stage, start_date, initial_quantity, substrate_type, status, notes) VALUES
    ('BATCH-2026-001', 'ZONE-LAR', 'LARVAE', CURRENT_TIMESTAMP - INTERVAL '3 days', 15.0, 'Substrato orgánico vegetal y pulpa cítrica', 'ACTIVE', 'Lote de calibración de biorreactor')
ON CONFLICT (id) DO NOTHING;

-- 5. Alimentación Inicial
INSERT INTO feeding_records (batch_id, food_mass_g, food_type, notes, fed_at) VALUES
    ('BATCH-2026-001', 2500.0, 'Fruta y verduras trituradas', 'Alimentación inicial de siembra', CURRENT_TIMESTAMP - INTERVAL '2 days'),
    ('BATCH-2026-001', 3000.0, 'Pulpa de manzana y salvado', 'Segunda dosis programada', CURRENT_TIMESTAMP - INTERVAL '1 day')
ON CONFLICT DO NOTHING;
