import React, { useState } from 'react';
import { X, Box, Utensils } from 'lucide-react';
import { Batch } from '../types';

interface BatchManagerModalProps {
  isOpen: boolean;
  onClose: () => void;
  batches: Batch[];
  onCreateBatch: (data: { id: string; zone_id: string; stage: string; initial_quantity: number; substrate_type?: string; notes?: string }) => Promise<void>;
  onAddFeeding: (data: { batch_id: string; food_mass_g: number; food_type: string; notes?: string }) => Promise<void>;
}

export const BatchManagerModal: React.FC<BatchManagerModalProps> = ({
  isOpen,
  onClose,
  batches,
  onCreateBatch,
  onAddFeeding
}) => {
  const [activeTab, setActiveTab] = useState<'create_batch' | 'feed'>('create_batch');

  // Form states
  const [batchId, setBatchId] = useState('');
  const [zoneId, setZoneId] = useState('ZONE-LAR');
  const [stage, setStage] = useState('LARVAE');
  const [initialQty, setInitialQty] = useState('15.0');
  const [substrate, setSubstrate] = useState('Residuos de cocina y subproductos hortícolas');
  const [notes, setNotes] = useState('');

  // Feeding form states
  const [selectedBatchId, setSelectedBatchId] = useState(batches[0]?.id || '');
  const [foodMass, setFoodMass] = useState('2500');
  const [foodType, setFoodType] = useState('Pulpa frutal fermentada y salvado');
  const [feedingNotes, setFeedingNotes] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmitBatch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await onCreateBatch({
        id: batchId,
        zone_id: zoneId,
        stage,
        initial_quantity: parseFloat(initialQty) || 0,
        substrate_type: substrate,
        notes
      });
      setBatchId('');
      onClose();
    } catch (err: any) {
      alert(err.message || 'Error al crear lote');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitFeeding = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedBatchId) return;
    setLoading(true);
    try {
      await onAddFeeding({
        batch_id: selectedBatchId,
        food_mass_g: parseFloat(foodMass) || 0,
        food_type: foodType,
        notes: feedingNotes
      });
      setFoodMass('');
      onClose();
    } catch (err: any) {
      alert(err.message || 'Error al registrar alimentación');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
      <div className="w-full max-w-lg rounded-2xl bg-white border border-slate-200 shadow-xl p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="flex items-center space-x-2 border-b border-slate-100 pb-3 mb-5">
          <button
            onClick={() => setActiveTab('create_batch')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-2 ${
              activeTab === 'create_batch'
                ? 'bg-emerald-50 text-emerald-800 border border-emerald-300 font-semibold'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <Box className="w-3.5 h-3.5 text-emerald-700" /> Registrar Lote
          </button>
          <button
            onClick={() => setActiveTab('feed')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-2 ${
              activeTab === 'feed'
                ? 'bg-amber-50 text-amber-800 border border-amber-300 font-semibold'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <Utensils className="w-3.5 h-3.5 text-amber-700" /> Suministro de Dieta
          </button>
        </div>

        {activeTab === 'create_batch' ? (
          <form onSubmit={handleSubmitBatch} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Identificador del Lote</label>
              <input
                type="text"
                required
                placeholder="BATCH-2026-002"
                value={batchId}
                onChange={(e) => setBatchId(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-emerald-600 focus:bg-white"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Zona Destino</label>
                <select
                  value={zoneId}
                  onChange={(e) => setZoneId(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-emerald-600 focus:bg-white"
                >
                  <option value="ZONE-LAR">ZONE-LAR (Larvas / Biorreactor)</option>
                  <option value="ZONE-INC">ZONE-INC (Incubación de Huevos)</option>
                  <option value="ZONE-REP">ZONE-REP (Reproducción de Adultos)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Masa Inicial (kg)</label>
                <input
                  type="number"
                  step="0.1"
                  required
                  value={initialQty}
                  onChange={(e) => setInitialQty(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-emerald-600 focus:bg-white"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Composición del Sustrato</label>
              <input
                type="text"
                value={substrate}
                onChange={(e) => setSubstrate(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-emerald-600 focus:bg-white"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-xs tracking-wide transition-colors shadow-xs"
            >
              {loading ? 'Guardando...' : 'Registrar Lote de Producción'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleSubmitFeeding} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Lote Destino</label>
              <select
                value={selectedBatchId}
                onChange={(e) => setSelectedBatchId(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-amber-600 focus:bg-white"
              >
                {batches.map((b) => (
                  <option key={b.id} value={b.id}>
                    {b.id} ({b.stage} - {b.zone_id})
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Ración Suministrada (g)</label>
                <input
                  type="number"
                  step="10"
                  required
                  value={foodMass}
                  onChange={(e) => setFoodMass(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-amber-600 focus:bg-white"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Tipo de Dieta</label>
                <input
                  type="text"
                  required
                  value={foodType}
                  onChange={(e) => setFoodType(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-amber-600 focus:bg-white"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white font-medium text-xs tracking-wide transition-colors shadow-xs"
            >
              {loading ? 'Guardando...' : 'Registrar Suministro de Dieta'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};
