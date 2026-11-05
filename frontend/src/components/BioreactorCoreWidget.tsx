import React from 'react';
import { Thermometer, Droplets, Scale, Flame, Box, CheckCircle2, AlertTriangle } from 'lucide-react';
import { SensorReading, Batch } from '../types';

interface BioreactorCoreWidgetProps {
  larvaeReadings: Record<string, SensorReading>;
  activeBatch?: Batch;
}

export const BioreactorCoreWidget: React.FC<BioreactorCoreWidgetProps> = ({ larvaeReadings, activeBatch }) => {
  const subTemp = larvaeReadings['LAR-TEMP-001']?.value ?? 33.5;
  const humidity = larvaeReadings['LAR-HUM-001']?.value ?? 68.0;
  const weight = larvaeReadings['LAR-WEIGHT-001']?.value ?? 15.8;

  const ambTemp = 24.5;
  const deltaT = subTemp - ambTemp;

  const isOptimal = subTemp >= 30.0 && subTemp <= 38.0;
  const isOverheating = subTemp > 41.0;

  return (
    <div className="p-6 rounded-2xl clean-card space-y-6">
      {/* Title & Batch Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-[11px] font-mono font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
              ZONE-LAR • BIORREACTOR CENTRAL
            </span>
            <span className="text-xs text-slate-500">
              Seguimiento del lecho de cría
            </span>
          </div>
          <h2 className="text-lg font-bold text-slate-900 mt-1">
            Condiciones del Sustrato y Actividad Larvaria
          </h2>
        </div>

        {/* Lote Activo */}
        <div className="flex items-center space-x-2.5 px-3.5 py-1.5 rounded-lg bg-slate-50 border border-slate-200">
          <Box className="w-4 h-4 text-slate-500" />
          <div className="text-xs">
            <span className="text-slate-500">Lote Activo: </span>
            <strong className="text-slate-900 font-mono">{activeBatch?.id || 'BATCH-2026-001'}</strong>
          </div>
        </div>
      </div>

      {/* 3 Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Temperatura Central del Sustrato */}
        <div className="p-4 rounded-xl bg-slate-50/70 border border-slate-200/80">
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span className="flex items-center gap-1.5 font-medium text-slate-700">
              <Thermometer className="w-4 h-4 text-orange-600" />
              Temperatura del Sustrato
            </span>
            <span className="text-[10px] font-mono text-slate-400">
              LAR-TEMP-001
            </span>
          </div>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className="text-3xl font-mono font-bold text-slate-900">
              {subTemp.toFixed(1)}
            </span>
            <span className="text-sm font-mono text-slate-500">°C</span>
          </div>
          <div className="mt-2 text-xs flex items-center justify-between text-slate-500 border-t border-slate-200/60 pt-2">
            <span>Rango ideal: 30 - 36 °C</span>
            <span className={`font-semibold flex items-center gap-1 ${isOptimal ? 'text-emerald-700' : 'text-amber-700'}`}>
              {isOptimal ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> : <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />}
              {isOptimal ? 'Normal' : 'Verificar'}
            </span>
          </div>
        </div>

        {/* Diferencial Térmico (ΔT) */}
        <div className="p-4 rounded-xl bg-slate-50/70 border border-slate-200/80">
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span className="flex items-center gap-1.5 font-medium text-slate-700">
              <Flame className="w-4 h-4 text-amber-600" />
              Gradiente Térmico (ΔT)
            </span>
            <span className="text-[10px] font-mono text-slate-400">
              Sobre Ambiente
            </span>
          </div>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className="text-3xl font-mono font-bold text-slate-900">
              +{deltaT.toFixed(1)}
            </span>
            <span className="text-sm font-mono text-slate-500">°C</span>
          </div>
          <p className="mt-2 text-xs text-slate-500 leading-relaxed border-t border-slate-200/60 pt-2">
            Calor biológico generado por la fricción y digestión larvaria en el núcleo del lecho.
          </p>
        </div>

        {/* Masa Total & Humedad */}
        <div className="p-4 rounded-xl bg-slate-50/70 border border-slate-200/80">
          <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
            <span className="flex items-center gap-1.5 font-medium text-slate-700">
              <Scale className="w-4 h-4 text-emerald-600" />
              Masa Registrada
            </span>
            <span className="text-[10px] font-mono text-slate-400">
              Celda de Carga
            </span>
          </div>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className="text-3xl font-mono font-bold text-slate-900">
              {weight.toFixed(2)}
            </span>
            <span className="text-sm font-mono text-slate-500">kg</span>
          </div>
          <div className="mt-2 text-xs flex items-center justify-between text-slate-500 border-t border-slate-200/60 pt-2">
            <span>Humedad relativa:</span>
            <span className="font-semibold text-sky-700 flex items-center gap-1">
              <Droplets className="w-3.5 h-3.5 text-sky-600" />
              {humidity.toFixed(1)}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
