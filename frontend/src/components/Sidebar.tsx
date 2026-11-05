import React from 'react';
import { 
  LayoutDashboard, 
  Layers, 
  BookOpen, 
  Microscope, 
  ClipboardList, 
  LineChart, 
  SlidersHorizontal,
  Info
} from 'lucide-react';

export type NavTab = 'overview' | 'zones' | 'protocol' | 'macro' | 'batches' | 'telemetry' | 'simulator';

interface SidebarProps {
  currentTab: NavTab;
  onTabChange: (tab: NavTab) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentTab, onTabChange }) => {
  const menuItems = [
    { id: 'overview', label: 'Biorreactor Central', icon: LayoutDashboard },
    { id: 'zones', label: 'Zonas del Proceso', icon: Layers },
    { id: 'protocol', label: 'Protocolo & Ecuaciones', icon: BookOpen },
    { id: 'macro', label: 'Inspección & Fotografías', icon: Microscope },
    { id: 'batches', label: 'Lotes y Nutrición', icon: ClipboardList },
    { id: 'telemetry', label: 'Telemetría & Gráficas', icon: LineChart },
    { id: 'simulator', label: 'Control HAL & Fallas', icon: SlidersHorizontal, badge: 'HAL' },
  ];

  return (
    <aside className="w-64 border-r border-slate-200 bg-white flex flex-col justify-between p-4 shrink-0">
      <div className="space-y-6">
        <div>
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 px-3">
            Módulos del Sistema
          </span>
          <nav className="mt-2 space-y-1">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onTabChange(item.id as NavTab)}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-emerald-50 text-emerald-800 font-semibold border border-emerald-200'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50 border border-transparent'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-700' : 'text-slate-400'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-100 text-slate-500 border border-slate-200">
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Biological Context Card */}
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-800 flex items-center gap-1.5">
              <Info className="w-3.5 h-3.5 text-emerald-600" />
              Cultivo Activo
            </span>
            <span className="text-[10px] font-mono text-emerald-800 bg-emerald-100/70 px-1.5 py-0.5 rounded font-medium">
              Instar L5
            </span>
          </div>
          <p className="text-[11px] text-slate-500 leading-relaxed">
            Larvas en etapa de mayor ingesta y bioconversión de residuos orgánicos en <strong className="text-slate-700">ZONE-LAR</strong>.
          </p>
        </div>
      </div>

      {/* Footer Info */}
      <div className="pt-3 border-t border-slate-200 text-xs text-slate-400 font-mono flex items-center justify-between">
        <span>Arquitectura HAL</span>
        <span className="text-emerald-700 font-medium">Conectado</span>
      </div>
    </aside>
  );
};
