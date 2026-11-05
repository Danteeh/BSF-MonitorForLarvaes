import React, { useState } from 'react';
import { 
  Thermometer, 
  Droplets, 
  Sun, 
  Scale, 
  Eye, 
  Layers, 
  Flame,
  CheckCircle2,
  Clock,
  Sparkles
} from 'lucide-react';
import { SensorReading, Zone, Batch } from '../types';

interface BioreactorDigitalTwinProps {
  zones: Zone[];
  readings: Record<string, SensorReading>;
  activeBatch?: Batch;
  onSelectChamber?: (chamberId: string) => void;
  onOpenPhotoViewer?: () => void;
}

export const BioreactorDigitalTwin: React.FC<BioreactorDigitalTwinProps> = ({
  zones,
  readings,
  activeBatch,
  onSelectChamber,
  onOpenPhotoViewer
}) => {
  const [selectedChamber, setSelectedChamber] = useState<'rep' | 'inc' | 'lar'>('lar');
  const [activeDepth, setActiveDepth] = useState<'surface' | 'core' | 'bottom'>('core');

  // Valores de telemetría en tiempo real
  const repTemp = readings['REP-TEMP-001']?.value ?? 27.5;
  const repHum = readings['REP-HUM-001']?.value ?? 65.0;
  const repLux = readings['REP-LUX-001']?.value ?? 12500;

  const incTemp = readings['INC-TEMP-001']?.value ?? 29.0;
  const incHum = readings['INC-HUM-001']?.value ?? 76.0;

  const larTemp = readings['LAR-TEMP-001']?.value ?? 34.2;
  const larHum = readings['LAR-HUM-001']?.value ?? 68.0;
  const larWeight = readings['LAR-WEIGHT-001']?.value ?? 16.4;

  // Gradiente térmico estimado según profundidad del lecho
  const depthTemps = {
    surface: Math.round((larTemp - 3.8) * 10) / 10,
    core: larTemp,
    bottom: Math.round((larTemp - 1.5) * 10) / 10
  };

  return (
    <div className="rounded-xl bg-white border border-slate-200 shadow-xs p-6 space-y-6">
      {/* Header del Digital Twin */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3 border-b border-slate-100 pb-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-[10px] font-mono font-bold tracking-wider text-emerald-800 bg-emerald-50 px-2.5 py-0.5 rounded border border-emerald-200 uppercase">
              Modelo Digital del Biorreactor
            </span>
            <span className="text-xs text-slate-500 font-sans">
              Esquema físico-espacial de los módulos de cría
            </span>
          </div>
          <h2 className="text-lg font-bold text-slate-900 mt-1">
            Topología del Biorreactor & Gradiente de Parámetros
          </h2>
        </div>

        {/* Chamber Selector Tabs */}
        <div className="flex items-center space-x-1.5 p-1 rounded-xl bg-slate-100 border border-slate-200 self-start lg:self-auto">
          <button
            onClick={() => { setSelectedChamber('rep'); onSelectChamber?.('ZONE-REP'); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
              selectedChamber === 'rep'
                ? 'bg-white text-emerald-800 font-semibold shadow-xs border border-slate-200'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Sun className="w-3.5 h-3.5 text-amber-500" />
            <span>1. Jaula Adultos (REP)</span>
          </button>

          <button
            onClick={() => { setSelectedChamber('inc'); onSelectChamber?.('ZONE-INC'); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
              selectedChamber === 'inc'
                ? 'bg-white text-emerald-800 font-semibold shadow-xs border border-slate-200'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Droplets className="w-3.5 h-3.5 text-sky-500" />
            <span>2. Incubadora (INC)</span>
          </button>

          <button
            onClick={() => { setSelectedChamber('lar'); onSelectChamber?.('ZONE-LAR'); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 ${
              selectedChamber === 'lar'
                ? 'bg-white text-emerald-800 font-semibold shadow-xs border border-slate-200'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Layers className="w-3.5 h-3.5 text-emerald-600" />
            <span>3. Biorreactor Larvario (LAR)</span>
          </button>
        </div>
      </div>

      {/* Main Interactive Digital Twin Visualizer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        {/* Left Side: Technical Schematic Graphic (8 Cols) */}
        <div className="lg:col-span-8 rounded-xl bg-slate-50 border border-slate-200 p-5 relative flex flex-col justify-between overflow-hidden">
          
          {/* VIEW 1: REPRODUCTION FLIGHT CAGE */}
          {selectedChamber === 'rep' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                <span className="text-xs font-semibold text-slate-800">
                  CÁMARA DE REPRODUCCIÓN • FOTOPERIODO Y OVIPOSICIÓN
                </span>
                <span className="text-[11px] font-mono text-slate-500 bg-white px-2 py-0.5 rounded border border-slate-200">
                  Malla entomológica 1.0 mm
                </span>
              </div>

              {/* Schematic Illustration */}
              <div className="h-64 border border-slate-200 rounded-xl bg-white p-4 flex flex-col justify-between shadow-xs">
                {/* Lámpara UV / Espectro Solar */}
                <div className="flex items-center justify-between p-2.5 rounded-lg bg-amber-50/60 border border-amber-200">
                  <div className="flex items-center space-x-2">
                    <Sun className="w-4 h-4 text-amber-600" />
                    <span className="text-xs font-medium text-slate-800">Iluminación Solar Inductora de Cópula</span>
                  </div>
                  <span className="text-xs font-mono font-bold text-amber-700">{repLux.toLocaleString()} lux</span>
                </div>

                {/* Zona de Vuelo y Apareamiento */}
                <div className="my-auto text-center space-y-1">
                  <div className="text-xs font-semibold text-slate-800">
                    Zona de Vuelo Libre de Imagos (<span className="italic">Hermetia illucens</span>)
                  </div>
                  <div className="text-[11px] text-slate-500 max-w-sm mx-auto">
                    Los adultos no consumen alimento sólido; requieren nebulización fina de agua potable y fotoperiodo controlado (12h luz / 12h penumbra).
                  </div>
                </div>

                {/* Tablillas de Oviposición */}
                <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
                  <div className="text-xs text-slate-700 flex items-center gap-2">
                    <Layers className="w-3.5 h-3.5 text-amber-600" />
                    <span>Bloques de Tablillas Alveoladas (Atrayente de Olor)</span>
                  </div>
                  <span className="text-[10px] font-mono font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    Oviposición Activa
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* VIEW 2: INCUBATION NEST */}
          {selectedChamber === 'inc' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                <span className="text-xs font-semibold text-slate-800">
                  CÁMARA DE INCUBACIÓN & ECLOSIÓN DE NEONATOS
                </span>
                <span className="text-[11px] font-mono text-slate-500 bg-white px-2 py-0.5 rounded border border-slate-200">
                  Ambiente Saturado Hermético
                </span>
              </div>

              <div className="h-64 border border-slate-200 rounded-xl bg-white p-4 flex flex-col justify-between shadow-xs">
                {/* Microclima Humedad */}
                <div className="p-2.5 rounded-lg bg-sky-50/70 border border-sky-200 flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Droplets className="w-4 h-4 text-sky-600" />
                    <span className="text-xs font-medium text-slate-800">Cúpula de Humedad Relativa</span>
                  </div>
                  <span className="text-xs font-mono font-bold text-sky-700">{incHum.toFixed(1)}% HR</span>
                </div>

                {/* Nido de Huevos */}
                <div className="my-auto p-4 rounded-xl bg-slate-50 border border-dashed border-slate-300 text-center space-y-1.5">
                  <div className="text-xs font-semibold text-slate-800">
                    Soporte Suspendido de Posturas
                  </div>
                  <p className="text-[11px] text-slate-500 max-w-sm mx-auto">
                    Los huevos se sitúan 3 cm por encima de la dieta húmeda para evitar asfixia hídrica y permitir que las larvas neonatas caigan por gravedad al eclosionar.
                  </p>
                  <div className="text-[10px] font-mono text-emerald-700 font-medium">
                    Tiempo de eclosión restante estimado: ~36 horas
                  </div>
                </div>

                {/* Bandeja de Iniciación */}
                <div className="p-2 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between text-xs font-mono text-slate-600">
                  <span>Temperatura de Incubación:</span>
                  <span className="font-bold text-slate-800">{incTemp.toFixed(1)} °C</span>
                </div>
              </div>
            </div>
          )}

          {/* VIEW 3: LARVAL BIOREACTOR CROSS-SECTION (DEFAULT) */}
          {selectedChamber === 'lar' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                <span className="text-xs font-semibold text-slate-800 flex items-center gap-1.5">
                  <Layers className="w-4 h-4 text-emerald-600" />
                  CORTE TRANSVERSAL DEL LECHO DE CRÍA (ZONE-LAR)
                </span>
                <span className="text-[11px] font-mono text-slate-500 bg-white px-2 py-0.5 rounded border border-slate-200">
                  Profundidad Total: 15 cm
                </span>
              </div>

              {/* Reactor Cutaway Drawing */}
              <div className="border border-slate-200 rounded-xl bg-white p-4 space-y-2.5 shadow-xs">
                {/* 1. Capa Superior / Superficie */}
                <div 
                  onClick={() => setActiveDepth('surface')}
                  className={`p-3 rounded-lg border cursor-pointer transition-all ${
                    activeDepth === 'surface'
                      ? 'bg-emerald-50/60 border-emerald-400 ring-1 ring-emerald-300'
                      : 'bg-slate-50/60 border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-800 flex items-center gap-2">
                      <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                      Estrato 0 - 3 cm: Superficie Aerobia & Alimento Fresco
                    </span>
                    <span className="font-bold font-mono text-emerald-800">{depthTemps.surface} °C</span>
                  </div>
                  <p className="text-[11px] text-slate-500 mt-1 pl-4.5">
                    Zona de oxigenación pasiva y consumo de alimento recién dosificado.
                  </p>
                </div>

                {/* 2. Núcleo Metabólico (Core) */}
                <div 
                  onClick={() => setActiveDepth('core')}
                  className={`p-3 rounded-lg border cursor-pointer transition-all ${
                    activeDepth === 'core'
                      ? 'bg-amber-50/70 border-amber-400 ring-1 ring-amber-300'
                      : 'bg-slate-50/60 border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-800 flex items-center gap-2">
                      <Flame className="w-3.5 h-3.5 text-amber-600" />
                      Estrato 3 - 10 cm: Núcleo Termogénico Larvario (Sensor LAR-TEMP-001)
                    </span>
                    <span className="font-bold font-mono text-amber-800 text-sm">{depthTemps.core} °C</span>
                  </div>
                  <p className="text-[11px] text-slate-600 mt-1 pl-5.5">
                    Máxima densidad de biomasa (Instar L5). Fermentación acelerada y calor de fricción biológica.
                  </p>
                </div>

                {/* 3. Fondo Drenante */}
                <div 
                  onClick={() => setActiveDepth('bottom')}
                  className={`p-3 rounded-lg border cursor-pointer transition-all ${
                    activeDepth === 'bottom'
                      ? 'bg-sky-50/70 border-sky-400 ring-1 ring-sky-300'
                      : 'bg-slate-50/60 border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-800 flex items-center gap-2">
                      <Droplets className="w-3.5 h-3.5 text-sky-600" />
                      Estrato 10 - 15 cm: Base Drenante de Lixiviados
                    </span>
                    <span className="font-bold font-mono text-sky-800">{depthTemps.bottom} °C</span>
                  </div>
                  <p className="text-[11px] text-slate-500 mt-1 pl-5.5">
                    Malla perforada de acero inox. Evacuación de condensados y flujo de aire inferior.
                  </p>
                </div>

                {/* Substrate Base Load Cell Scale */}
                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs font-mono text-slate-600">
                  <div className="flex items-center gap-2">
                    <Scale className="w-4 h-4 text-slate-400" />
                    <span>Plataforma de Carga (Peso Neto del Lecho):</span>
                  </div>
                  <span className="text-sm font-bold text-slate-900">{larWeight.toFixed(2)} kg</span>
                </div>
              </div>
            </div>
          )}

          {/* Bottom Toolbar */}
          <div className="mt-4 pt-3 border-t border-slate-200 flex items-center justify-between text-xs">
            <span className="text-slate-500 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              Sondas Térmicas 1-Wire & I2C Operativas
            </span>
            <button
              onClick={onOpenPhotoViewer}
              className="px-3 py-1.5 rounded-lg bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 shadow-2xs flex items-center gap-1.5 font-medium transition-colors"
            >
              <Eye className="w-3.5 h-3.5 text-emerald-600" />
              <span>Inspección de Muestra</span>
            </button>
          </div>
        </div>

        {/* Right Side: Bioprocess Diagnostics Card (4 Cols) */}
        <div className="lg:col-span-4 rounded-xl bg-slate-50 border border-slate-200 p-5 flex flex-col justify-between space-y-4">
          <div>
            <div className="text-xs font-semibold text-slate-700 uppercase tracking-wider border-b border-slate-200 pb-2 mb-3">
              Diagnóstico Zootécnico
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-3.5 rounded-lg bg-white border border-slate-200 shadow-2xs">
                <div className="text-[11px] font-medium text-slate-500">Condición Actual</div>
                <div className="text-sm font-bold text-slate-900 mt-0.5">
                  {selectedChamber === 'lar' ? 'Bioconversión Óptima' : selectedChamber === 'inc' ? 'Incubación Estable' : 'Fotoperiodo Óptimo'}
                </div>
                <div className="text-[11px] text-slate-600 mt-1 leading-relaxed">
                  {selectedChamber === 'lar' 
                    ? `El núcleo a ${larTemp} °C confirma digestión enzimática acelerada sin rebasar el umbral de estrés térmico.`
                    : selectedChamber === 'inc'
                    ? `Humedad de ${incHum}% previene deshidratación y colapso de las cubiertas coriónicas.`
                    : `Intensidad lumínica de ${repLux.toLocaleString()} lux estimula el cortejo sexual.`}
                </div>
              </div>

              <div className="p-3.5 rounded-lg bg-white border border-slate-200 shadow-2xs space-y-2 font-mono text-[11px]">
                <div className="text-slate-500 uppercase text-[10px] font-sans font-semibold">Parámetros Clave</div>
                <div className="flex justify-between">
                  <span className="text-slate-600">ΔT Fermentativo:</span>
                  <span className="font-bold text-amber-700">+{Math.max(0, larTemp - 24.5).toFixed(1)} °C</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600">Humedad Sustrato:</span>
                  <span className="font-bold text-sky-700">{larHum.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-600">Densidad Estimada:</span>
                  <span className="font-bold text-emerald-700">3.8 larvas / cm³</span>
                </div>
              </div>
            </div>
          </div>

          <div className="p-3.5 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-900 leading-relaxed">
            <span className="font-bold text-emerald-800">Recomendación:</span> Mantener ventilación pasiva continua. Próxima ración de sustrato programada en 14 horas.
          </div>
        </div>
      </div>
    </div>
  );
};
