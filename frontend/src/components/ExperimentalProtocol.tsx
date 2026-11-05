import React, { useState } from 'react';
import { Calculator, BookOpen, FlaskConical, TrendingUp, CheckCircle2 } from 'lucide-react';
import { Batch } from '../types';

interface ExperimentalProtocolProps {
  batches: Batch[];
  currentSubstrateTemp: number;
}

export const ExperimentalProtocol: React.FC<ExperimentalProtocolProps> = ({
  batches,
  currentSubstrateTemp
}) => {
  // Calculadora interactiva de modelado biológico
  const [initialWaste, setInitialWaste] = useState<number>(50.0); // kg
  const [residualWaste, setResidualWaste] = useState<number>(12.5); // kg
  const [harvestedBiomass, setHarvestedBiomass] = useState<number>(8.2); // kg
  const [dryMatterRatio, setDryMatterRatio] = useState<number>(30); // % materia seca

  // Cálculos bio-agronómicos
  const wasteReduced = Math.max(0, initialWaste - residualWaste);
  const wrePercentage = initialWaste > 0 ? (wasteReduced / initialWaste) * 100 : 0;
  const fcr = harvestedBiomass > 0 ? (initialWaste * (dryMatterRatio / 100)) / harvestedBiomass : 0;

  // Modelo Grados-Día (GDD)
  // T_base para Hermetia illucens = 13.5 °C
  const tBase = 13.5;
  const dailyGDD = Math.max(0, currentSubstrateTemp - tBase);
  const requiredGDD = 220; // GDD acumulados para llegar a prepupa
  const estimatedDaysToHarvest = dailyGDD > 0 ? Math.ceil(requiredGDD / dailyGDD) : 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-xl bg-white border border-slate-200 shadow-xs space-y-2">
        <div className="flex items-center space-x-2 text-xs font-mono text-emerald-700">
          <BookOpen className="w-4 h-4" />
          <span className="uppercase tracking-wider font-semibold">Protocolo Científico & Métricas de Bioconversión</span>
        </div>
        <h2 className="text-xl font-bold text-slate-900">
          Evaluación de Eficiencia Zootécnica & Fisiología Térmica
        </h2>
        <p className="text-xs text-slate-600 leading-relaxed max-w-3xl">
          Ecuaciones zootécnicas estandarizadas para cuantificar la capacidad de 
          <span className="italic font-medium text-slate-800"> Hermetia illucens</span> para valorizar sustratos orgánicos 
          y estimar la ventana de cosecha mediante acumulación térmica de Grados-Día (GDD).
        </p>
      </div>

      {/* Main Equations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* ECUACIÓN 1: WRE */}
        <div className="p-5 rounded-xl bg-white border border-slate-200 shadow-xs space-y-3 flex flex-col justify-between">
          <div>
            <div className="text-[10px] font-mono text-emerald-700 uppercase tracking-wider font-bold">
              Métrica 1 • Reducción de Residuos
            </div>
            <h3 className="text-sm font-bold text-slate-900 mt-1">Eficiencia de Reducción (WRE)</h3>
            
            {/* Mathematical Formula Box */}
            <div className="my-3 p-3 rounded-lg bg-slate-50 border border-slate-200 font-mono text-xs text-center text-slate-800">
              <span className="text-emerald-700 font-bold">WRE (%)</span> = [ (W₀ - W₁) / W₀ ] × 100
            </div>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              Donde <span className="font-mono text-slate-700 font-medium">W₀</span> es la masa de residuo suministrado y <span className="font-mono text-slate-700 font-medium">W₁</span> el compost o frass remanente.
            </p>
          </div>

          <div className="p-3.5 rounded-lg bg-emerald-50/70 border border-emerald-200 flex items-baseline justify-between font-mono">
            <span className="text-xs text-emerald-800 font-sans font-medium">Eficiencia actual:</span>
            <span className="text-2xl font-bold text-emerald-800">{wrePercentage.toFixed(1)}%</span>
          </div>
        </div>

        {/* ECUACIÓN 2: FCR */}
        <div className="p-5 rounded-xl bg-white border border-slate-200 shadow-xs space-y-3 flex flex-col justify-between">
          <div>
            <div className="text-[10px] font-mono text-amber-700 uppercase tracking-wider font-bold">
              Métrica 2 • Conversión Alimenticia
            </div>
            <h3 className="text-sm font-bold text-slate-900 mt-1">Tasa de Conversión (FCR)</h3>

            <div className="my-3 p-3 rounded-lg bg-slate-50 border border-slate-200 font-mono text-xs text-center text-slate-800">
              <span className="text-amber-700 font-bold">FCR</span> = Alimento Seco (kg) / Biomasa Larvaria (kg)
            </div>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              Cantidad de materia seca consumida por kilogramo de larva viva producida. Valores menores a 2.0 denotan excelente asimilación.
            </p>
          </div>

          <div className="p-3.5 rounded-lg bg-amber-50/70 border border-amber-200 flex items-baseline justify-between font-mono">
            <span className="text-xs text-amber-800 font-sans font-medium">Ratio FCR:</span>
            <span className="text-2xl font-bold text-amber-800">{fcr.toFixed(2)} : 1</span>
          </div>
        </div>

        {/* ECUACIÓN 3: GRADOS DÍA (GDD) */}
        <div className="p-5 rounded-xl bg-white border border-slate-200 shadow-xs space-y-3 flex flex-col justify-between">
          <div>
            <div className="text-[10px] font-mono text-sky-700 uppercase tracking-wider font-bold">
              Métrica 3 • Fisiología Térmica
            </div>
            <h3 className="text-sm font-bold text-slate-900 mt-1">Modelo Grados-Día (GDD)</h3>

            <div className="my-3 p-3 rounded-lg bg-slate-50 border border-slate-200 font-mono text-xs text-center text-slate-800">
              <span className="text-sky-700 font-bold">GDD diario</span> = T_sustrato - 13.5 °C
            </div>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              Suma térmica fisiológica para completar el ciclo larvario. Con sustrato a {currentSubstrateTemp.toFixed(1)} °C se acumulan {dailyGDD.toFixed(1)} GDD/día.
            </p>
          </div>

          <div className="p-3.5 rounded-lg bg-sky-50/70 border border-sky-200 flex items-baseline justify-between font-mono">
            <span className="text-xs text-sky-800 font-sans font-medium">Tiempo a Cosecha:</span>
            <span className="text-2xl font-bold text-sky-800">~{estimatedDaysToHarvest} días</span>
          </div>
        </div>
      </div>

      {/* Interactive Assay Calculator Workbench */}
      <div className="p-6 rounded-xl bg-white border border-slate-200 shadow-xs space-y-5">
        <div className="flex items-center space-x-2 border-b border-slate-100 pb-3">
          <Calculator className="w-4 h-4 text-emerald-700" />
          <h3 className="text-sm font-bold text-slate-900">
            Calculadora Experimental de Dietas & Digestibilidad
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              Alimento Suministrado (kg)
            </label>
            <input
              type="number"
              step="0.5"
              value={initialWaste}
              onChange={(e) => setInitialWaste(parseFloat(e.target.value) || 0)}
              className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-emerald-600 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              Frass Remanente (kg)
            </label>
            <input
              type="number"
              step="0.5"
              value={residualWaste}
              onChange={(e) => setResidualWaste(parseFloat(e.target.value) || 0)}
              className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-emerald-600 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              Larva Viva Cosechada (kg)
            </label>
            <input
              type="number"
              step="0.1"
              value={harvestedBiomass}
              onChange={(e) => setHarvestedBiomass(parseFloat(e.target.value) || 0)}
              className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-emerald-600 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">
              Materia Seca Dieta (%)
            </label>
            <input
              type="number"
              step="1"
              value={dryMatterRatio}
              onChange={(e) => setDryMatterRatio(parseFloat(e.target.value) || 0)}
              className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-emerald-600 focus:bg-white"
            />
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-mono">
          <div>
            <span className="text-slate-500 font-sans">Masa Degradada Neta:</span>
            <div className="text-base font-bold text-slate-900 mt-0.5">{wasteReduced.toFixed(1)} kg</div>
          </div>
          <div>
            <span className="text-slate-500 font-sans">Tasa de Reducción:</span>
            <div className="text-base font-bold text-emerald-700 mt-0.5">{wrePercentage.toFixed(1)}%</div>
          </div>
          <div>
            <span className="text-slate-500 font-sans">Proteína Cruda Estimada:</span>
            <div className="text-base font-bold text-amber-700 mt-0.5">
              ~{(harvestedBiomass * 0.42).toFixed(1)} kg (42% BS)
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
