import React, { useState } from 'react';
import { Camera, ZoomIn, ZoomOut, Grid, Eye, Bug } from 'lucide-react';
import { MediaFile } from '../types';

interface MacroInspectionViewerProps {
  mediaFiles: MediaFile[];
  onUploadClick: () => void;
}

export const MacroInspectionViewer: React.FC<MacroInspectionViewerProps> = ({
  mediaFiles,
  onUploadClick
}) => {
  const [selectedPhoto, setSelectedPhoto] = useState<MediaFile | null>(mediaFiles[0] || null);
  const [showGrid, setShowGrid] = useState<boolean>(true);
  const [zoomLevel, setZoomLevel] = useState<number>(100);
  const [selectedInstar, setSelectedInstar] = useState<string>('L5');

  const instars = [
    { id: 'L1', name: 'Neonato (L1)', length: '1 - 2 mm', description: 'Blanco traslúcido, recién eclosionado.' },
    { id: 'L2', name: 'Instar L2', length: '3 - 5 mm', description: 'Aparato bucal incipiente, alimentación superficial.' },
    { id: 'L3', name: 'Instar L3', length: '6 - 10 mm', description: 'Migración activa en el lecho orgánico.' },
    { id: 'L4', name: 'Instar L4', length: '11 - 18 mm', description: 'Ingesta acelerada, cápsula cefálica visible.' },
    { id: 'L5', name: 'Instar L5', length: '19 - 25 mm', description: 'Máxima acumulación de lípidos y proteína.' },
    { id: 'Pre', name: 'Prepupa', length: '20 - 24 mm', description: 'Cutícula melánica marrón oscura, no se alimenta.' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-xl bg-white border border-slate-200 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-mono text-emerald-700">
            <Eye className="w-4 h-4" />
            <span className="uppercase tracking-wider font-semibold">Morfometría & Fenotipado Óptico</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 mt-1">
            Estación de Inspección Macroscópica de Muestras
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Registro fotográfico real de colonias larvarias con retícula milimétrica de calibración.
          </p>
        </div>

        <button
          onClick={onUploadClick}
          className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-xs flex items-center gap-2 self-start sm:self-auto transition-colors shadow-xs"
        >
          <Camera className="w-4 h-4" />
          <span>Subir Fotografía Real</span>
        </button>
      </div>

      {/* Main Optical Workbench */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Side: Optical Viewport (8 Cols) */}
        <div className="lg:col-span-8 rounded-xl bg-white border border-slate-200 shadow-xs p-5 space-y-3 flex flex-col justify-between">
          {/* Controls Bar */}
          <div className="flex items-center justify-between border-b border-slate-100 pb-3 text-xs font-mono">
            <div className="flex items-center space-x-2">
              <span className="text-slate-500 font-sans">Muestra:</span>
              <span className="text-slate-900 font-medium truncate max-w-[220px]">
                {selectedPhoto ? selectedPhoto.filename : 'Sin archivo seleccionado'}
              </span>
            </div>

            <div className="flex items-center space-x-2">
              <button
                onClick={() => setShowGrid(!showGrid)}
                className={`px-2.5 py-1 rounded-md text-xs font-sans transition-colors flex items-center gap-1.5 ${
                  showGrid 
                    ? 'bg-emerald-50 border border-emerald-300 text-emerald-800 font-medium' 
                    : 'bg-slate-100 border border-slate-200 text-slate-600 hover:bg-slate-200'
                }`}
              >
                <Grid className="w-3.5 h-3.5" />
                <span>Retícula (5mm)</span>
              </button>

              <button
                onClick={() => setZoomLevel((z) => Math.max(50, z - 25))}
                className="p-1.5 rounded-md bg-slate-100 border border-slate-200 text-slate-600 hover:bg-slate-200"
              >
                <ZoomOut className="w-3.5 h-3.5" />
              </button>
              <span className="text-[11px] px-1 font-semibold text-slate-700">{zoomLevel}%</span>
              <button
                onClick={() => setZoomLevel((z) => Math.min(250, z + 25))}
                className="p-1.5 rounded-md bg-slate-100 border border-slate-200 text-slate-600 hover:bg-slate-200"
              >
                <ZoomIn className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Viewport Display */}
          <div className="h-96 rounded-xl bg-slate-900 border border-slate-300 relative overflow-hidden flex items-center justify-center">
            {selectedPhoto ? (
              <div 
                className="relative transition-transform duration-200"
                style={{ transform: `scale(${zoomLevel / 100})` }}
              >
                <img
                  src={`/api/v1/media/${selectedPhoto.id}/file`}
                  alt={selectedPhoto.filename}
                  className="max-h-80 max-w-full rounded object-contain mx-auto"
                />

                {/* Millimetric Overlay Grid */}
                {showGrid && (
                  <div className="absolute inset-0 bg-[linear-gradient(to_right,#ffffff20_1px,transparent_1px),linear-gradient(to_bottom,#ffffff20_1px,transparent_1px)] bg-[size:25px_25px] pointer-events-none border border-emerald-400/50">
                    <span className="absolute bottom-2 right-2 text-[9px] font-mono text-emerald-300 bg-slate-950/80 px-2 py-0.5 rounded border border-emerald-500/40">
                      Escala de cuadrícula: 5.0 mm
                    </span>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center space-y-2 text-slate-400 font-mono text-xs">
                <Bug className="w-8 h-8 mx-auto text-slate-500 opacity-60" />
                <p>No hay fotografías seleccionadas.</p>
                <p className="text-[11px] text-slate-500">Sube una fotografía real o elige del catálogo lateral.</p>
              </div>
            )}
          </div>

          {/* Scale Legend Footnote */}
          <div className="pt-2 flex items-center justify-between text-xs text-slate-500">
            <span>Módulo: <strong className="text-slate-700 font-mono">{selectedPhoto?.zone_id || 'ZONE-LAR'}</strong></span>
            <span>Fecha de Toma: <span className="text-slate-700 font-mono">{selectedPhoto ? new Date(selectedPhoto.captured_at).toLocaleString('es-ES') : '--'}</span></span>
          </div>
        </div>

        {/* Right Side: Larval Ontogeny Guide (4 Cols) */}
        <div className="lg:col-span-4 rounded-xl bg-white border border-slate-200 shadow-xs p-5 space-y-4 flex flex-col justify-between">
          <div>
            <div className="text-xs font-semibold text-slate-800 uppercase tracking-wider border-b border-slate-100 pb-2 mb-3">
              Guía de Clasificación de Estadios
            </div>

            <div className="space-y-2 text-xs">
              {instars.map((ins) => (
                <div
                  key={ins.id}
                  onClick={() => setSelectedInstar(ins.id)}
                  className={`p-2.5 rounded-lg border cursor-pointer transition-all ${
                    selectedInstar === ins.id
                      ? 'bg-emerald-50/70 border-emerald-300 ring-1 ring-emerald-200'
                      : 'bg-slate-50 border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-900">{ins.name}</span>
                    <span className="text-[11px] font-mono font-medium text-emerald-800">{ins.length}</span>
                  </div>
                  <p className="text-[11px] text-slate-500 mt-1 leading-snug">
                    {ins.description}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Photo strip selector */}
          <div className="pt-3 border-t border-slate-100">
            <span className="text-xs font-semibold text-slate-600 block mb-2">
              Galería de Muestras ({mediaFiles.length})
            </span>
            <div className="flex space-x-2 overflow-x-auto pb-1">
              {mediaFiles.map((m) => (
                <button
                  key={m.id}
                  onClick={() => setSelectedPhoto(m)}
                  className={`w-14 h-14 rounded-lg overflow-hidden shrink-0 border transition-all ${
                    selectedPhoto?.id === m.id ? 'border-emerald-600 ring-2 ring-emerald-300' : 'border-slate-200 opacity-70 hover:opacity-100'
                  }`}
                >
                  <img
                    src={`/api/v1/media/${m.id}/file`}
                    alt={m.filename}
                    className="w-full h-full object-cover"
                  />
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
