import os
import sys
import subprocess

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE_DIR = r"E:\BSF Moscas"

CSS_STYLES = """
@page {
    size: letter portrait;
    margin: 14mm 16mm 16mm 16mm;
    @bottom-center {
        content: "Pagina " counter(page) " de " counter(pages);
        font-size: 8pt;
        color: #64748b;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
}

body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.5;
    font-size: 9pt;
    margin: 0;
    padding: 0;
}

.report-header {
    margin-bottom: 20px;
    padding-bottom: 14px;
    border-bottom: 2px solid #059669;
}

.institution-title {
    font-size: 10pt;
    font-weight: 700;
    color: #065f46;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 3px;
}

.report-meta-badge {
    display: inline-block;
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #065f46;
    background-color: #ecfdf5;
    border: 1px solid #a7f3d0;
    padding: 2px 7px;
    border-radius: 4px;
    margin-bottom: 8px;
    font-family: Consolas, monospace;
}

.report-title {
    font-size: 17pt;
    font-weight: 800;
    color: #0f172a;
    margin: 4px 0;
    line-height: 1.25;
}

.report-subtitle {
    font-size: 9.5pt;
    color: #475569;
    margin-bottom: 12px;
}

.author-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 9px 12px;
    margin-top: 8px;
}

.author-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin: 0 !important;
}

.author-table td {
    padding: 2px 5px !important;
    border: none !important;
    background: transparent !important;
}

.author-label {
    color: #64748b;
    font-weight: 600;
    width: 22%;
}

.author-value {
    color: #0f172a;
    width: 28%;
}

h1 { 
    font-size: 13pt; 
    color: #065f46; 
    border-bottom: 1.5px solid #e2e8f0; 
    padding-bottom: 4px; 
    margin-top: 20px; 
    margin-bottom: 10px; 
    page-break-after: avoid; 
}

h2 { 
    font-size: 11pt; 
    color: #0f172a; 
    margin-top: 16px; 
    margin-bottom: 8px; 
    page-break-after: avoid; 
}

h3 { 
    font-size: 9.5pt; 
    color: #1e293b; 
    margin-top: 12px; 
    margin-bottom: 6px; 
    page-break-after: avoid; 
}

p {
    color: #334155;
    margin: 6px 0;
    text-align: justify;
}

ul, ol {
    margin: 6px 0;
    padding-left: 20px;
}

li {
    color: #334155;
    margin-bottom: 2px;
}

.mockup-container {
    margin: 14px 0 20px 0;
    page-break-inside: avoid;
    text-align: center;
}

.mockup-img {
    max-width: 100%;
    width: 100%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
    display: block;
    margin: 0 auto 8px auto;
}

.mockup-caption {
    font-size: 8pt;
    color: #64748b;
    font-style: italic;
    margin-top: 4px;
}

.tech-spec-table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 16px 0;
    font-size: 8pt;
    page-break-inside: avoid;
}

.tech-spec-table th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 5px 8px;
    border: 1px solid #cbd5e1;
}

.tech-spec-table td {
    padding: 4px 8px;
    border: 1px solid #e2e8f0;
    color: #334155;
}

.tech-spec-table tr:nth-child(even) td {
    background: #f8fafc;
}

.badge {
    display: inline-block;
    padding: 1px 5px;
    font-size: 7.5pt;
    font-weight: 600;
    border-radius: 3px;
    font-family: Consolas, monospace;
}

.badge-emerald { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
.badge-blue { background: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; }
.badge-amber { background: #fffbeb; color: #92400e; border: 1px solid #fde68a; }

.page-break {
    page-break-before: always;
}

.info-box {
    background: #f0fdf4;
    border-left: 3px solid #059669;
    padding: 8px 12px;
    margin: 10px 0;
    font-size: 8.5pt;
    color: #065f46;
}
"""

REPORT_1_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Dossier de Diseno de Interfaces Web - Integrante 1</title>
<style>
{css_styles}
</style>
</head>
<body>

<div class="report-header">
    <div class="institution-title">Universidad Distrital Francisco Jose de Caldas - Proyecto Curricular de Ingenieria</div>
    <div class="report-meta-badge">INFORME TECNICO Y CATALOGO DE MOCKUPS DE INTERFAZ WEB - BSF MONITOR</div>
    <div class="report-title">Dossier de Diseno de Interfaces: Hardware, HAL y Telemetria Operativa</div>
    <div class="report-subtitle">Sistema Computacional de Monitoreo y Control Biologico para Hermetia illucens (Mosca Soldado Negro)</div>
    
    <div class="author-card">
        <table class="author-table">
            <tr>
                <td class="author-label">Estudiante / Responsable:</td>
                <td class="author-value"><strong>Carlos Andres Pescador Castro</strong></td>
                <td class="author-label">Codigo Estudiantil:</td>
                <td class="author-value"><strong>20182020139</strong></td>
            </tr>
            <tr>
                <td class="author-label">Especialidad Asignada:</td>
                <td class="author-value">Ingenieria de Hardware, IoT, Capa HAL y Resiliencia</td>
                <td class="author-label">Plataforma Web:</td>
                <td class="author-value">React 18 + Vite + Tailwind CSS + Chart.js</td>
            </tr>
        </table>
    </div>
</div>

<h1>1. Resumen Ejecutivo y Alcance Tecnico</h1>
<p>
El presente informe consolida el diseno y la implementacion de las interfaces web correspondientes al frente de <strong>Hardware, Capa de Abstraccion de Hardware (HAL), Telemetria Multizona y Motor de Simulacion de Resiliencia</strong> dentro de la plataforma <strong>BSF MONITOR</strong>. Bajo la responsabilidad de Carlos Andres Pescador Castro (codigo 20182020139), se formularon 4 interfaces funcionales orientadas a satisfacer las exigencias de supervision fisica, diagnostico de buses de comunicacion de campo e inyeccion controlada de fallas para entornos zootecnicos de cultivo intensivo de larvas de <em>Hermetia illucens</em>.
</p>
<p>
Cada interfaz ha sido concebida bajo la filosofia estetica de <strong>laboratorio diurno de investigacion</strong>, empleando fondos claros (slate-50 / white), tipografia de alta legibilidad, bordes estructurales sutiles y paletas cromaticas normalizadas que erradican distorsiones visuales y aseguran el estricto cumplimiento de accesibilidad y ergonomia cognitiva.
</p>

<h1>2. Filosofia de Diseno e Identidad Visual del Sistema</h1>
<ul>
    <li><strong>Sustrato Visual Neutro:</strong> Fondo general en tonalidad #f8fafc (slate-50) con paneles en blanco puro (#ffffff) y bordes contrastados en #e2e8f0 (slate-200), emulando cuadernos de laboratorio clinico y suites de grado instrumental.</li>
    <li><strong>Codificacion Cromatica Funcional:</strong> Se reserva el verde esmeralda (#059669) para estados estables/optimos, el azul cobalto (#2563eb) para telemetria continua, el ambar (#d97706) para advertencias tempranas y el carmesi (#dc2626) exclusivamente para fallas criticas de transductores.</li>
    <li><strong>Tipografia Instrumental:</strong> Inter y Segoe UI para encabezados y cuerpos de lectura, complementadas con Consolas / SF Mono para lecturas crudas de paquetes MQTT, direcciones hexadecimales I2C (0x44, 0x40, 0x62) e identificadores ROM 1-Wire (28-00000...).</li>
</ul>

<div class="page-break"></div>

<h1>3. Catalogo de Interfaces Desarrolladas</h1>

<h2>Mockup 01: Consola de Resiliencia HAL e Inyeccion Controlada de Fallas</h2>
<p>
Esta interfaz permite al operador e investigador simular contingencias fisicas y perturbaciones en los buses de campo sin alterar el hardware en produccion. Implementada en el componente <code>SimulatorControls.tsx</code>, ofrece perfiles de estres termico, congelamiento ambiental y degradacion intencional de transductores de temperatura, humedad, dioxido de carbono y celdas de carga.
</p>

<div class="mockup-container">
    <img src="{img_m1_1}" class="mockup-img" alt="Consola de Resiliencia HAL">
    <div class="mockup-caption">Figura 1.1: Interfaz de Consola de Resiliencia HAL e Inyeccion de Fallas (mockup_01_consola_hal_fallas.png).</div>
</div>

<table class="tech-spec-table">
    <thead>
        <tr>
            <th>Parametro Operativo</th>
            <th>Rango / Opciones</th>
            <th>Componente React</th>
            <th>Proposito Zootecnico / Tecnico</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Latencia de Red / Bus</td>
            <td>0 ms a 2500 ms</td>
            <td><code>SimulatorControls.tsx</code></td>
            <td>Simulacion de retardo en la propagacion de tramas MQTT sobre enlaces Wi-Fi/Ethernet.</td>
        </tr>
        <tr>
            <td>Jitter de Medicion</td>
            <td>0 ms a 500 ms</td>
            <td><code>SimulatorControls.tsx</code></td>
            <td>Validacion de buffers temporales ante variabilidad en tiempos de sondeo de sensores.</td>
        </tr>
        <tr>
            <td>Tasa de Descarte de Paquetes</td>
            <td>0.0% a 25.0%</td>
            <td><code>SimulatorControls.tsx</code></td>
            <td>Prueba de resiliencia del pipeline de telemetria ante perdida de tramas de telemetria.</td>
        </tr>
        <tr>
            <td>Inyeccion de Fallas Especificas</td>
            <td>Falla SHT31, Falla DS18B20, Falla CO2, Falla Balanza</td>
            <td><code>SimulatorControls.tsx</code></td>
            <td>Comprobacion de fallback y conmutacion de actuadores a estado seguro (Fail-Safe).</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<h2>Mockup 02: Monitoreo Multizona y Sensores de Proceso en Tiempo Real</h2>
<p>
Presenta el estado operacional distribuido de las 4 zonas criticas del biorreactor (Z-01 Superior, Z-02 Media, Z-03 Inferior y Z-04 Camara de Descarga). Desplegado mediante <code>ZoneCard.tsx</code> y <code>MetricCard.tsx</code>, permite visualizar simultaneamente temperatura, humedad relativa, concentracion de CO2 y masa de biomasa por estrato.
</p>

<div class="mockup-container">
    <img src="{img_m1_2}" class="mockup-img" alt="Monitoreo Multizona">
    <div class="mockup-caption">Figura 1.2: Panel de Monitoreo Multizona y Sensores de Proceso (mockup_02_monitoreo_multizona_sensores.png).</div>
</div>

<table class="tech-spec-table">
    <thead>
        <tr>
            <th>Zona de Monitoreo</th>
            <th>Sensores Asociados</th>
            <th>Rango Termico Optimo</th>
            <th>Estado Operacional</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Zona Z-01 (Estrato Superior)</td>
            <td>DS18B20 #1, SHT31 (Aire), SCD30</td>
            <td>28.5 C - 31.0 C</td>
            <td><span class="badge badge-emerald">NORMAL / ACTIVO</span></td>
        </tr>
        <tr>
            <td>Zona Z-02 (Estrato Medio)</td>
            <td>DS18B20 #2, DHT22</td>
            <td>29.0 C - 33.5 C</td>
            <td><span class="badge badge-amber">ALERTA TERMICA (+32.4 C)</span></td>
        </tr>
        <tr>
            <td>Zona Z-03 (Estrato Inferior)</td>
            <td>DS18B20 #3, Celda HX711 #1</td>
            <td>27.0 C - 30.0 C</td>
            <td><span class="badge badge-emerald">NORMAL / ACTIVO</span></td>
        </tr>
        <tr>
            <td>Zona Z-04 (Tolva y Lixiviados)</td>
            <td>DS18B20 #4, Celda HX711 #2</td>
            <td>24.0 C - 28.0 C</td>
            <td><span class="badge badge-emerald">NORMAL / ACTIVO</span></td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<h2>Mockup 03: Telemetria de Series Temporales y Exportacion CSV de Datos Crudos</h2>
<p>
Esta interfaz grafica permite el analisis cronologico de variables biofisicas mediante graficos vectoriales de alta precision implementados con <code>LiveTelemetryChart.tsx</code> y <code>Chart.js</code>. Ofrece selectores de ventana temporal (1h, 6h, 24h, 7d), aislamiento de variables mediante leyenda interactiva y exportacion directa de datasets limpios a formato CSV.
</p>

<div class="mockup-container">
    <img src="{img_m1_3}" class="mockup-img" alt="Telemetria de Series Temporales">
    <div class="mockup-caption">Figura 1.3: Telemetria de Series Temporales y Consola de Exportacion CSV (mockup_03_telemetria_series_temporales.png).</div>
</div>

<table class="tech-spec-table">
    <thead>
        <tr>
            <th>Serie Temporal</th>
            <th>Frecuencia de Muestreo</th>
            <th>Unidades de Ingenieria</th>
            <th>Algoritmo de Filtrado</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Temperatura de Sustrato</td>
            <td>1.0 Hz (1 muestra/segundo)</td>
            <td>Grados Celsius (C)</td>
            <td>Filtro de media movil exponencial (EMA, alfa = 0.25).</td>
        </tr>
        <tr>
            <td>Humedad Relativa de Espacio de Cabeza</td>
            <td>0.5 Hz (1 muestra cada 2 s)</td>
            <td>Porcentaje (% HR)</td>
            <td>Ventana deslizante de 10 muestras con rechazo de outliers.</td>
        </tr>
        <tr>
            <td>Emision Metabolica de CO2</td>
            <td>0.2 Hz (1 muestra cada 5 s)</td>
            <td>Partes por Millon (ppm)</td>
            <td>Compensacion automatica de presion y temperatura (SCD30).</td>
        </tr>
        <tr>
            <td>Masa Neta de la Cohorte</td>
            <td>0.1 Hz (1 muestra cada 10 s)</td>
            <td>Kilogramos (kg)</td>
            <td>Filtro digital notch para cancelacion de vibracion mecanica.</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<h2>Mockup 04: Topologia de Hardware y Diagnostico de Buses Fisicos</h2>
<p>
Provee un esquema tecnico interactivo de la arquitectura de conexion fisica entre la computadora monoplaca Raspberry Pi 4 Model B, el concentrador de adquisicion ESP32 y los buses industriales de transductores. Permite diagnosticar en tiempo real el trafico de tramas, colisiones de bus I2C, tiempos de respuesta 1-Wire y calibracion de puente de Wheatstone (HX711).
</p>

<div class="mockup-container">
    <img src="{img_m1_4}" class="mockup-img" alt="Topologia de Hardware">
    <div class="mockup-caption">Figura 1.4: Diagnostico de Topologia de Hardware y Buses Fisicos (mockup_04_topologia_hardware_biorreactor.png).</div>
</div>

<table class="tech-spec-table">
    <thead>
        <tr>
            <th>Bus Fisico</th>
            <th>Topologia / Protocolo</th>
            <th>Direccion / Pinout</th>
            <th>Dispositivos Conectados</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Bus I2C Principal (i2c-1)</td>
            <td>Maestro-Esclavo (3.3V, 100 kHz)</td>
            <td>SDA: GPIO 2, SCL: GPIO 3</td>
            <td>SHT31 (0x44), SCD30 (0x61), Pantalla OLED SSD1306 (0x3C).</td>
        </tr>
        <tr>
            <td>Bus Dallas 1-Wire</td>
            <td>Multi-Drop Asincrono</td>
            <td>1-Wire: GPIO 4 (Pull-up 4.7k)</td>
            <td>Arreglo de 4 sondas de inmersion de acero DS18B20 (ROMs unicas).</td>
        </tr>
        <tr>
            <td>Canal SPI / Bit-Banging</td>
            <td>Serial de 2 Hilos</td>
            <td>DT: GPIO 5, SCK: GPIO 6</td>
            <td>Convertidor A/D HX711 de 24 bits para celda de carga de 20 kg.</td>
        </tr>
        <tr>
            <td>Canal de Actuacion PWM / Rele</td>
            <td>Salidas Digitales Optoacopladas</td>
            <td>GPIO 17, 27, 22</td>
            <td>SSR para calefactor ceramico, MOSFET PWM para ventilacion forzada.</td>
        </tr>
    </tbody>
</table>

<h1>4. Matriz de Cumplimiento de Requerimientos</h1>
<p>
Las 4 interfaces generadas para el Integrante 1 satisfacen plenamente los requerimientos tecnicos y funcionales estipulados en la carta de responsabilidades academicas:
</p>
<ul>
    <li><strong>REQ-HW-01:</strong> Despliegue de variables ambientales y fisicas en tiempo real mediante interfaz grafica reactiva.</li>
    <li><strong>REQ-HW-02:</strong> Visualizacion de alarmas y estados de contingencia con senalizacion semaforica estandarizada.</li>
    <li><strong>REQ-HW-03:</strong> Inyeccion de anomalias controladas para auditoria de resiliencia del software de control.</li>
    <li><strong>REQ-HW-04:</strong> Diagnostico de salud de los buses de campo y tasa de transferencia de telemetria MQTT.</li>
</ul>

</body>
</html>
"""

REPORT_2_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Dossier de Diseno de Interfaces Web - Integrante 2</title>
<style>
{css_styles}
</style>
</head>
<body>

<div class="report-header">
    <div class="institution-title">Universidad Distrital Francisco Jose de Caldas - Proyecto Curricular de Ingenieria</div>
    <div class="report-meta-badge">INFORME TECNICO Y CATALOGO DE MOCKUPS DE INTERFAZ WEB - BSF MONITOR</div>
    <div class="report-title">Dossier de Diseno de Interfaces: UX/UI, Gemelo Digital y Analitica Zootecnica</div>
    <div class="report-subtitle">Sistema Computacional de Monitoreo y Control Biologico para Hermetia illucens (Mosca Soldado Negro)</div>
    
    <div class="author-card">
        <table class="author-table">
            <tr>
                <td class="author-label">Estudiante / Responsable:</td>
                <td class="author-value"><strong>Miguel Alejandro Chavez Porras</strong></td>
                <td class="author-label">Codigo Estudiantil:</td>
                <td class="author-value"><strong>20212020033</strong></td>
            </tr>
            <tr>
                <td class="author-label">Especialidad Asignada:</td>
                <td class="author-value">Diseno UX/UI, Gemelo Digital, Morfometria Optica y Trazabilidad</td>
                <td class="author-label">Plataforma Web:</td>
                <td class="author-value">React 18 + TypeScript + Lucide Icons + Tailwind CSS</td>
            </tr>
        </table>
    </div>
</div>

<h1>1. Resumen Ejecutivo y Alcance de Experiencia de Usuario</h1>
<p>
El presente informe documenta el desarrollo de las interfaces de usuario (UI) y la arquitectura de experiencia de usuario (UX) lideradas por <strong>Miguel Alejandro Chavez Porras</strong> (codigo 20212020033) para la plataforma <strong>BSF MONITOR</strong>. El alcance cubre la representacion ciberfisica del biorreactor mediante un <strong>Gemelo Digital de 3 niveles</strong>, la estacion de <strong>morfometria optica y clasificacion ontogenica de estadios larvales</strong>, la <strong>bitacora de investigacion y calculadora de bioconversion zootecnica</strong>, y la <strong>consola de gestion y trazabilidad de lotes y dietas</strong>.
</p>
<p>
El enfoque de diseno prioriza la reduccion de la carga cognitiva del investigador biologico mediante componentes atomicos desacoplados, densidad informativa controlada y jerarquia visual basada en la estetica de laboratorio diurno (#f8fafc canvas, superficies blancas, bordes sutiles y acentos esmeralda/ambar normalizados).
</p>

<h1>2. Criterios de Accesibilidad y Arquitectura de Informacion</h1>
<ul>
    <li><strong>Navegacion Jerarquica Optimizada:</strong> Barra superior compacta con estado del nodo central, conmutador de entorno operacional y acceso a modulos principales en 1 clic.</li>
    <li><strong>Sombreado y Profundidad Tactil:</strong> Uso moderado de elevaciones CSS (shadow-sm, shadow-md) para denotar capas activas de interaccion sin generar saturacion visual.</li>
    <li><strong>Conformidad WCAG 2.1 AA:</strong> Ratios de contraste superiores a 4.5:1 en todos los textos e indicadores de estado, garantizando legibilidad en pantallas de monitoreo de campo bajo iluminacion natural.</li>
</ul>

<div class="page-break"></div>

<h1>3. Catalogo de Interfaces Desarrolladas</h1>

<h2>Mockup 01: Dashboard Central y Gemelo Digital de 3 Niveles del Biorreactor</h2>
<p>
Constituye la pantalla de entrada principal del sistema. Integra el componente <code>BioreactorDigitalTwin.tsx</code> y <code>BioreactorCoreWidget.tsx</code>, presentando un corte esquematico del biorreactor cilíndrico seccionado en 3 niveles de sustrato (superior, medio, profundo). Refleja el estado en tiempo real de los actuadores (ventilador PWM, calefactor ceramico, humidificador ultrasonico) y los gradientes termicos.
</p>

<div class="mockup-container">
    <img src="{img_m2_1}" class="mockup-img" alt="Dashboard Central y Gemelo Digital">
    <div class="mockup-caption">Figura 2.1: Dashboard Central con Gemelo Digital de 3 Niveles (mockup_01_dashboard_gemelo_digital.png).</div>
</div>

<table class="tech-spec-table">
    <thead>
        <tr>
            <th>Seccion de Interfaz</th>
            <th>Componente React</th>
            <th>Informacion Desplegada</th>
            <th>Interaccion de Usuario</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Corte de Gemelo Digital</td>
            <td><code>BioreactorDigitalTwin.tsx</code></td>
            <td>Gradiente de temperatura por nivel sustrato (31.2 C, 32.4 C, 29.8 C).</td>
            <td>Seleccion de estrato para expansion de telemetria detallada.</td>
        </tr>
        <tr>
            <td>Panel de Actuadores</td>
            <td><code>ActuatorControlPanel.tsx</code></td>
            <td>Estado de ventilador (65% PWM), calefactor (OFF), humidificador (ON).</td>
            <td>Conmutacion manual/automatica y ajuste fino de consignas.</td>
        </tr>
        <tr>
            <td>Tarjetas de Resumen KPI</td>
            <td><code>KpiSummaryCard.tsx</code></td>
            <td>Biomasa viva estimada (14.2 kg), Tasa de conversion (FCR 1.82).</td>
            <td>Enlace directo a informes de bioconversion y balance de masas.</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<h2>Mockup 02: Estacion de Morfometria Optica y Clasificacion Ontogenica</h2>
<p>
Diseñada en el componente <code>MacroInspectionViewer.tsx</code>, esta interfaz ofrece una estacion de vision computacional asistida para el seguimiento ontogenico de <em>Hermetia illucens</em>. Dispone de un visor macroscopico con reticula milimetrica de 5.0 mm, reconocimiento de contornos larvales, clasificacion automatica de estadios (L1 a L6, prepupa, pupa) y calculo biometrico de longitud media.
</p>

<div class="mockup-container">
    <img src="{img_m2_2}" class="mockup-img" alt="Estacion de Morfometria Optica">
    <div class="mockup-caption">Figura 2.2: Estacion de Morfometria Optica y Clasificacion Ontogenica (mockup_02_estacion_morfometria_optica.png).</div>
</div>

<table class="tech-spec-table">
    <thead>
        <tr>
            <th>Elemento Grafico</th>
            <th>Especificacion Tecnica</th>
            <th>Metrica Zootecnica</th>
            <th>Precision / Resolucion</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Reticula Calibrada</td>
            <td>Grilla ortogonal de paso 5.0 mm</td>
            <td>Referencia espacial dimensional absoluta</td>
            <td>Resolucion submilimetrica (0.1 mm)</td>
        </tr>
        <tr>
            <td>Bounding Boxes de Larvas</td>
            <td>Cuadros delimitadores vectoriales verdes</td>
            <td>Identificacion individual de especimenes</td>
            <td>IoU > 0.85 en camara macroscopica</td>
        </tr>
        <tr>
            <td>Histograma Ontogenico</td>
            <td>Grafico de barras de distribucion</td>
            <td>% de poblacion en estadio L4, L5, Prepupa</td>
            <td>Actualizacion en cada captura fotografica</td>
        </tr>
        <tr>
            <td>Biometria Promedio</td>
            <td>Longitud (mm) y diametro maximo (mm)</td>
            <td>Velocidad de elongacion diaria (mm/dia)</td>
            <td>Desviacion estandar y coeficiente de variacion</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<h2>Mockup 03: Bitacora de Ensayos y Calculadora de Bioconversion</h2>
<p>
Modulo cientifico implementado en <code>ExperimentalProtocol.tsx</code> que integra formalmente el marco teorico zootecnico. Presenta las formulas matematicas de Eficiencia de Reduccion de Residuos (WRE), Tasa de Conversion de Alimento (FCR) y Grados-Dia de Desarrollo (GDD), junto a una calculadora interactiva que valida los balances de masa experimentales.
</p>

<div class="mockup-container">
    <img src="{img_m2_3}" class="mockup-img" alt="Bitacora de Ensayos y Calculadora">
    <div class="mockup-caption">Figura 2.3: Bitacora de Ensayos y Calculadora de Ecuaciones Zootecnicas (mockup_03_bitacora_ecuaciones_bioconversion.png).</div>
</div>

<table class="tech-spec-table">
    <thead>
        <tr>
            <th>Ecuacion Zootecnica</th>
            <th>Expresion Matematica</th>
            <th>Variables de Entrada</th>
            <th>Valor Tipico Esperado</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Reduccion de Residuos (WRE)</td>
            <td><code>WRE (%) = [(W_in - W_res) / W_in] * 100</code></td>
            <td>Sustrato inicial (kg), residuo final (kg)</td>
            <td>55.0% a 75.0% en dietas organicas</td>
        </tr>
        <tr>
            <td>Tasa de Conversion (FCR)</td>
            <td><code>FCR = Alimento Ingerido (kg) / Ganancia Peso (kg)</code></td>
            <td>Masa de alimento neto, biomasa cosechada</td>
            <td>1.5 a 2.2 kg alimento / kg larva</td>
        </tr>
        <tr>
            <td>Grados-Dia de Desarrollo (GDD)</td>
            <td><code>GDD = Sumatoria [(T_media - T_base) * dias]</code></td>
            <td>Historial termico diario, T_base = 13.5 C</td>
            <td>380 a 450 GDD para estadio prepupal</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<h2>Mockup 04: Trazabilidad de Lotes de Produccion y Gestion de Dietas</h2>
<p>
Interfaz para la gestion de cohortes productivas desarrollada en <code>BatchManagerModal.tsx</code> y vistas tabulares de auditoria. Permite registrar lotes de siembra (cepas, fecha de inoculacion, peso inicial de neonatos), monitorear suministros de dietas (bagazo cervecero, pulpa de frutas, estiercol avicola) y validar balances de salida previo al cosechado.
</p>

<div class="mockup-container">
    <img src="{img_m2_4}" class="mockup-img" alt="Trazabilidad de Lotes y Dietas">
    <div class="mockup-caption">Figura 2.4: Trazabilidad de Lotes de Produccion y Gestion de Dietas (mockup_04_trazabilidad_lotes_dietas.png).</div>
</div>

<table class="tech-spec-table">
    <thead>
        <tr>
            <th>Atributo del Lote</th>
            <th>Ejemplo de Registro</th>
            <th>Validacion del Sistema</th>
            <th>Impacto en Trazabilidad</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Codigo Unico de Lote</td>
            <td><code>LOT-2026-HI-042</code></td>
            <td>Generacion automatica mediante UUID / serie</td>
            <td>Indice principal de base de datos relacional.</td>
        </tr>
        <tr>
            <td>Composicion de la Dieta</td>
            <td>Bagazo Cervecero 60% + Orujo Citrico 40%</td>
            <td>Suma porcentual normalizada al 100%</td>
            <td>Correlacion con la tasa de crecimiento y FCR.</td>
        </tr>
        <tr>
            <td>Etapa Ontogenica Actual</td>
            <td>Larva Estadio 5 (L5) - Dia 12</td>
            <td>Verificada con modulo morfometrico optico</td>
            <td>Programacion de cosecha y retencion de luz.</td>
        </tr>
        <tr>
            <td>Supervivencia Proyectada</td>
            <td>94.2% (Densidad: 4 larvas/cm2)</td>
            <td>Modelo logistico de decaimiento poblacional</td>
            <td>Estimacion del rendimiento final de proteina.</td>
        </tr>
    </tbody>
</table>

<h1>4. Matriz de Cumplimiento de Requerimientos UX/UI</h1>
<p>
Las 4 interfaces web entregadas para el Integrante 2 validan exhaustivamente los compromisos de su perfil academico:
</p>
<ul>
    <li><strong>REQ-UI-01:</strong> Diseno de paneles diferenciados para monitoreo operativo, seguimiento biologico y trazabilidad zootecnica.</li>
    <li><strong>REQ-UI-02:</strong> Implementacion de gemelo digital interactivo con renderizado de corte tridimensional de sustrato.</li>
    <li><strong>REQ-UI-03:</strong> Estacion optica de medicion biometrica y clasificacion de estadios larvales.</li>
    <li><strong>REQ-UI-04:</strong> Integracion de protocolos experimentales con calculadoras dinamicas de rendimiento biotecnologico.</li>
</ul>

</body>
</html>
"""

def generate_pdf(html_content, output_pdf_path, temp_html_path):
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--virtual-time-budget=2000",
        f"--print-to-pdf={output_pdf_path}",
        f"file:///{os.path.abspath(temp_html_path)}"
    ]
    
    print(f"Ejecutando generacion PDF -> {output_pdf_path}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(temp_html_path):
        try:
            os.remove(temp_html_path)
        except Exception:
            pass
            
    if os.path.exists(output_pdf_path) and os.path.getsize(output_pdf_path) > 0:
        size_kb = os.path.getsize(output_pdf_path) / 1024
        print(f"[OK] PDF Creado exitosamente: {output_pdf_path} ({size_kb:.1f} KB)")
        return True
    else:
        print(f"[ERROR] Fallo al crear PDF (codigo {res.returncode}): {res.stderr}")
        return False

def main():
    print("Iniciando compilacion de dossiers de mockups para Integrante 1 e Integrante 2...")
    
    # Rutas de imagenes Integrante 1
    int1_dir = os.path.join(BASE_DIR, "Integrante 1")
    int1_mockups_dir = os.path.join(int1_dir, "mockups")
    m1_1 = os.path.abspath(os.path.join(int1_mockups_dir, "mockup_01_consola_hal_fallas.png")).replace("\\", "/")
    m1_2 = os.path.abspath(os.path.join(int1_mockups_dir, "mockup_02_monitoreo_multizona_sensores.png")).replace("\\", "/")
    m1_3 = os.path.abspath(os.path.join(int1_mockups_dir, "mockup_03_telemetria_series_temporales.png")).replace("\\", "/")
    m1_4 = os.path.abspath(os.path.join(int1_mockups_dir, "mockup_04_topologia_hardware_biorreactor.png")).replace("\\", "/")
    
    # Rutas de imagenes Integrante 2
    int2_dir = os.path.join(BASE_DIR, "Integrante 2")
    int2_mockups_dir = os.path.join(int2_dir, "mockups")
    m2_1 = os.path.abspath(os.path.join(int2_mockups_dir, "mockup_01_dashboard_gemelo_digital.png")).replace("\\", "/")
    m2_2 = os.path.abspath(os.path.join(int2_mockups_dir, "mockup_02_estacion_morfometria_optica.png")).replace("\\", "/")
    m2_3 = os.path.abspath(os.path.join(int2_mockups_dir, "mockup_03_bitacora_ecuaciones_bioconversion.png")).replace("\\", "/")
    m2_4 = os.path.abspath(os.path.join(int2_mockups_dir, "mockup_04_trazabilidad_lotes_dietas.png")).replace("\\", "/")
    
    # Integrante 1
    html_1 = REPORT_1_HTML.format(
        css_styles=CSS_STYLES,
        img_m1_1=f"file:///{m1_1}",
        img_m1_2=f"file:///{m1_2}",
        img_m1_3=f"file:///{m1_3}",
        img_m1_4=f"file:///{m1_4}"
    )
    pdf_1 = os.path.join(int1_dir, "MOCKUPS_INTERFACES_INTEGRANTE_1.pdf")
    temp_1 = os.path.join(int1_dir, "_temp_mockups.html")
    generate_pdf(html_1, pdf_1, temp_1)
    
    # Integrante 2
    html_2 = REPORT_2_HTML.format(
        css_styles=CSS_STYLES,
        img_m2_1=f"file:///{m2_1}",
        img_m2_2=f"file:///{m2_2}",
        img_m2_3=f"file:///{m2_3}",
        img_m2_4=f"file:///{m2_4}"
    )
    pdf_2 = os.path.join(int2_dir, "MOCKUPS_INTERFACES_INTEGRANTE_2.pdf")
    temp_2 = os.path.join(int2_dir, "_temp_mockups.html")
    generate_pdf(html_2, pdf_2, temp_2)
    
    print("\nCompilacion de reportes PDF de mockups finalizada con exito.")

if __name__ == "__main__":
    main()
