import { Zone, Sensor, SensorReading, Batch, FeedingRecord, MediaFile, Alert, SystemStatus } from '../types';

const API_BASE = '/api/v1';

export async function fetchSystemStatus(): Promise<SystemStatus> {
  const res = await fetch(`${API_BASE}/system/status`);
  if (!res.ok) throw new Error('Error al obtener estado del sistema');
  return res.json();
}

export async function fetchZones(): Promise<Zone[]> {
  const res = await fetch(`${API_BASE}/zones`);
  if (!res.ok) throw new Error('Error al obtener zonas');
  return res.json();
}

export async function fetchZone(zoneId: string): Promise<Zone> {
  const res = await fetch(`${API_BASE}/zones/${zoneId}`);
  if (!res.ok) throw new Error(`Error al obtener zona ${zoneId}`);
  return res.json();
}

export async function fetchSensors(): Promise<Sensor[]> {
  const res = await fetch(`${API_BASE}/sensors`);
  if (!res.ok) throw new Error('Error al obtener sensores');
  return res.json();
}

export async function fetchSensorHistory(sensorId: string, limit: number = 60): Promise<SensorReading[]> {
  const res = await fetch(`${API_BASE}/sensors/${sensorId}/readings?limit=${limit}`);
  if (!res.ok) throw new Error(`Error al obtener historial de ${sensorId}`);
  return res.json();
}

export async function fetchBatches(): Promise<Batch[]> {
  const res = await fetch(`${API_BASE}/batches`);
  if (!res.ok) throw new Error('Error al obtener lotes');
  return res.json();
}

export async function createBatch(data: { id: string; zone_id: string; stage: string; initial_quantity: number; substrate_type?: string; notes?: string }): Promise<Batch> {
  const res = await fetch(`${API_BASE}/batches`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Error al crear lote');
  }
  return res.json();
}

export async function fetchFeedings(batchId: string): Promise<FeedingRecord[]> {
  const res = await fetch(`${API_BASE}/batches/${batchId}/feedings`);
  if (!res.ok) throw new Error('Error al obtener eventos de alimentación');
  return res.json();
}

export async function addFeeding(data: { batch_id: string; food_mass_g: number; food_type: string; notes?: string }): Promise<FeedingRecord> {
  const res = await fetch(`${API_BASE}/batches/${data.batch_id}/feedings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Error al registrar alimentación');
  return res.json();
}

export async function fetchMedia(zoneId?: string, batchId?: string): Promise<MediaFile[]> {
  const params = new URLSearchParams();
  if (zoneId) params.append('zone_id', zoneId);
  if (batchId) params.append('batch_id', batchId);
  const res = await fetch(`${API_BASE}/media?${params.toString()}`);
  if (!res.ok) throw new Error('Error al obtener galería multimedia');
  return res.json();
}

export async function uploadMedia(file: File, zoneId: string = 'ZONE-LAR', batchId?: string): Promise<MediaFile> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('zone_id', zoneId);
  if (batchId) formData.append('batch_id', batchId);

  const res = await fetch(`${API_BASE}/media/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Error al subir archivo de imagen');
  return res.json();
}

export async function fetchAlerts(): Promise<Alert[]> {
  const res = await fetch(`${API_BASE}/system/alerts`);
  if (!res.ok) throw new Error('Error al obtener alertas');
  return res.json();
}

export async function injectSimulatorFault(sensorId: string, faultType: string): Promise<void> {
  const res = await fetch(`${API_BASE}/system/simulator/fault`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sensor_id: sensorId, fault_type: faultType }),
  });
  if (!res.ok) throw new Error('Error al inyectar fallo en simulador');
}
