import React, { useState } from 'react';
import { FlaskConical, Play, Check } from 'lucide-react';
import { Sensor } from '../types';

interface SimulatorControlsProps {
  sensors: Sensor[];
  onInjectFault: (sensorId: string, faultType: string) => Promise<void>;
}

export const SimulatorControls: React.FC<SimulatorControlsProps> = ({ sensors, onInjectFault }) => {
  const [selectedSensor, setSelectedSensor] = useState(sensors[0]?.id || 'LAR-TEMP-001');
  const [faultType, setFaultType] = useState('out_of_range');
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const handleApply = async () => {
    setLoading(true);
    setStatusMsg(null);
    try {
      await onInjectFault(selectedSensor, faultType);
      setStatusMsg(`Escenario '${faultType}' transmitido al sensor ${selectedSensor}.`);
    } catch (err: any) {
      setStatusMsg(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 rounded-xl bg-white border border-slate-200 shadow-xs space-y-5">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-slate-100 border border-slate-200 text-slate-700">
            <FlaskConical className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">
              Laboratorio de Ensayos y Resiliencia HAL
            </h3>
            <p className="text-xs text-slate-500">
              Inyección de perturbaciones controladas para pruebas de tolerancia a fallos
            </p>
          </div>
        </div>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-100 border border-slate-200 text-slate-600 font-medium">
          Hardware Abstraction Layer
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-medium text-slate-700 mb-1">Sensor a Evaluar</label>
          <select
            value={selectedSensor}
            onChange={(e) => setSelectedSensor(e.target.value)}
            className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-slate-500 focus:bg-white"
          >
            {sensors.map((s) => (
              <option key={s.id} value={s.id}>
                {s.id} — {s.variable} ({s.zone_id})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-700 mb-1">Condición Anómala</label>
          <select
            value={faultType}
            onChange={(e) => setFaultType(e.target.value)}
            className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-slate-500 focus:bg-white"
          >
            <option value="out_of_range">Sobrecalentamiento Biológico Crítico (&gt;50 °C)</option>
            <option value="disconnected">Interrupción de Bus Eléctrico (Desconexión)</option>
            <option value="frozen">Señal Atascada (Sensor Congelado)</option>
            <option value="clear">Restablecer Comportamiento Fisiológico Normal</option>
          </select>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
        <span className="text-xs text-slate-500 font-mono">
          Las lecturas anómalas se etiquetan con calidad <code className="text-amber-700 font-semibold">degraded / invalid</code>.
        </span>
        <button
          onClick={handleApply}
          disabled={loading}
          className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-900 text-white font-medium text-xs tracking-wide transition-colors flex items-center gap-1.5 shadow-xs"
        >
          <Play className="w-3.5 h-3.5" />
          <span>{loading ? 'Transmitiendo...' : 'Inyectar Escenario'}</span>
        </button>
      </div>

      {statusMsg && (
        <div className="p-3 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-mono flex items-center gap-2">
          <Check className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{statusMsg}</span>
        </div>
      )}
    </div>
  );
};
