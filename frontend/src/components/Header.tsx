import React, { useState, useEffect } from 'react';
import { Clock, AlertCircle, Layers, Activity, Microscope } from 'lucide-react';
import { SystemStatus } from '../types';

interface HeaderProps {
  systemStatus: SystemStatus | null;
  wsConnected: boolean;
  alertCount: number;
}

export const Header: React.FC<HeaderProps> = ({ systemStatus, wsConnected, alertCount }) => {
  const [time, setTime] = useState<string>('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTime(now.toLocaleTimeString('es-ES', { hour12: false }) + ' (UTC-5)');
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-16 border-b border-slate-200 bg-white px-6 flex items-center justify-between sticky top-0 z-30 shadow-xs">
      {/* Brand & Project Identity - Sencillo y Grato */}
      <div className="flex items-center space-x-3.5">
        <div className="w-9 h-9 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-700 shadow-xs">
          <Microscope className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-sm font-bold tracking-tight text-slate-900">
              BSF MONITOR
            </h1>
            <span className="text-[10px] font-mono text-slate-600 bg-slate-100 border border-slate-200 px-2 py-0.5 rounded font-medium">
              v1.0 • Lab
            </span>
          </div>
          <p className="text-xs text-slate-500 font-normal">
            Sistema de Monitoreo Biológico • <span className="italic text-slate-600">Hermetia illucens</span>
          </p>
        </div>
      </div>

      {/* Operational Indicators */}
      <div className="flex items-center space-x-3 text-xs">
        {/* Reloj de Servidor */}
        <div className="hidden md:flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 text-slate-600 font-mono">
          <Clock className="w-3.5 h-3.5 text-slate-400" />
          <span>{time}</span>
        </div>

        {/* Modo Operativo */}
        <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 text-slate-700 font-mono">
          <Layers className="w-3.5 h-3.5 text-slate-400" />
          <span>Modo: <strong className="text-emerald-700 font-semibold">{systemStatus?.mode || 'SIMULACIÓN'}</strong></span>
        </div>

        {/* Enlace en Vivo (WebSocket) */}
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 font-mono">
          <span className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></span>
          <span className={wsConnected ? 'text-slate-700' : 'text-red-600 font-medium'}>
            {wsConnected ? 'Telemetría Activa' : 'Desconectado'}
          </span>
        </div>

        {/* Notificación de Alertas */}
        {alertCount > 0 && (
          <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 font-medium">
            <AlertCircle className="w-3.5 h-3.5 text-amber-600" />
            <span>{alertCount} Alerta{alertCount > 1 ? 's' : ''}</span>
          </div>
        )}
      </div>
    </header>
  );
};
