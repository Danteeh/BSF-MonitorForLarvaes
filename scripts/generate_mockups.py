import os
import subprocess

BASE_DIR = r"E:\BSF Moscas"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

DIR_INT1 = os.path.join(BASE_DIR, "Integrante 1", "mockups")
DIR_INT2 = os.path.join(BASE_DIR, "Integrante 2", "mockups")

os.makedirs(DIR_INT1, exist_ok=True)
os.makedirs(DIR_INT2, exist_ok=True)

COMMON_CSS = """
* { box-sizing: border-box; }
body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: #f8fafc;
    color: #0f172a;
    -webkit-font-smoothing: antialiased;
}
.app-container {
    display: flex;
    flex-direction: column;
    height: 900px;
    width: 1440px;
    background-color: #f8fafc;
    overflow: hidden;
}
.header {
    height: 64px;
    background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
}
.brand-group {
    display: flex;
    align-items: center;
    gap: 12px;
}
.brand-logo {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #047857;
}
.brand-title {
    font-size: 14px;
    font-weight: 700;
    color: #0f172a;
    display: flex;
    align-items: center;
    gap: 8px;
}
.badge-version {
    font-family: Consolas, monospace;
    font-size: 10px;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    padding: 2px 6px;
    border-radius: 4px;
    color: #475569;
}
.brand-subtitle {
    font-size: 11px;
    color: #64748b;
}
.header-indicators {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 12px;
}
.header-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 6px 12px;
    border-radius: 8px;
    font-family: Consolas, monospace;
    color: #475569;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
}
.main-wrapper {
    display: flex;
    flex: 1;
    overflow: hidden;
}
.sidebar {
    width: 260px;
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex-shrink: 0;
}
.sidebar-section-title {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #94a3b8;
    padding: 0 12px;
    margin-bottom: 8px;
}
.nav-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 9px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 500;
    color: #475569;
    margin-bottom: 3px;
    border: 1px solid transparent;
}
.nav-item.active {
    background: #ecfdf5;
    color: #065f46;
    font-weight: 600;
    border-color: #a7f3d0;
}
.nav-item-left {
    display: flex;
    align-items: center;
    gap: 10px;
}
.badge-nav {
    font-family: Consolas, monospace;
    font-size: 10px;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    padding: 1px 5px;
    border-radius: 4px;
    color: #64748b;
}
.context-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 12px;
    margin-top: 12px;
}
.context-title {
    font-size: 12px;
    font-weight: 600;
    color: #1e293b;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
}
.context-desc {
    font-size: 11px;
    color: #64748b;
    line-height: 1.4;
    margin: 0;
}
.content-area {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.top-action-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
}
.page-title {
    font-size: 16px;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
}
.page-subtitle {
    font-size: 12px;
    color: #64748b;
    margin: 2px 0 0 0;
}
.btn-primary {
    background: #059669;
    color: #ffffff;
    font-size: 12px;
    font-weight: 500;
    padding: 7px 14px;
    border-radius: 8px;
    border: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.btn-secondary {
    background: #ffffff;
    color: #334155;
    font-size: 12px;
    font-weight: 500;
    padding: 7px 14px;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}
.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}
.badge-status {
    font-family: Consolas, monospace;
    font-size: 10px;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 600;
}
.badge-valid { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
.badge-degraded { background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }
.badge-invalid { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
"""

def render_sidebar(active_id="overview"):
    items = [
        ("overview", "Biorreactor Central", None),
        ("zones", "Zonas del Proceso", None),
        ("protocol", "Protocolo & Ecuaciones", None),
        ("macro", "Inspeccion & Fotografias", None),
        ("batches", "Lotes y Nutricion", None),
        ("telemetry", "Telemetria & Graficas", None),
        ("simulator", "Control HAL & Fallas", "HAL")
    ]
    html = ['<aside class="sidebar"><div><div class="sidebar-section-title">Modulos del Sistema</div><nav>']
    for mid, mlabel, mbadge in items:
        is_act = "active" if mid == active_id else ""
        badge_html = f'<span class="badge-nav">{mbadge}</span>' if mbadge else ""
        html.append(f'''
        <div class="nav-item {is_act}">
            <div class="nav-item-left">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
                <span>{mlabel}</span>
            </div>
            {badge_html}
        </div>
        ''')
    html.append('''
    </nav>
    <div class="context-box">
        <div class="context-title">
            <span>Cultivo Activo</span>
            <span style="font-family: Consolas, monospace; font-size: 10px; background: #ecfdf5; color: #047857; padding: 2px 6px; border-radius: 4px;">Instar L5</span>
        </div>
        <p class="context-desc">Larvas en etapa de mayor ingesta y bioconversion de residuos organicos en <strong>ZONE-LAR</strong>.</p>
    </div>
    </div>
    <div style="padding-top: 12px; border-top: 1px solid #e2e8f0; font-size: 11px; font-family: Consolas, monospace; color: #94a3b8; display: flex; justify-content: space-between;">
        <span>Arquitectura HAL</span>
        <span style="color: #059669; font-weight: 600;">Conectado</span>
    </div>
    </aside>
    ''')
    return "".join(html)

def render_header(time_str="17:50:24 (UTC-5)", alert_count=1):
    return f'''
    <header class="header">
        <div class="brand-group">
            <div class="brand-logo">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 1 0 0-14h-1"/><path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/><path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3"/></svg>
            </div>
            <div>
                <div class="brand-title">
                    <span>BSF MONITOR</span>
                    <span class="badge-version">v1.0 - Lab</span>
                </div>
                <div class="brand-subtitle">Sistema de Monitoreo Biologico - <em>Hermetia illucens</em></div>
            </div>
        </div>
        <div class="header-indicators">
            <div class="header-pill">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <span>{time_str}</span>
            </div>
            <div class="header-pill">
                <span>Modo: <strong style="color: #047857;">SIMULACION</strong></span>
            </div>
            <div class="header-pill">
                <span class="status-dot"></span>
                <span>Telemetria Activa</span>
            </div>
            <div class="header-pill" style="background: #fffbeb; border-color: #fde68a; color: #92400e;">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <span>{alert_count} Alerta Activa</span>
            </div>
        </div>
    </header>
    '''

def capture_screenshot(html_content, out_png):
    temp_html = out_png.replace(".png", "_temp.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--window-size=1440,900",
        f"--screenshot={out_png}",
        f"file:///{os.path.abspath(temp_html)}"
    ]
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"[OK] Generado Mockup: {os.path.basename(out_png)} ({os.path.getsize(out_png)/1024:.1f} KB)")

# ==============================================================================
# INTEGRANTE 1: MOCKUPS (Carlos Andres Pescador Castro)
# ==============================================================================

# 1. Consola de Control HAL e Inyeccion de Fallas
def build_int1_mockup_01():
    out = os.path.join(DIR_INT1, "mockup_01_consola_hal_fallas.png")
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Mockup 1 - Control HAL</title><style>{COMMON_CSS}</style></head>
<body>
<div class="app-container">
    {render_header()}
    <div class="main-wrapper">
        {render_sidebar("simulator")}
        <main class="content-area">
            <div class="top-action-bar">
                <div>
                    <h1 class="page-title">Laboratorio de Resiliencia y Control HAL</h1>
                    <p class="page-subtitle">Inyeccion de perturbaciones controladas para pruebas de tolerancia a fallos</p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-secondary">Restablecer Sensores</button>
                    <button class="btn-primary">Ejecutar Ensayo</button>
                </div>
            </div>

            <div class="card" style="display: flex; flex-direction: column; gap: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; pb: 14px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="padding: 8px; border-radius: 8px; background: #f1f5f9; border: 1px solid #e2e8f0; color: #334155;">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 2v7.31"/><path d="M14 9.3V2"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/><path d="M5.52 16h12.96"/></svg>
                        </div>
                        <div>
                            <div style="font-weight: 700; font-size: 14px;">Consola de Inyeccion de Fallas (Hardware Abstraction Layer)</div>
                            <div style="font-size: 11px; color: #64748b;">Prueba de deteccion automatica de lecturas anomalas y marcado de calidad</div>
                        </div>
                    </div>
                    <span class="badge-status badge-valid">HAL ACTIVO - SIMULACION</span>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div>
                        <label style="display: block; font-size: 12px; font-weight: 600; color: #334155; margin-bottom: 6px;">Sensor a Perturbar</label>
                        <select style="width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-family: Consolas, monospace; font-size: 12px; background: #ffffff;">
                            <option>LAR-TEMP-001 - Temperatura del Sustrato (ZONE-LAR)</option>
                            <option>REP-HUM-001 - Humedad Relativa (ZONE-REP)</option>
                            <option>INC-TEMP-001 - Temperatura Incubacion (ZONE-INC)</option>
                            <option>LAR-WEIGHT-001 - Celda de Carga Masa Lecho (ZONE-LAR)</option>
                        </select>
                    </div>
                    <div>
                        <label style="display: block; font-size: 12px; font-weight: 600; color: #334155; margin-bottom: 6px;">Escenario de Contingencia</label>
                        <select style="width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-family: Consolas, monospace; font-size: 12px; background: #ffffff;">
                            <option>Sobrecalentamiento Biologico Critico (>50 °C - Hipertermia)</option>
                            <option>Interrupcion de Bus Electrico (Desconexion de sonda)</option>
                            <option>Senal Congelada (Fallo ADC / Lectura estancada)</option>
                            <option>Restablecer Comportamiento Fisiologico Normal</option>
                        </select>
                    </div>
                </div>

                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px; display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 12px; color: #475569;">
                        Estado actual: Las lecturas se etiquetan como <code style="color: #b45309; font-weight: 600;">degraded</code> o <code style="color: #b91c1c; font-weight: 600;">invalid</code> y difunden alertas tempranas.
                    </div>
                    <button class="btn-primary" style="background: #1e293b;">Inyectar Escenario</button>
                </div>

                <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 12px 16px; font-family: Consolas, monospace; font-size: 11px; color: #065f46; display: flex; align-items: center; gap: 8px;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                    <span>Comando emitido via MQTT topic: bsf/simulator/command | Escenario 'out_of_range' aplicado al sensor LAR-TEMP-001</span>
                </div>
            </div>

            <div class="card" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px;">
                    <div style="font-size: 11px; color: #64748b; font-weight: 600;">BUS I2C (REP / INC)</div>
                    <div style="font-size: 18px; font-weight: 700; color: #0f172a; margin-top: 4px;">4 Nodos Conectados</div>
                    <div style="font-size: 11px; color: #059669; font-family: Consolas, monospace; margin-top: 4px;">Tasa de refresco: 5000 ms</div>
                </div>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px;">
                    <div style="font-size: 11px; color: #64748b; font-weight: 600;">BUS 1-WIRE (LAR-TEMP)</div>
                    <div style="font-size: 18px; font-weight: 700; color: #0f172a; margin-top: 4px;">DS18B20 Calibrado</div>
                    <div style="font-size: 11px; color: #059669; font-family: Consolas, monospace; margin-top: 4px;">Precision: +- 0.5 °C</div>
                </div>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px;">
                    <div style="font-size: 11px; color: #64748b; font-weight: 600;">BROKER MOSQUITTO</div>
                    <div style="font-size: 18px; font-weight: 700; color: #0f172a; margin-top: 4px;">0 Paquetes Perdidos</div>
                    <div style="font-size: 11px; color: #059669; font-family: Consolas, monospace; margin-top: 4px;">QoS: 0 (At most once)</div>
                </div>
            </div>
        </main>
    </div>
</div>
</body></html>"""
    capture_screenshot(html, out)

# 2. Panel Multizona de Monitoreo Operativo
def build_int1_mockup_02():
    out = os.path.join(DIR_INT1, "mockup_02_monitoreo_multizona_sensores.png")
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Mockup 2 - Monitoreo Multizona</title><style>{COMMON_CSS}</style></head>
<body>
<div class="app-container">
    {render_header()}
    <div class="main-wrapper">
        {render_sidebar("zones")}
        <main class="content-area">
            <div class="top-action-bar">
                <div>
                    <h1 class="page-title">Zonas de Cria y Monitoreo Ambiental</h1>
                    <p class="page-subtitle">Supervision desacoplada de condiciones microclimaticas en REP, INC y LAR</p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-secondary">Exportar Telemetria</button>
                    <button class="btn-primary">+ Registrar Suministro</button>
                </div>
            </div>

            <!-- ZONA 1: ZONE-REP -->
            <div class="card" style="display: flex; flex-direction: column; gap: 14px; padding: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="padding: 6px; border-radius: 6px; background: #ecfdf5; color: #047857;">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
                        </div>
                        <div>
                            <span style="font-weight: 700; font-size: 13px;">ZONE-REP: Camara de Reproduccion y Oviposicion</span>
                            <span style="font-family: Consolas, monospace; font-size: 10px; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; margin-left: 6px;">NODE-REP-001</span>
                        </div>
                    </div>
                    <span class="badge-status badge-valid">ESTADO: OPERATIVO</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px;">
                        <div style="font-size: 11px; color: #64748b;">Temperatura Ambiental (REP-TEMP-001)</div>
                        <div style="font-size: 22px; font-weight: 700; color: #0f172a; margin-top: 4px; font-family: Consolas, monospace;">27.4 <span style="font-size: 13px;">°C</span></div>
                        <div style="font-size: 10px; color: #047857; margin-top: 4px;">Rango optimo: 26.0 - 29.0 °C</div>
                    </div>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px;">
                        <div style="font-size: 11px; color: #64748b;">Humedad Relativa (REP-HUM-001)</div>
                        <div style="font-size: 22px; font-weight: 700; color: #0f172a; margin-top: 4px; font-family: Consolas, monospace;">68.2 <span style="font-size: 13px;">%</span></div>
                        <div style="font-size: 10px; color: #047857; margin-top: 4px;">Rango optimo: 60.0 - 75.0 %</div>
                    </div>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px;">
                        <div style="font-size: 11px; color: #64748b;">Intensidad Luminica (REP-LUX-001)</div>
                        <div style="font-size: 22px; font-weight: 700; color: #0f172a; margin-top: 4px; font-family: Consolas, monospace;">12.450 <span style="font-size: 13px;">lux</span></div>
                        <div style="font-size: 10px; color: #047857; margin-top: 4px;">Fotoperiodo activo (12h luz / 12h penumbra)</div>
                    </div>
                </div>
            </div>

            <!-- ZONA 2: ZONE-LAR -->
            <div class="card" style="display: flex; flex-direction: column; gap: 14px; padding: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="padding: 6px; border-radius: 6px; background: #ecfdf5; color: #047857;">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m2 12 10-6 10 6-10 6Z"/><path d="m2 17 10 6 10-6"/><path d="m2 7 10 6 10-6"/></svg>
                        </div>
                        <div>
                            <span style="font-weight: 700; font-size: 13px;">ZONE-LAR: Biorreactor Central de Bioconversion</span>
                            <span style="font-family: Consolas, monospace; font-size: 10px; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; margin-left: 6px;">NODE-LAR-001</span>
                        </div>
                    </div>
                    <span class="badge-status badge-valid">BIOCONVERSION ACTIVA</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px;">
                        <div style="font-size: 11px; color: #64748b;">Temp. Sustrato (LAR-TEMP-001)</div>
                        <div style="font-size: 22px; font-weight: 700; color: #0f172a; margin-top: 4px; font-family: Consolas, monospace;">34.8 <span style="font-size: 13px;">°C</span></div>
                        <div style="font-size: 10px; color: #047857; margin-top: 4px;">Gradiente termico: +9.8 °C sobre ambiente</div>
                    </div>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px;">
                        <div style="font-size: 11px; color: #64748b;">Humedad Sustrato (LAR-HUM-001)</div>
                        <div style="font-size: 22px; font-weight: 700; color: #0f172a; margin-top: 4px; font-family: Consolas, monospace;">68.5 <span style="font-size: 13px;">%</span></div>
                        <div style="font-size: 10px; color: #047857; margin-top: 4px;">Rango ideal de digestion: 60 - 75 %</div>
                    </div>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px;">
                        <div style="font-size: 11px; color: #64748b;">Masa Gravimetrica (LAR-WEIGHT-001)</div>
                        <div style="font-size: 22px; font-weight: 700; color: #0f172a; margin-top: 4px; font-family: Consolas, monospace;">16.42 <span style="font-size: 13px;">kg</span></div>
                        <div style="font-size: 10px; color: #047857; margin-top: 4px;">Celda de carga HX711 conectada</div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>
</body></html>"""
    capture_screenshot(html, out)

# 3. Matriz de Telemetría Multivariable y Curvas Temporales
def build_int1_mockup_03():
    out = os.path.join(DIR_INT1, "mockup_03_telemetria_series_temporales.png")
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Mockup 3 - Telemetria</title><style>{COMMON_CSS}</style></head>
<body>
<div class="app-container">
    {render_header()}
    <div class="main-wrapper">
        {render_sidebar("telemetry")}
        <main class="content-area">
            <div class="top-action-bar">
                <div>
                    <h1 class="page-title">Telemetria Multivariable en Tiempo Real</h1>
                    <p class="page-subtitle">Adquisicion dinamica y analisis de series temporales por nodo sensor</p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-secondary">Filtro de Sensores</button>
                    <button class="btn-primary">Exportar CSV</button>
                </div>
            </div>

            <!-- Controls bar -->
            <div class="card" style="padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 12px; font-weight: 600; color: #334155;">Sensor Activo:</span>
                    <select style="padding: 6px 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-family: Consolas, monospace; font-size: 12px;">
                        <option>LAR-TEMP-001 - Temperatura del Sustrato (ZONE-LAR)</option>
                        <option>LAR-WEIGHT-001 - Masa Gravimetrica (ZONE-LAR)</option>
                        <option>REP-TEMP-001 - Temperatura Ambiente (ZONE-REP)</option>
                    </select>
                </div>
                <div style="display: flex; align-items: center; gap: 10px; font-size: 12px; color: #64748b; font-family: Consolas, monospace;">
                    <span>Transmision: 5 s</span>
                    <span>•</span>
                    <span>80 puntos en buffer</span>
                </div>
            </div>

            <!-- Chart Mockup -->
            <div class="card" style="display: flex; flex-direction: column; gap: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px;">
                    <div>
                        <div style="font-weight: 700; font-size: 13px;">Curva Temporal: LAR-TEMP-001 (Temperatura de Sustrato)</div>
                        <div style="font-size: 11px; color: #64748b;">Comportamiento termogenico del lecho durante el ciclo de alimentacion</div>
                    </div>
                    <span class="badge-status badge-valid">Unidad: °C</span>
                </div>

                <div style="height: 280px; width: 100%; position: relative; background: #fafafa; border: 1px solid #f1f5f9; border-radius: 8px; display: flex; align-items: flex-end; padding: 20px 30px;">
                    <!-- Simulated Vector Area Chart SVG -->
                    <svg viewBox="0 0 1000 240" style="width: 100%; height: 100%; overflow: visible;">
                        <defs>
                            <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stop-color="#10b981" stop-opacity="0.25"/>
                                <stop offset="100%" stop-color="#10b981" stop-opacity="0.0"/>
                            </linearGradient>
                        </defs>
                        <!-- Grid lines -->
                        <line x1="0" y1="40" x2="1000" y2="40" stroke="#e2e8f0" stroke-dasharray="4"/>
                        <line x1="0" y1="100" x2="1000" y2="100" stroke="#e2e8f0" stroke-dasharray="4"/>
                        <line x1="0" y1="160" x2="1000" y2="160" stroke="#e2e8f0" stroke-dasharray="4"/>
                        <line x1="0" y1="220" x2="1000" y2="220" stroke="#cbd5e1"/>

                        <!-- Area Fill -->
                        <path d="M 0 140 Q 150 110, 300 130 T 600 70 T 800 85 T 1000 60 L 1000 220 L 0 220 Z" fill="url(#chartGrad)"/>
                        <!-- Stroke Line -->
                        <path d="M 0 140 Q 150 110, 300 130 T 600 70 T 800 85 T 1000 60" fill="none" stroke="#059669" stroke-width="3"/>
                        
                        <!-- Data Points -->
                        <circle cx="300" cy="130" r="4" fill="#059669"/>
                        <circle cx="600" cy="70" r="4" fill="#059669"/>
                        <circle cx="800" cy="85" r="4" fill="#059669"/>
                        <circle cx="1000" cy="60" r="5" fill="#047857"/>
                    </svg>
                </div>

                <div style="display: flex; justify-content: space-between; font-size: 11px; font-family: Consolas, monospace; color: #64748b; padding: 0 10px;">
                    <span>17:00:00</span>
                    <span>17:15:00</span>
                    <span>17:30:00</span>
                    <span>17:45:00</span>
                    <span>18:00:00</span>
                </div>
            </div>
        </main>
    </div>
</div>
</body></html>"""
    capture_screenshot(html, out)

# 4. Topología Física y Red IoT de Sensores
def build_int1_mockup_04():
    out = os.path.join(DIR_INT1, "mockup_04_topologia_hardware_biorreactor.png")
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Mockup 4 - Topologia Hardware</title><style>{COMMON_CSS}</style></head>
<body>
<div class="app-container">
    {render_header()}
    <div class="main-wrapper">
        {render_sidebar("simulator")}
        <main class="content-area">
            <div class="top-action-bar">
                <div>
                    <h1 class="page-title">Topologia de Hardware y Arquitectura IoT</h1>
                    <p class="page-subtitle">Distribucion de buses fisicos, transductores y conexion de nodos de captura</p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-secondary">Escanear Buses</button>
                    <button class="btn-primary">Ver Esquema Electrico</button>
                </div>
            </div>

            <div class="card" style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
                <!-- Left: Physical wiring schematic visualization -->
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; display: flex; flex-direction: column; gap: 14px;">
                    <div style="font-weight: 700; font-size: 13px; color: #0f172a; display: flex; justify-content: space-between;">
                        <span>Distribucion de Nodos Sensores y Buses</span>
                        <span style="font-family: Consolas, monospace; font-size: 10px; color: #059669;">Raspberry Pi 5 Gateway</span>
                    </div>

                    <div style="display: flex; flex-direction: column; gap: 10px;">
                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-weight: 600; font-size: 12px;">Bus I2C (GPIO 2 / 3 - SDA / SCL)</span>
                                <div style="font-size: 11px; color: #64748b;">Sensores SHT31-D (0x44, 0x45) y BH1750 (0x23)</div>
                            </div>
                            <span class="badge-status badge-valid">3 Dispositivos OK</span>
                        </div>

                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-weight: 600; font-size: 12px;">Bus 1-Wire (GPIO 4 - Pull-up 4.7k)</span>
                                <div style="font-size: 11px; color: #64748b;">Sonda Sumergible DS18B20 Acero Inox (Rom ID: 28-00000)</div>
                            </div>
                            <span class="badge-status badge-valid">1 Dispositivo OK</span>
                        </div>

                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-weight: 600; font-size: 12px;">Bus SPI / GPIO (HX711 DT/SCK)</span>
                                <div style="font-size: 11px; color: #64748b;">4 Celdas de Carga de 50 kg con puente Wheatstone</div>
                            </div>
                            <span class="badge-status badge-valid">Calibrado (Offset Tarado)</span>
                        </div>
                    </div>
                </div>

                <!-- Right: Hardware Diagnostics -->
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div class="card" style="padding: 14px;">
                        <div style="font-size: 11px; font-weight: 600; color: #64748b;">TENSION DE ALIMENTACION</div>
                        <div style="font-size: 20px; font-weight: 700; color: #0f172a; margin-top: 4px;">5.12 V <span style="font-size: 12px; color: #059669;">Nominal</span></div>
                    </div>
                    <div class="card" style="padding: 14px;">
                        <div style="font-size: 11px; font-weight: 600; color: #64748b;">FRECUENCIA DE ADQUISICION</div>
                        <div style="font-size: 20px; font-weight: 700; color: #0f172a; margin-top: 4px;">0.2 Hz <span style="font-size: 12px; color: #64748b;">(5 seg)</span></div>
                    </div>
                    <div class="card" style="padding: 14px;">
                        <div style="font-size: 11px; font-weight: 600; color: #64748b;">LATENCIA BROKER MQTT</div>
                        <div style="font-size: 20px; font-weight: 700; color: #0f172a; margin-top: 4px;">1.4 ms <span style="font-size: 12px; color: #059669;">Excelente</span></div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>
</body></html>"""
    capture_screenshot(html, out)

# ==============================================================================
# INTEGRANTE 2: MOCKUPS (Miguel Alejandro Chavez Porras)
# ==============================================================================

# 1. Dashboard Central y Gemelo Digital
def build_int2_mockup_01():
    out = os.path.join(DIR_INT2, "mockup_01_dashboard_gemelo_digital.png")
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Mockup 1 - Gemelo Digital</title><style>{COMMON_CSS}</style></head>
<body>
<div class="app-container">
    {render_header()}
    <div class="main-wrapper">
        {render_sidebar("overview")}
        <main class="content-area">
            <div class="top-action-bar">
                <div>
                    <h1 class="page-title">Biorreactor Central & Topologia del Sistema</h1>
                    <p class="page-subtitle">Esquema anatomico y distribucion espacial de variables biologicas</p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-secondary">Registrar Lote / Dieta</button>
                    <button class="btn-primary">Cargar Fotografia</button>
                </div>
            </div>

            <!-- Core Metrics Banner -->
            <div class="card" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; padding: 18px;">
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px;">
                    <div style="font-size: 11px; color: #64748b;">Temperatura del Sustrato (LAR-TEMP-001)</div>
                    <div style="font-size: 26px; font-weight: 700; color: #0f172a; font-family: Consolas, monospace; margin-top: 4px;">34.8 <span style="font-size: 14px;">°C</span></div>
                    <div style="font-size: 11px; color: #047857; margin-top: 4px;">Estado Fisiologico: Normal (30 - 36 °C)</div>
                </div>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px;">
                    <div style="font-size: 11px; color: #64748b;">Gradiente Termico (ΔT sobre ambiente)</div>
                    <div style="font-size: 26px; font-weight: 700; color: #b45309; font-family: Consolas, monospace; margin-top: 4px;">+9.8 <span style="font-size: 14px;">°C</span></div>
                    <div style="font-size: 11px; color: #b45309; margin-top: 4px;">Friccion metabolica larvaria intensa</div>
                </div>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px;">
                    <div style="font-size: 11px; color: #64748b;">Biomasa Neta en Digestor (LAR-WEIGHT-001)</div>
                    <div style="font-size: 26px; font-weight: 700; color: #0f172a; font-family: Consolas, monospace; margin-top: 4px;">16.42 <span style="font-size: 14px;">kg</span></div>
                    <div style="font-size: 11px; color: #047857; margin-top: 4px;">Lote activo: BATCH-2026-001</div>
                </div>
            </div>

            <!-- Gemelo Digital Cutaway Drawing -->
            <div class="card" style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
                <div>
                    <div style="font-weight: 700; font-size: 13px; margin-bottom: 12px; display: flex; justify-content: space-between;">
                        <span>Corte Transversal del Lecho Larvario (ZONE-LAR)</span>
                        <span style="font-family: Consolas, monospace; font-size: 11px; color: #047857;">Profundidad: 15 cm</span>
                    </div>

                    <div style="display: flex; flex-direction: column; gap: 8px;">
                        <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 12px;">
                            <div style="font-weight: 600; font-size: 12px; color: #065f46; display: flex; justify-content: space-between;">
                                <span>1. Estrato 0 - 3 cm: Superficie Aerobia y Alimento Fresco</span>
                                <span style="font-family: Consolas, monospace;">31.0 °C</span>
                            </div>
                            <div style="font-size: 11px; color: #047857; margin-top: 4px;">Zona de ventilacion pasiva y consumo de alimento dosificado.</div>
                        </div>

                        <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px;">
                            <div style="font-weight: 600; font-size: 12px; color: #92400e; display: flex; justify-content: space-between;">
                                <span>2. Estrato 3 - 10 cm: Nucleo Termogenico Larvario (Sensor LAR-TEMP-001)</span>
                                <span style="font-family: Consolas, monospace; font-weight: 700;">34.8 °C</span>
                            </div>
                            <div style="font-size: 11px; color: #92400e; margin-top: 4px;">Maxima densidad de biomasa (Instar L5). Fermentacion acelerada.</div>
                        </div>

                        <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 12px;">
                            <div style="font-weight: 600; font-size: 12px; color: #0369a1; display: flex; justify-content: space-between;">
                                <span>3. Estrato 10 - 15 cm: Base Drenante de Lixiviados</span>
                                <span style="font-family: Consolas, monospace;">33.3 °C</span>
                            </div>
                            <div style="font-size: 11px; color: #0369a1; margin-top: 4px;">Malla perforada de acero inox para evacuacion de condensados.</div>
                        </div>
                    </div>
                </div>

                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase;">Diagnostico Zootecnico</div>
                        <div style="font-size: 14px; font-weight: 700; color: #0f172a; margin-top: 6px;">Bioconversion Optima</div>
                        <p style="font-size: 11px; color: #64748b; line-height: 1.5; margin-top: 8px;">
                            El lecho a 34.8 °C indica digestion enzimatica activa de residuos de frutas y salvado. Sin riesgo de choque termico.
                        </p>
                    </div>
                    <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 6px; padding: 8px; font-size: 11px; color: #065f46;">
                        <strong>Recomendacion:</strong> Mantener aireacion pasiva. Proxima racion programada en 14 h.
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>
</body></html>"""
    capture_screenshot(html, out)

# 2. Estación de Morfometría Óptica y Muestras
def build_int2_mockup_02():
    out = os.path.join(DIR_INT2, "mockup_02_estacion_morfometria_optica.png")
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Mockup 2 - Morfometria</title><style>{COMMON_CSS}</style></head>
<body>
<div class="app-container">
    {render_header()}
    <div class="main-wrapper">
        {render_sidebar("macro")}
        <main class="content-area">
            <div class="top-action-bar">
                <div>
                    <h1 class="page-title">Morfometria Optica & Fotografia Real de Muestras</h1>
                    <p class="page-subtitle">Inspeccion macroscopica de estadios ontogenicos con reticula milimetrica calibrada</p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-secondary">Exportar Muestra</button>
                    <button class="btn-primary">+ Cargar Fotografia Real</button>
                </div>
            </div>

            <div class="card" style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
                <!-- Left: Viewport with 5.0mm grid -->
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px;">
                        <span style="font-size: 12px; font-weight: 600;">Muestra: muestra_larvas_lecho_lote01.jpg</span>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span class="badge-status badge-valid">Reticula: 5.0 mm</span>
                            <span style="font-family: Consolas, monospace; font-size: 11px;">Zoom: 100%</span>
                        </div>
                    </div>

                    <!-- Visual Viewport Canvas -->
                    <div style="height: 380px; background: #0f172a; border-radius: 8px; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center;">
                        <!-- Millimetric Grid Overlay -->
                        <div style="position: absolute; inset: 0; background-image: linear-gradient(to right, rgba(255,255,255,0.15) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.15) 1px, transparent 1px); background-size: 30px 30px; pointer-events: none;"></div>
                        
                        <!-- Simulated Specimen Graphic -->
                        <div style="width: 280px; height: 160px; border-radius: 40px; background: #92400e; opacity: 0.85; border: 2px solid #b45309; display: flex; align-items: center; justify-content: center; color: #fef3c7; font-size: 12px; font-family: Consolas, monospace; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
                            Muestra Biologica - Instar L5 (~22 mm)
                        </div>

                        <span style="position: absolute; bottom: 10px; right: 12px; font-family: Consolas, monospace; font-size: 10px; color: #a7f3d0; background: rgba(0,0,0,0.6); padding: 2px 6px; border-radius: 4px;">
                            Escala de calibracion: 1 division = 5.0 mm
                        </span>
                    </div>
                </div>

                <!-- Right: Ontogenic Guide -->
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <div style="font-size: 12px; font-weight: 700; color: #1e293b; text-transform: uppercase;">Guia de Clasificacion</div>
                    
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
                        <div style="font-weight: 600; font-size: 11px; display: flex; justify-content: space-between;">
                            <span>Neonato (L1)</span>
                            <span style="font-family: Consolas, monospace; color: #059669;">1 - 2 mm</span>
                        </div>
                        <div style="font-size: 10px; color: #64748b;">Blanco traslucido recien eclosionado.</div>
                    </div>

                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
                        <div style="font-weight: 600; font-size: 11px; display: flex; justify-content: space-between;">
                            <span>Instar L3</span>
                            <span style="font-family: Consolas, monospace; color: #059669;">6 - 10 mm</span>
                        </div>
                        <div style="font-size: 10px; color: #64748b;">Migracion activa en el sustrato.</div>
                    </div>

                    <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 6px; padding: 8px 12px;">
                        <div style="font-weight: 700; font-size: 11px; color: #065f46; display: flex; justify-content: space-between;">
                            <span>Instar L5 (Activo)</span>
                            <span style="font-family: Consolas, monospace;">19 - 25 mm</span>
                        </div>
                        <div style="font-size: 10px; color: #047857;">Maxima acumulacion lipidica y proteica.</div>
                    </div>

                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px;">
                        <div style="font-weight: 600; font-size: 11px; display: flex; justify-content: space-between;">
                            <span>Prepupa</span>
                            <span style="font-family: Consolas, monospace; color: #059669;">20 - 24 mm</span>
                        </div>
                        <div style="font-size: 10px; color: #64748b;">Cuticula melanica marron oscuro.</div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>
</body></html>"""
    capture_screenshot(html, out)

# 3. Bitácora Científica y Calculadora de Bioconversión
def build_int2_mockup_03():
    out = os.path.join(DIR_INT2, "mockup_03_bitacora_ecuaciones_bioconversion.png")
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Mockup 3 - Protocolo y Ecuaciones</title><style>{COMMON_CSS}</style></head>
<body>
<div class="app-container">
    {render_header()}
    <div class="main-wrapper">
        {render_sidebar("protocol")}
        <main class="content-area">
            <div class="top-action-bar">
                <div>
                    <h1 class="page-title">Protocolo Cientifico & Ecuaciones de Bioconversion</h1>
                    <p class="page-subtitle">Evaluacion cuantitativa de digestibilidad, conversion de nutrientes y fisiologia termica</p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-secondary">Exportar Parametros</button>
                    <button class="btn-primary">Guardar Ensayo</button>
                </div>
            </div>

            <!-- 3 Equation Cards -->
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
                <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="font-size: 10px; font-weight: 700; color: #059669; text-transform: uppercase;">Metrica 1 - Reduccion</div>
                        <div style="font-weight: 700; font-size: 13px; margin: 4px 0 10px 0;">Eficiencia de Reduccion (WRE)</div>
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px; font-family: Consolas, monospace; font-size: 11px; text-align: center;">
                            WRE (%) = [(W₀ - W₁) / W₀] × 100
                        </div>
                        <p style="font-size: 11px; color: #64748b; margin-top: 8px;">Porcentaje de residuo organico transformado en frass o asimilado.</p>
                    </div>
                    <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: baseline; font-family: Consolas, monospace;">
                        <span style="font-size: 11px; color: #047857;">Resultado Actual:</span>
                        <span style="font-size: 20px; font-weight: 700; color: #065f46;">75.0 %</span>
                    </div>
                </div>

                <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="font-size: 10px; font-weight: 700; color: #b45309; text-transform: uppercase;">Metrica 2 - Conversion</div>
                        <div style="font-weight: 700; font-size: 13px; margin: 4px 0 10px 0;">Tasa de Conversion (FCR)</div>
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px; font-family: Consolas, monospace; font-size: 11px; text-align: center;">
                            FCR = Alimento Seco (kg) / Biomasa (kg)
                        </div>
                        <p style="font-size: 11px; color: #64748b; margin-top: 8px;">Masa seca consumida por kilogramo de larva viva cosechada.</p>
                    </div>
                    <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: baseline; font-family: Consolas, monospace;">
                        <span style="font-size: 11px; color: #92400e;">Ratio FCR:</span>
                        <span style="font-size: 20px; font-weight: 700; color: #92400e;">1.83 : 1</span>
                    </div>
                </div>

                <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="font-size: 10px; font-weight: 700; color: #0369a1; text-transform: uppercase;">Metrica 3 - Fenologia</div>
                        <div style="font-weight: 700; font-size: 13px; margin: 4px 0 10px 0;">Modelo Grados-Dia (GDD)</div>
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px; font-family: Consolas, monospace; font-size: 11px; text-align: center;">
                            GDD diario = T_sustrato - 13.5 °C
                        </div>
                        <p style="font-size: 11px; color: #64748b; margin-top: 8px;">Suma termica acumulada requerida hasta prepupa (~220 GDD).</p>
                    </div>
                    <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: baseline; font-family: Consolas, monospace;">
                        <span style="font-size: 11px; color: #0284c7;">Tiempo a Cosecha:</span>
                        <span style="font-size: 20px; font-weight: 700; color: #0369a1;">~11 dias</span>
                    </div>
                </div>
            </div>

            <!-- Interactive Workbench Simulator -->
            <div class="card" style="display: flex; flex-direction: column; gap: 14px;">
                <div style="font-weight: 700; font-size: 13px;">Calculadora Experimental de Dietas & Rendimiento</div>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;">
                    <div>
                        <label style="display: block; font-size: 11px; color: #475569; margin-bottom: 4px;">Alimento Suministrado (kg)</label>
                        <input type="number" value="50.0" style="width: 100%; padding: 6px 10px; border: 1px solid #cbd5e1; border-radius: 6px; font-family: Consolas, monospace; font-size: 12px;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 11px; color: #475569; margin-bottom: 4px;">Residuo Remanente Frass (kg)</label>
                        <input type="number" value="12.5" style="width: 100%; padding: 6px 10px; border: 1px solid #cbd5e1; border-radius: 6px; font-family: Consolas, monospace; font-size: 12px;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 11px; color: #475569; margin-bottom: 4px;">Larva Viva Cosechada (kg)</label>
                        <input type="number" value="8.2" style="width: 100%; padding: 6px 10px; border: 1px solid #cbd5e1; border-radius: 6px; font-family: Consolas, monospace; font-size: 12px;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 11px; color: #475569; margin-bottom: 4px;">% Materia Seca Dieta (%)</label>
                        <input type="number" value="30" style="width: 100%; padding: 6px 10px; border: 1px solid #cbd5e1; border-radius: 6px; font-family: Consolas, monospace; font-size: 12px;">
                    </div>
                </div>
            </div>
        </main>
    </div>
</div>
</body></html>"""
    capture_screenshot(html, out)

# 4. Trazabilidad de Lotes de Producción y Gestión de Dietas
def build_int2_mockup_04():
    out = os.path.join(DIR_INT2, "mockup_04_trazabilidad_lotes_dietas.png")
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Mockup 4 - Trazabilidad de Lotes</title><style>{COMMON_CSS}</style></head>
<body>
<div class="app-container">
    {render_header()}
    <div class="main-wrapper">
        {render_sidebar("batches")}
        <main class="content-area">
            <div class="top-action-bar">
                <div>
                    <h1 class="page-title">Trazabilidad de Lotes y Formulacion Nutricional</h1>
                    <p class="page-subtitle">Registro historico de cohortes de larvas, dietas aplicadas y rendimientos zootecnicos</p>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-secondary">Exportar Historial</button>
                    <button class="btn-primary">+ Registrar Lote / Dieta</button>
                </div>
            </div>

            <!-- Batches Table -->
            <div class="card" style="padding: 16px; display: flex; flex-direction: column; gap: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-weight: 700; font-size: 13px;">Cohortes en Sistema de Cria</div>
                    <span style="font-size: 11px; color: #64748b; font-family: Consolas, monospace;">Total: 3 Lotes Activos</span>
                </div>

                <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
                    <thead>
                        <tr style="border-bottom: 2px solid #e2e8f0; text-align: left; color: #64748b; font-size: 11px;">
                            <th style="padding: 8px;">Codigo</th>
                            <th style="padding: 8px;">Modulo</th>
                            <th style="padding: 8px;">Etapa</th>
                            <th style="padding: 8px;">Masa Inicial</th>
                            <th style="padding: 8px;">Dieta / Sustrato</th>
                            <th style="padding: 8px;">Estado</th>
                            <th style="padding: 8px;">Fecha Inicio</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #f1f5f9;">
                            <td style="padding: 10px 8px; font-family: Consolas, monospace; font-weight: 700; color: #047857;">BATCH-2026-001</td>
                            <td style="padding: 10px 8px; font-family: Consolas, monospace;">ZONE-LAR</td>
                            <td style="padding: 10px 8px;">Larva (Instar L5)</td>
                            <td style="padding: 10px 8px; font-family: Consolas, monospace;">15.0 kg</td>
                            <td style="padding: 10px 8px; color: #475569;">Residuos horticolas y salvado de trigo</td>
                            <td style="padding: 10px 8px;"><span class="badge-status badge-valid">ACTIVO</span></td>
                            <td style="padding: 10px 8px; font-family: Consolas, monospace; color: #64748b;">18/11/2026</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #f1f5f9;">
                            <td style="padding: 10px 8px; font-family: Consolas, monospace; font-weight: 700; color: #047857;">BATCH-2026-002</td>
                            <td style="padding: 10px 8px; font-family: Consolas, monospace;">ZONE-INC</td>
                            <td style="padding: 10px 8px;">Incubacion Huevos</td>
                            <td style="padding: 10px 8px; font-family: Consolas, monospace;">0.25 kg</td>
                            <td style="padding: 10px 8px; color: #475569;">Dieta humeda de iniciacion</td>
                            <td style="padding: 10px 8px;"><span class="badge-status badge-valid">INCUBANDO</span></td>
                            <td style="padding: 10px 8px; font-family: Consolas, monospace; color: #64748b;">21/11/2026</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px 8px; font-family: Consolas, monospace; font-weight: 700; color: #047857;">BATCH-2026-003</td>
                            <td style="padding: 10px 8px; font-family: Consolas, monospace;">ZONE-REP</td>
                            <td style="padding: 10px 8px;">Imagos Adultos</td>
                            <td style="padding: 10px 8px; font-family: Consolas, monospace;">2.5 kg</td>
                            <td style="padding: 10px 8px; color: #475569;">Nebulizacion hidrica + atracion olfativa</td>
                            <td style="padding: 10px 8px;"><span class="badge-status badge-valid">OVIPOSICION</span></td>
                            <td style="padding: 10px 8px; font-family: Consolas, monospace; color: #64748b;">15/11/2026</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Feeding Modal Preview -->
            <div class="card" style="border: 2px solid #a7f3d0; background: #f0fdf4; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 700; font-size: 12px; color: #065f46;">Registro Rapido de Alimentacion: BATCH-2026-001</div>
                    <div style="font-size: 11px; color: #047857;">Ultima racion: 2.500 g de pulpa frutal fermentada suministrada exitosamente</div>
                </div>
                <button class="btn-primary" style="background: #047857;">+ Anadir Dosis Nutricional</button>
            </div>
        </main>
    </div>
</div>
</body></html>"""
    capture_screenshot(html, out)

def main():
    print("--- GENERANDO MOCKUPS INTEGRANTE 1 (Carlos Andres Pescador Castro) ---")
    build_int1_mockup_01()
    build_int1_mockup_02()
    build_int1_mockup_03()
    build_int1_mockup_04()

    print("\n--- GENERANDO MOCKUPS INTEGRANTE 2 (Miguel Alejandro Chavez Porras) ---")
    build_int2_mockup_01()
    build_int2_mockup_02()
    build_int2_mockup_03()
    build_int2_mockup_04()

    print("\nTodas las capturas de mockups generadas exitosamente!")

if __name__ == "__main__":
    main()
