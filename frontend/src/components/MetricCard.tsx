import React from 'react';
import { Sensor, SensorReading } from '../types';
import { Thermometer, Droplets, Sun, Scale, Clock, Activity } from 'lucide-react';

interface MetricCardProps {
  sensor: Sensor;
  reading?: SensorReading;
}

export const MetricCard: React.FC<MetricCardProps> = ({ sensor, reading }) => {
  const getIcon = (variable: string) => {
    switch (variable) {
      case 'ambient_temperature':
      case 'substrate_temperature':
        return <Thermometer className="w-4 h-4 text-orange-600" />;
      case 'relative_humidity':
        return <Droplets className="w-4 h-4 text-sky-600" />;
      case 'light_intensity':
        return <Sun className="w-4 h-4 text-amber-500" />;
      case 'weight':
        return <Scale className="w-4 h-4 text-emerald-600" />;
      default:
        return <Activity className="w-4 h-4 text-slate-500" />;
    }
  };

  const getVariableLabel = (variable: string) => {
    switch (variable) {
      case 'ambient_temperature':
        return 'Temperatura Ambiental';
      case 'substrate_temperature':
        return 'Temperatura del Sustrato';
      case 'relative_humidity':
        return 'Humedad Relativa';
      case 'light_intensity':
        return 'Intensidad Lumínica';
      case 'weight':
        return 'Masa Total';
      default:
        return variable.replace('_', ' ');
    }
  };

  const curVal = reading ? reading.value : (sensor.latest_reading?.value ?? null);
  const curQuality = reading ? reading.quality : (sensor.latest_reading?.quality ?? 'valid');
  const curSource = reading ? reading.source : (sensor.latest_reading?.source ?? 'simulation');
  const recordedAt = reading ? reading.recorded_at : sensor.latest_reading?.recorded_at;

  const isInvalid = curQuality === 'invalid';
  const isDegraded = curQuality === 'degraded';

  return (
    <div className={`p-4 rounded-xl clean-card transition-shadow hover:shadow-md ${
      isInvalid ? 'border-red-300 bg-red-50/20' : ''
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-lg bg-slate-50 border border-slate-200">
            {getIcon(sensor.variable)}
          </div>
          <div>
            <h4 className="text-xs font-semibold text-slate-800">
              {getVariableLabel(sensor.variable)}
            </h4>
            <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wide">
              {sensor.id}
            </span>
          </div>
        </div>

        {/* Quality / Source Badges */}
        <div className="flex flex-col items-end space-y-1">
          <span className={`text-[9px] font-mono uppercase px-2 py-0.5 rounded border ${
            isInvalid
              ? 'bg-red-50 border-red-200 text-red-700'
              : isDegraded
              ? 'bg-amber-50 border-amber-200 text-amber-700'
              : 'bg-emerald-50 border-emerald-200 text-emerald-700'
          }`}>
            {curQuality}
          </span>
          <span className="text-[9px] font-mono text-slate-400">
            {curSource}
          </span>
        </div>
      </div>

      {/* Main Metric Value */}
      <div className="mt-3 flex items-baseline justify-between">
        <div className="flex items-baseline space-x-1.5">
          <span className={`text-2xl font-mono font-bold tracking-tight ${
            isInvalid ? 'text-red-600 line-through' : 'text-slate-900'
          }`}>
            {curVal !== null ? curVal.toFixed(1) : '--.-'}
          </span>
          <span className="text-xs font-mono text-slate-500 font-semibold">
            {sensor.unit}
          </span>
        </div>

        {/* Min / Max Expected */}
        {sensor.min_expected !== undefined && sensor.max_expected !== undefined && (
          <div className="text-[10px] font-mono text-right text-slate-500">
            <span>Rango: </span>
            <span className="text-slate-700 font-medium">{sensor.min_expected} - {sensor.max_expected} {sensor.unit}</span>
          </div>
        )}
      </div>

      {/* Footer Timestamp */}
      <div className="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-[10px] font-mono text-slate-400">
        <div className="flex items-center space-x-1">
          <Clock className="w-3 h-3 text-slate-400" />
          <span>
            {recordedAt ? new Date(recordedAt).toLocaleTimeString('es-ES') : 'Esperando datos'}
          </span>
        </div>
        <span className="text-slate-500 font-sans">
          Sensor en línea
        </span>
      </div>
    </div>
  );
};
