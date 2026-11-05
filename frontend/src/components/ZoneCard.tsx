import React from 'react';
import { Zone, SensorReading } from '../types';
import { MetricCard } from './MetricCard';
import { Layers } from 'lucide-react';

interface ZoneCardProps {
  zone: Zone;
  readings: Record<string, SensorReading>;
}

export const ZoneCard: React.FC<ZoneCardProps> = ({ zone, readings }) => {
  return (
    <div className="p-5 rounded-xl bg-white border border-slate-200 shadow-xs space-y-4">
      {/* Zone Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-700">
            <Layers className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-sm font-bold text-slate-900">{zone.name}</h3>
              <span className="text-[10px] font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-600 border border-slate-200 font-medium">
                {zone.id}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">{zone.description}</p>
          </div>
        </div>

        <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 font-medium self-start sm:self-center flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
          <span>{zone.status === 'ACTIVE' ? 'Operativo' : zone.status}</span>
        </span>
      </div>

      {/* Sensor Tiles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5">
        {zone.sensors.map((sensor) => (
          <MetricCard
            key={sensor.id}
            sensor={sensor}
            reading={readings[sensor.id]}
          />
        ))}
      </div>
    </div>
  );
};
