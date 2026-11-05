import React from 'react';
import { Check, Clock, ArrowRight } from 'lucide-react';

interface StageInfo {
  id: string;
  name: string;
  scientificStage: string;
  zone: string;
  duration: string;
  conditions: string;
  status: 'completed' | 'active' | 'upcoming';
}

export const LifeCycleWidget: React.FC = () => {
  const stages: StageInfo[] = [
    {
      id: 'rep',
      name: 'Adultos & Cópula',
      scientificStage: 'Imago reproductor',
      zone: 'ZONE-REP',
      duration: '5 - 8 días',
      conditions: '27.5 °C • 12.000 lux',
      status: 'completed'
    },
    {
      id: 'inc',
      name: 'Incubación de Huevos',
      scientificStage: 'Posturas coriónicas',
      zone: 'ZONE-INC',
      duration: '3 - 4 días',
      conditions: '29.0 °C • >70% HR',
      status: 'completed'
    },
    {
      id: 'lar',
      name: 'Bioconversión Larvaria',
      scientificStage: 'Instar L4 - L5',
      zone: 'ZONE-LAR',
      duration: '12 - 16 días',
      conditions: '33.5 °C en sustrato',
      status: 'active'
    },
    {
      id: 'pre',
      name: 'Prepupa & Cosecha',
      scientificStage: 'Cutícula melánica',
      zone: 'ZONE-LAR',
      duration: '5 - 7 días',
      conditions: 'Migración activa',
      status: 'upcoming'
    }
  ];

  return (
    <div className="p-5 rounded-xl bg-white border border-slate-200 shadow-xs space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-sm font-bold text-slate-900">
            Fases Ontogénicas de la Mosca Soldado Negra
          </h3>
          <p className="text-xs text-slate-500">
            Ciclo de desarrollo biológico en bioreactor (<span className="italic">Hermetia illucens</span>)
          </p>
        </div>
        <span className="text-[11px] font-mono font-medium text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded border border-emerald-200 self-start">
          Etapa Actual: Instar L5 (Alimentación Voraz)
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 pt-1">
        {stages.map((st) => {
          const isActive = st.status === 'active';
          const isDone = st.status === 'completed';

          return (
            <div
              key={st.id}
              className={`p-4 rounded-xl border transition-all ${
                isActive
                  ? 'bg-emerald-50/60 border-emerald-300 ring-1 ring-emerald-200 shadow-xs'
                  : isDone
                  ? 'bg-slate-50/70 border-slate-200'
                  : 'bg-white border-slate-200/80 opacity-60'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono font-semibold text-slate-500 uppercase">
                  {st.zone}
                </span>
                {isDone ? (
                  <span className="flex items-center gap-1 text-[10px] font-mono font-medium text-emerald-700 bg-emerald-100/80 px-1.5 py-0.5 rounded">
                    <Check className="w-3 h-3 text-emerald-700" />
                    Completado
                  </span>
                ) : isActive ? (
                  <span className="flex items-center gap-1 text-[10px] font-mono font-bold text-emerald-800 bg-emerald-200/70 px-1.5 py-0.5 rounded animate-pulse">
                    En Curso
                  </span>
                ) : (
                  <span className="flex items-center gap-1 text-[10px] font-mono text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded">
                    <Clock className="w-3 h-3 text-slate-400" />
                    Siguiente
                  </span>
                )}
              </div>

              <h4 className="text-xs font-bold text-slate-900">{st.name}</h4>
              <p className="text-[11px] text-slate-500 italic mt-0.5">{st.scientificStage}</p>

              <div className="mt-3 pt-2.5 border-t border-slate-200/60 text-[11px] font-mono space-y-1 text-slate-600">
                <div className="flex justify-between">
                  <span className="text-slate-400">Duración:</span>
                  <span className="font-semibold text-slate-700">{st.duration}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Objetivo:</span>
                  <span className="text-slate-700 text-right">{st.conditions}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
