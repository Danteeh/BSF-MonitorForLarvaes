import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Sidebar, NavTab } from './components/Sidebar';
import { BioreactorCoreWidget } from './components/BioreactorCoreWidget';
import { BioreactorDigitalTwin } from './components/BioreactorDigitalTwin';
import { LifeCycleWidget } from './components/LifeCycleWidget';
import { ExperimentalProtocol } from './components/ExperimentalProtocol';
import { MacroInspectionViewer } from './components/MacroInspectionViewer';
import { ZoneCard } from './components/ZoneCard';
import { LiveTelemetryChart } from './components/LiveTelemetryChart';
import { BatchManagerModal } from './components/BatchManagerModal';
import { CameraUploadModal } from './components/CameraUploadModal';
import { SimulatorControls } from './components/SimulatorControls';
import { wsClient } from './services/websocket';
import {
  fetchSystemStatus,
  fetchZones,
  fetchSensors,
  fetchSensorHistory,
  fetchBatches,
  createBatch,
  addFeeding,
  fetchMedia,
  uploadMedia,
  fetchAlerts,
  injectSimulatorFault
} from './services/api';
import { Zone, Sensor, SensorReading, Batch, MediaFile, Alert, SystemStatus } from './types';
import { Plus, Camera, Download, Layers, Activity, BookOpen, Microscope } from 'lucide-react';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<NavTab>('overview');
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [wsConnected, setWsConnected] = useState(false);
  const [zones, setZones] = useState<Zone[]>([]);
  const [sensors, setSensors] = useState<Sensor[]>([]);
  const [batches, setBatches] = useState<Batch[]>([]);
  const [mediaFiles, setMediaFiles] = useState<MediaFile[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);

  // Telemetry buffer keyed by sensor_id
  const [latestReadings, setLatestReadings] = useState<Record<string, SensorReading>>({});
  const [historicalSeries, setHistoricalSeries] = useState<Record<string, SensorReading[]>>({});

  // Modals
  const [isBatchModalOpen, setIsBatchModalOpen] = useState(false);
  const [isCameraModalOpen, setIsCameraModalOpen] = useState(false);

  // Selected sensor for Telemetry tab
  const [selectedHistorySensor, setSelectedHistorySensor] = useState<string>('LAR-TEMP-001');

  // Initial Data Fetch
  const loadInitialData = async () => {
    try {
      const [statusData, zonesData, sensorsData, batchesData, mediaData, alertsData] = await Promise.all([
        fetchSystemStatus().catch(() => null),
        fetchZones().catch(() => []),
        fetchSensors().catch(() => []),
        fetchBatches().catch(() => []),
        fetchMedia().catch(() => []),
        fetchAlerts().catch(() => [])
      ]);

      if (statusData) setSystemStatus(statusData);
      setZones(zonesData);
      setSensors(sensorsData);
      setBatches(batchesData);
      setMediaFiles(mediaData);
      setAlerts(alertsData);

      // Prepopulate latest readings from zones
      const initialMap: Record<string, SensorReading> = {};
      zonesData.forEach((z) => {
        z.sensors.forEach((s) => {
          if (s.latest_reading) {
            initialMap[s.id] = s.latest_reading;
          }
        });
      });
      setLatestReadings(initialMap);

      // Fetch initial history for default sensor
      const hist = await fetchSensorHistory('LAR-TEMP-001', 60).catch(() => []);
      setHistoricalSeries((prev) => ({ ...prev, 'LAR-TEMP-001': hist }));
    } catch (e) {
      console.error('Error fetching initial data:', e);
    }
  };

  useEffect(() => {
    loadInitialData();

    wsClient.connect();
    const unsubStatus = wsClient.onStatusChange(setWsConnected);

    const unsubTelemetry = wsClient.subscribe((event) => {
      if (event.type === 'telemetry' && event.data) {
        const reading: SensorReading = {
          id: Date.now(),
          sensor_id: event.data.sensor_id,
          zone_id: event.data.zone_id,
          batch_id: event.data.batch_id,
          variable: event.data.variable,
          value: parseFloat(event.data.value),
          unit: event.data.unit,
          source: event.data.source || 'simulation',
          quality: event.data.quality || 'valid',
          recorded_at: event.data.timestamp || new Date().toISOString(),
          received_at: new Date().toISOString()
        };

        setLatestReadings((prev) => ({
          ...prev,
          [reading.sensor_id]: reading
        }));

        setHistoricalSeries((prev) => {
          const currentList = prev[reading.sensor_id] || [];
          const updated = [...currentList, reading].slice(-80);
          return { ...prev, [reading.sensor_id]: updated };
        });
      } else if (event.type === 'alert') {
        const newAlert: Alert = {
          id: Date.now(),
          zone_id: event.zone_id,
          severity: event.severity,
          title: event.title,
          message: event.message,
          is_resolved: false,
          created_at: new Date().toISOString()
        };
        setAlerts((prev) => [newAlert, ...prev]);
      }
    });

    return () => {
      unsubStatus();
      unsubTelemetry();
      wsClient.disconnect();
    };
  }, []);

  const handleSelectHistorySensor = async (sId: string) => {
    setSelectedHistorySensor(sId);
    if (!historicalSeries[sId] || historicalSeries[sId].length === 0) {
      const hist = await fetchSensorHistory(sId, 80).catch(() => []);
      setHistoricalSeries((prev) => ({ ...prev, [sId]: hist }));
    }
  };

  const handleExportCSV = () => {
    const data = historicalSeries[selectedHistorySensor] || [];
    if (data.length === 0) {
      alert('No hay datos históricos para exportar');
      return;
    }
    const headers = ['id', 'sensor_id', 'zone_id', 'variable', 'value', 'unit', 'quality', 'source', 'recorded_at'];
    const rows = data.map((d) => [
      d.id,
      d.sensor_id,
      d.zone_id,
      d.variable,
      d.value,
      d.unit,
      d.quality,
      d.source,
      d.recorded_at
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `bsf_investigacion_${selectedHistorySensor}_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleCreateBatch = async (data: any) => {
    const newB = await createBatch(data);
    setBatches((prev) => [newB, ...prev]);
  };

  const handleAddFeeding = async (data: any) => {
    await addFeeding(data);
    alert('Dosis nutricional registrada exitosamente.');
  };

  const handleUploadImage = async (file: File, zoneId: string, batchId?: string) => {
    const newMedia = await uploadMedia(file, zoneId, batchId);
    setMediaFiles((prev) => [newMedia, ...prev]);
  };

  const handleInjectFault = async (sensorId: string, faultType: string) => {
    await injectSimulatorFault(sensorId, faultType);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f8fafc] text-slate-900">
      <Header
        systemStatus={systemStatus}
        wsConnected={wsConnected}
        alertCount={alerts.filter((a) => !a.is_resolved).length}
      />

      <div className="flex-1 flex overflow-hidden">
        <Sidebar currentTab={currentTab} onTabChange={setCurrentTab} />

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Top Quick Actions Bar */}
          <div className="flex flex-wrap items-center justify-between gap-4 pb-1">
            <div>
              <h2 className="text-base font-bold text-slate-900">
                {currentTab === 'overview' && 'Biorreactor Central & Topología del Sistema'}
                {currentTab === 'zones' && 'Zonas de Cría y Monitoreo Ambiental'}
                {currentTab === 'protocol' && 'Protocolo Científico & Ecuaciones de Bioconversión'}
                {currentTab === 'macro' && 'Morfometría Óptica & Fotografía Real de Muestras'}
                {currentTab === 'batches' && 'Trazabilidad de Lotes y Formulación Nutricional'}
                {currentTab === 'telemetry' && 'Telemetría Multivariable en Tiempo Real'}
                {currentTab === 'simulator' && 'Laboratorio de Resiliencia y Control HAL'}
              </h2>
              <p className="text-xs text-slate-500 font-sans mt-0.5">
                Investigación Entomológica de <span className="italic">Hermetia illucens</span> • Monitoreo Continuo
              </p>
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={() => setIsBatchModalOpen(true)}
                className="px-3.5 py-1.5 rounded-lg bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 text-xs font-medium flex items-center gap-1.5 transition-colors shadow-2xs"
              >
                <Plus className="w-3.5 h-3.5 text-emerald-700" />
                <span>Registrar Lote / Dieta</span>
              </button>

              <button
                onClick={() => setIsCameraModalOpen(true)}
                className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-medium flex items-center gap-1.5 transition-colors shadow-xs"
              >
                <Camera className="w-3.5 h-3.5" />
                <span>Cargar Fotografía</span>
              </button>
            </div>
          </div>

          {/* TAB 1: OVERVIEW / BIORREACTOR CENTRAL */}
          {currentTab === 'overview' && (
            <div className="space-y-6">
              <BioreactorCoreWidget
                larvaeReadings={latestReadings}
                activeBatch={batches[0]}
              />

              <BioreactorDigitalTwin
                zones={zones}
                readings={latestReadings}
                activeBatch={batches[0]}
                onOpenPhotoViewer={() => setCurrentTab('macro')}
              />

              <LifeCycleWidget />
            </div>
          )}

          {/* TAB 2: ZONAS DEL PROCESO */}
          {currentTab === 'zones' && (
            <div className="space-y-5">
              <div className="grid grid-cols-1 gap-5">
                {zones.map((zone) => (
                  <ZoneCard
                    key={zone.id}
                    zone={zone}
                    readings={latestReadings}
                  />
                ))}
              </div>
            </div>
          )}

          {/* TAB 3: PROTOCOLO & ECUACIONES */}
          {currentTab === 'protocol' && (
            <div className="space-y-6">
              <ExperimentalProtocol
                batches={batches}
                currentSubstrateTemp={latestReadings['LAR-TEMP-001']?.value ?? 34.2}
              />
            </div>
          )}

          {/* TAB 4: MORFOMETRÍA ÓPTICA */}
          {currentTab === 'macro' && (
            <div className="space-y-6">
              <MacroInspectionViewer
                mediaFiles={mediaFiles}
                onUploadClick={() => setIsCameraModalOpen(true)}
              />
            </div>
          )}

          {/* TAB 5: LOTES & DIETAS */}
          {currentTab === 'batches' && (
            <div className="space-y-5">
              <div className="p-6 rounded-xl bg-white border border-slate-200 shadow-xs space-y-4">
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">Registro de Lotes de Producción</h3>
                    <p className="text-xs text-slate-500">Trazabilidad completa de ciclos de bioconversión</p>
                  </div>
                  <button
                    onClick={() => setIsBatchModalOpen(true)}
                    className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-xs flex items-center gap-1.5 transition-colors shadow-xs"
                  >
                    <Plus className="w-3.5 h-3.5" /> Registrar Lote
                  </button>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs font-sans">
                    <thead className="border-b border-slate-100 text-slate-500">
                      <tr>
                        <th className="py-2.5 px-3 font-semibold">Código</th>
                        <th className="py-2.5 px-3 font-semibold">Módulo</th>
                        <th className="py-2.5 px-3 font-semibold">Etapa Ontogénica</th>
                        <th className="py-2.5 px-3 font-semibold">Cantidad Inicial</th>
                        <th className="py-2.5 px-3 font-semibold">Dieta / Sustrato</th>
                        <th className="py-2.5 px-3 font-semibold">Estado</th>
                        <th className="py-2.5 px-3 font-semibold">Fecha Inicio</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {batches.map((b) => (
                        <tr key={b.id} className="hover:bg-slate-50/70 transition-colors">
                          <td className="py-2.5 px-3 font-mono font-semibold text-emerald-800">{b.id}</td>
                          <td className="py-2.5 px-3 font-mono text-slate-600">{b.zone_id}</td>
                          <td className="py-2.5 px-3 text-slate-700 font-medium">{b.stage}</td>
                          <td className="py-2.5 px-3 font-mono text-slate-800 font-semibold">{b.initial_quantity} kg</td>
                          <td className="py-2.5 px-3 text-slate-600">{b.substrate_type || '--'}</td>
                          <td className="py-2.5 px-3">
                            <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 text-[10px] font-medium">
                              {b.status}
                            </span>
                          </td>
                          <td className="py-2.5 px-3 text-slate-500 font-mono">
                            {new Date(b.start_date).toLocaleDateString('es-ES')}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* TAB 6: MATRIZ DE TELEMETRÍA */}
          {currentTab === 'telemetry' && (
            <div className="space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-3 p-4 rounded-xl bg-white border border-slate-200 shadow-xs">
                <div className="flex items-center space-x-3">
                  <span className="text-xs font-medium text-slate-700">Sensor a Graficar:</span>
                  <select
                    value={selectedHistorySensor}
                    onChange={(e) => handleSelectHistorySensor(e.target.value)}
                    className="px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 text-slate-800 font-mono text-xs focus:outline-none focus:border-emerald-600 focus:bg-white"
                  >
                    {sensors.map((s) => (
                      <option key={s.id} value={s.id}>
                        {s.id} — {s.variable} ({s.zone_id})
                      </option>
                    ))}
                  </select>
                </div>

                <button
                  onClick={handleExportCSV}
                  className="px-3.5 py-1.5 rounded-lg bg-white hover:bg-slate-50 text-slate-700 text-xs font-medium flex items-center gap-2 border border-slate-200 shadow-2xs transition-colors"
                >
                  <Download className="w-3.5 h-3.5 text-slate-500" />
                  <span>Exportar CSV de Datos</span>
                </button>
              </div>

              <LiveTelemetryChart
                title={`Curva de Telemetría: ${selectedHistorySensor}`}
                variableName={selectedHistorySensor}
                data={historicalSeries[selectedHistorySensor] || []}
                unit={sensors.find((s) => s.id === selectedHistorySensor)?.unit || ''}
                color="#16a34a"
              />

              <div className="grid grid-cols-1 gap-5 pt-2">
                {zones.map((zone) => (
                  <ZoneCard
                    key={zone.id}
                    zone={zone}
                    readings={latestReadings}
                  />
                ))}
              </div>
            </div>
          )}

          {/* TAB 7: SIMULATOR */}
          {currentTab === 'simulator' && (
            <div className="space-y-5">
              <SimulatorControls
                sensors={sensors}
                onInjectFault={handleInjectFault}
              />
            </div>
          )}
        </main>
      </div>

      {/* Modals */}
      <BatchManagerModal
        isOpen={isBatchModalOpen}
        onClose={() => setIsBatchModalOpen(false)}
        batches={batches}
        onCreateBatch={handleCreateBatch}
        onAddFeeding={handleAddFeeding}
      />

      <CameraUploadModal
        isOpen={isCameraModalOpen}
        onClose={() => setIsCameraModalOpen(false)}
        mediaFiles={mediaFiles}
        batches={batches}
        onUploadImage={handleUploadImage}
      />
    </div>
  );
};
