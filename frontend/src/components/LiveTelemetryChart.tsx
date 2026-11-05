import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts';
import { SensorReading } from '../types';

interface LiveTelemetryChartProps {
  title: string;
  variableName: string;
  data: SensorReading[];
  color?: string;
  unit: string;
}

export const LiveTelemetryChart: React.FC<LiveTelemetryChartProps> = ({
  title,
  variableName,
  data,
  color = '#16a34a', // Verde esmeralda natural
  unit
}) => {
  const chartData = data.map((d) => ({
    time: new Date(d.recorded_at).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
    value: d.value,
    quality: d.quality
  }));

  return (
    <div className="p-5 rounded-xl bg-white border border-slate-200 shadow-xs space-y-4">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h4 className="text-sm font-bold text-slate-900">{title}</h4>
          <span className="text-[11px] font-mono text-slate-500">
            Serie temporal • {data.length} puntos adquiridos
          </span>
        </div>
        <span className="text-xs font-mono text-slate-600 bg-slate-100 px-2.5 py-1 rounded border border-slate-200">
          Unidad: <strong className="text-slate-800">{unit}</strong>
        </span>
      </div>

      <div className="h-64 w-full">
        {data.length === 0 ? (
          <div className="h-full flex items-center justify-center text-xs font-mono text-slate-400">
            Esperando transmisión de telemetría por WebSocket...
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id={`grad_${variableName}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={color} stopOpacity={0.15} />
                  <stop offset="95%" stopColor={color} stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis
                dataKey="time"
                stroke="#cbd5e1"
                tick={{ fontSize: 10, fill: '#64748b' }}
                tickLine={false}
              />
              <YAxis
                stroke="#cbd5e1"
                tick={{ fontSize: 10, fill: '#64748b' }}
                tickLine={false}
                domain={['auto', 'auto']}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#ffffff',
                  borderColor: '#e2e8f0',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
                  fontSize: '12px',
                  color: '#0f172a'
                }}
                labelStyle={{ color: '#64748b', fontWeight: 500 }}
                formatter={(val: any) => [`${val} ${unit}`, 'Lectura']}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke={color}
                strokeWidth={2}
                fill={`url(#grad_${variableName})`}
                isAnimationActive={false}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};
