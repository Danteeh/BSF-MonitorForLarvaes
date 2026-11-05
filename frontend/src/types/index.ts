export type Stage = 'REPRODUCTION' | 'INCUBATION' | 'LARVAE';

export interface SensorReading {
  id: number;
  sensor_id: string;
  zone_id: string;
  device_id?: string;
  batch_id?: string;
  variable: string;
  value: number;
  unit: string;
  source: 'simulation' | 'hardware';
  quality: 'valid' | 'degraded' | 'invalid';
  recorded_at: string;
  received_at: string;
}

export interface Sensor {
  id: string;
  device_id?: string;
  zone_id: string;
  variable: string;
  unit: string;
  min_expected?: number;
  max_expected?: number;
  status: 'ACTIVE' | 'FAULT' | 'DISCONNECTED';
  latest_reading?: SensorReading;
}

export interface Zone {
  id: string;
  name: string;
  description?: string;
  status: 'ACTIVE' | 'INACTIVE' | 'MAINTENANCE';
  sensors: Sensor[];
}

export interface Batch {
  id: string;
  zone_id: string;
  stage: Stage;
  start_date: string;
  end_date?: string;
  initial_quantity: number;
  substrate_type?: string;
  final_yield?: number;
  status: 'ACTIVE' | 'COMPLETED' | 'ARCHIVED';
  notes?: string;
  created_at: string;
}

export interface FeedingRecord {
  id: number;
  batch_id: string;
  food_mass_g: number;
  food_type: string;
  notes?: string;
  fed_at: string;
}

export interface MediaFile {
  id: number;
  filename: string;
  filepath: string;
  media_type: 'IMAGE' | 'VIDEO';
  zone_id?: string;
  batch_id?: string;
  file_size_bytes: number;
  resolution?: string;
  source: 'simulation' | 'hardware' | 'upload';
  captured_at: string;
}

export interface Alert {
  id: number;
  zone_id: string;
  sensor_id?: string;
  severity: 'INFO' | 'WARNING' | 'CRITICAL';
  title: string;
  message: string;
  is_resolved: boolean;
  created_at: string;
}

export interface SystemStatus {
  mode: 'SIMULATION' | 'PRODUCTION';
  status: 'OPERATIONAL' | 'DEGRADED';
  backend_version: string;
  active_zones: number;
  active_sensors: number;
  mqtt_connected: boolean;
  database_connected: boolean;
  timestamp: string;
}
