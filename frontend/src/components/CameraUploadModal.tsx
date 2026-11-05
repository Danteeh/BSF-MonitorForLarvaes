import React, { useState } from 'react';
import { Camera, Upload, X, Image as ImageIcon } from 'lucide-react';
import { MediaFile, Batch } from '../types';

interface CameraUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  mediaFiles: MediaFile[];
  batches: Batch[];
  onUploadImage: (file: File, zoneId: string, batchId?: string) => Promise<void>;
}

export const CameraUploadModal: React.FC<CameraUploadModalProps> = ({
  isOpen,
  onClose,
  mediaFiles,
  batches,
  onUploadImage
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [zoneId, setZoneId] = useState('ZONE-LAR');
  const [batchId, setBatchId] = useState(batches[0]?.id || '');
  const [uploading, setUploading] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;
    setUploading(true);
    try {
      await onUploadImage(selectedFile, zoneId, batchId || undefined);
      setSelectedFile(null);
      setPreviewUrl(null);
    } catch (err: any) {
      alert(err.message || 'Error al subir imagen');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
      <div className="w-full max-w-2xl rounded-2xl bg-white border border-slate-200 shadow-xl p-6 relative max-h-[90vh] flex flex-col">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        <div className="flex items-center space-x-3 border-b border-slate-100 pb-3 mb-4">
          <div className="p-2 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-700">
            <Camera className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">
              Registro Fotográfico del Cultivo
            </h3>
            <p className="text-xs text-slate-500">
              Carga y catálogo visual de muestras biológicas reales
            </p>
          </div>
        </div>

        {/* Upload Form */}
        <form onSubmit={handleUpload} className="space-y-3.5 mb-5">
          <div className="border border-dashed border-slate-300 hover:border-emerald-500 rounded-xl p-5 text-center transition-colors bg-slate-50">
            {previewUrl ? (
              <div className="space-y-2">
                <img
                  src={previewUrl}
                  alt="Vista previa"
                  className="max-h-44 mx-auto rounded-lg border border-slate-200 object-cover shadow-xs"
                />
                <p className="text-xs font-mono text-emerald-700">
                  {selectedFile?.name} ({(selectedFile!.size / 1024).toFixed(1)} KB)
                </p>
              </div>
            ) : (
              <label className="cursor-pointer flex flex-col items-center space-y-1.5 py-2">
                <Upload className="w-8 h-8 text-slate-400" />
                <span className="text-xs font-semibold text-slate-700">
                  Selecciona una fotografía de muestra del lecho
                </span>
                <span className="text-[11px] text-slate-500 font-mono">
                  Formatos soportados: JPG, PNG, WEBP (hasta 10 MB)
                </span>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </label>
            )}
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Zona / Módulo</label>
              <select
                value={zoneId}
                onChange={(e) => setZoneId(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-emerald-600 focus:bg-white"
              >
                <option value="ZONE-LAR">ZONE-LAR (Biorreactor Larvario)</option>
                <option value="ZONE-INC">ZONE-INC (Incubadora de Huevos)</option>
                <option value="ZONE-REP">ZONE-REP (Jaula de Adultos)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Lote Asociado</label>
              <select
                value={batchId}
                onChange={(e) => setBatchId(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 font-mono text-xs focus:outline-none focus:border-emerald-600 focus:bg-white"
              >
                <option value="">Sin lote específico</option>
                {batches.map((b) => (
                  <option key={b.id} value={b.id}>
                    {b.id} ({b.stage})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={!selectedFile || uploading}
            className="w-full py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-medium text-xs tracking-wide transition-colors shadow-xs"
          >
            {uploading ? 'Subiendo fotografía...' : 'Subir e Indexar Fotografía'}
          </button>
        </form>

        {/* Existing photos preview list */}
        <div className="flex-1 overflow-y-auto border-t border-slate-100 pt-3">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-700">
              Fotografías en Catálogo ({mediaFiles.length})
            </span>
          </div>

          {mediaFiles.length === 0 ? (
            <div className="py-6 text-center text-xs text-slate-400 font-mono">
              Aún no se han indexado fotografías. Sube la primera muestra fotográfica arriba.
            </div>
          ) : (
            <div className="grid grid-cols-4 gap-2.5">
              {mediaFiles.map((m) => (
                <div key={m.id} className="relative group rounded-lg overflow-hidden border border-slate-200 bg-slate-50 aspect-video shadow-xs">
                  <img
                    src={`/api/v1/media/${m.id}/file`}
                    alt={m.filename}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-slate-900/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-1.5 text-white">
                    <span className="text-[10px] font-mono truncate">{m.filename}</span>
                    <span className="text-[9px] font-mono text-slate-300">{m.zone_id}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
