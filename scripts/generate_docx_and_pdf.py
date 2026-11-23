import os
import io
import zipfile
import subprocess
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

TEMPLATE_PATH = r"C:\Users\Danteeh\.gemini\antigravity\brain\bdf2aa3e-3592-461d-9e64-4229e08555cf\.user_uploaded\media_1795473207225_eff193f6.docx"
OUT_DIR = r"E:\BSF Moscas\Integrante 2"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GITHUB_BASE = "https://github.com/Danteeh/BSF-MonitorForLarvaes/blob/main"

ACTIVITIES_DATA = [
    {
        "num": "1. Validar las variables críticas del proceso biológico y ambiental",
        "dev": "Se definieron y validaron los rangos operacionales óptimos para las tres zonas productivas de Hermetia illucens: fotoperiodo e intensidad lumínica (10.000-15.000 lux) y humedad (60-75 %) en ZONE-REP; saturación higrométrica (>70 %) en ZONE-INC; y en ZONE-LAR temperatura interna de sustrato (30-38 °C), gradiente térmico de fricción metabólica (ΔT), humedad de lecho y monitoreo gravimétrico continuo.",
        "evidencias": [
            {"text": "guia_agente.md", "url": f"{GITHUB_BASE}/guia_agente.md"},
            {"text": "DATA_MODEL.md", "url": f"{GITHUB_BASE}/docs/DATA_MODEL.md"},
            {"text": "01_Guia_Maestra_Desarrollo_Zootecnico.pdf", "url": None},
            {"text": "03_Modelo_Datos_Esquema_PostgreSQL.pdf", "url": None}
        ]
    },
    {
        "num": "2. Establecer requerimientos de visualización en tiempo real y de consulta histórica",
        "dev": "Se especificaron los contratos de telemetría continua por WebSocket (frecuencia de 5 s) y los parámetros de consulta REST para series temporales históricas (últimos 60 a 80 registros por sensor) con capacidad de exportación a archivo CSV para análisis bioestadístico.",
        "evidencias": [
            {"text": "API_SPECIFICATION.md", "url": f"{GITHUB_BASE}/docs/API_SPECIFICATION.md"},
            {"text": "App.tsx", "url": f"{GITHUB_BASE}/frontend/src/App.tsx"},
            {"text": "02_Especificacion_API_REST_WebSockets.pdf", "url": None}
        ]
    },
    {
        "num": "3. Determinar los límites operativos para ambientes de baja temperatura",
        "dev": "Se modelaron las restricciones de desarrollo en la sabana de Bogotá: temperatura basal fisiológica (T_base = 13.5 °C), umbral de letargo bajo 20 °C, umbral de estrés térmico crítico (>41 °C) en el lecho larvario y gradiente de fermentación aerobia ΔT.",
        "evidencias": [
            {"text": "guia_agente.md", "url": f"{GITHUB_BASE}/guia_agente.md"},
            {"text": "ExperimentalProtocol.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/ExperimentalProtocol.tsx"},
            {"text": "01_Guia_Maestra_Desarrollo_Zootecnico.pdf", "url": None}
        ]
    },
    {
        "num": "4. Determinar condiciones para captura de variables",
        "dev": "Se establecieron las especificaciones de carga y metadatos de muestras fotográficas reales (formatos JPG/PNG hasta 10 MB), indexación por zona y lote, y la clasificación de telemetría con flags de calidad (valid, degraded, invalid).",
        "evidencias": [
            {"text": "ADR-005-media-storage.md", "url": f"{GITHUB_BASE}/docs/DECISIONS/ADR-005-media-storage.md"},
            {"text": "media.py", "url": f"{GITHUB_BASE}/backend/app/api/v1/media.py"},
            {"text": "08_ADR-005_Almacenamiento_Multimedia.pdf", "url": None}
        ]
    },
    {
        "num": "5. Elaborar casos de uso y escenarios operativos (UX)",
        "dev": "Se estructuraron los flujos de interacción del operario e investigador: monitoreo de microclimas en vivo, control de fotoperiodo, registro de alimentación periódica, inspección macroscópica de larvas y auditoría de alertas tempranas.",
        "evidencias": [
            {"text": "guia_agente.md", "url": f"{GITHUB_BASE}/guia_agente.md"},
            {"text": "CONTRIBUTING.md", "url": f"{GITHUB_BASE}/CONTRIBUTING.md"},
            {"text": "01_Guia_Maestra_Desarrollo_Zootecnico.pdf", "url": None},
            {"text": "05_Estandares_Ingenieria_Contribucion.pdf", "url": None}
        ]
    },
    {
        "num": "6. Definir la navegación de la plataforma (UX)",
        "dev": "Se diseñó la arquitectura de información con 7 módulos temáticos accesibles desde la barra lateral: Biorreactor Central, Zonas del Proceso, Protocolo & Ecuaciones, Inspección Óptica, Lotes y Nutrición, Telemetría & Gráficas y Control HAL.",
        "evidencias": [
            {"text": "Sidebar.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/Sidebar.tsx"},
            {"text": "App.tsx", "url": f"{GITHUB_BASE}/frontend/src/App.tsx"},
            {"text": "04_Indice_Documentacion_Tecnica.pdf", "url": None}
        ]
    },
    {
        "num": "7. Diseñar panel diferenciado de monitoreo operativo",
        "dev": "Se implementó la vista multizona (ZONE-REP, ZONE-INC, ZONE-LAR) con tarjetas de métricas en tiempo real que presentan variable física, valor, unidad, rango esperado y estado operativo de conexión.",
        "evidencias": [
            {"text": "ZoneCard.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/ZoneCard.tsx"},
            {"text": "MetricCard.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/MetricCard.tsx"}
        ]
    },
    {
        "num": "8. Diseñar panel diferenciado de seguimiento biológico de larvas",
        "dev": "Se implementó el widget del ciclo ontogénico (Adultos, Huevos, Larva L5, Prepupa) y la estación de morfometría macroscópica con catálogo fotográfico y caracterización morfológica de estadios L1 a L5.",
        "evidencias": [
            {"text": "LifeCycleWidget.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/LifeCycleWidget.tsx"},
            {"text": "MacroInspectionViewer.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/MacroInspectionViewer.tsx"}
        ]
    },
    {
        "num": "9. Diseñar panel diferenciado de indicadores de desempeño",
        "dev": "Se implementó la bitácora científica interactiva con formulación y cálculo en tiempo real de Eficiencia de Reducción de Residuos (WRE), Factor de Conversión Alimenticia (FCR) y acumulación térmica de Grados-Día (GDD).",
        "evidencias": [
            {"text": "ExperimentalProtocol.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/ExperimentalProtocol.tsx"},
            {"text": "01_Guia_Maestra_Desarrollo_Zootecnico.pdf", "url": None}
        ]
    },
    {
        "num": "10. Diseñar panel diferenciado de gestión de alertas",
        "dev": "Se incorporó el sistema de notificación visual en el encabezado con contador de alertas reactivo, código de colores para advertencias y panel de eventos no resueltos.",
        "evidencias": [
            {"text": "Header.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/Header.tsx"},
            {"text": "API_SPECIFICATION.md", "url": f"{GITHUB_BASE}/docs/API_SPECIFICATION.md"},
            {"text": "02_Especificacion_API_REST_WebSockets.pdf", "url": None}
        ]
    },
    {
        "num": "11. Validar prototipos generados y ajustar prototipos interactivos (UI)",
        "dev": "Se transformó la interfaz hacia un diseño de laboratorio diurno y limpio (#f8fafc) con tarjetas blancas (#ffffff) y bordes sutiles, eliminando estilos oscuros y fuentes neón, garantizando confort visual y ergonomía para jornadas de investigación.",
        "evidencias": [
            {"text": "tailwind.config.js", "url": f"{GITHUB_BASE}/frontend/tailwind.config.js"},
            {"text": "index.css", "url": f"{GITHUB_BASE}/frontend/src/index.css"},
            {"text": "CHANGELOG.md", "url": f"{GITHUB_BASE}/docs/CHANGELOG.md"},
            {"text": "06_Historial_Versiones_Changelog.pdf", "url": None}
        ]
    },
    {
        "num": "12. Validar el diseño del Dashboard principal y gemelo digital",
        "dev": "Se diseñó e integró el Gemelo Digital interactivo con conmutación entre jaula de vuelo, cámara de incubación y corte transversal del lecho larvario (superficie 0-3 cm, núcleo 3-10 cm, drenaje 10-15 cm).",
        "evidencias": [
            {"text": "BioreactorDigitalTwin.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/BioreactorDigitalTwin.tsx"},
            {"text": "BioreactorCoreWidget.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/BioreactorCoreWidget.tsx"}
        ]
    },
    {
        "num": "13. Validar el diseño de gráficos temporales multivariables",
        "dev": "Se configuró el componente de series temporales con biblioteca Recharts sobre fondo claro, gradiente esmeralda natural, cuadrícula sutil #f1f5f9, escala automática y tooltip detallado.",
        "evidencias": [
            {"text": "LiveTelemetryChart.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/LiveTelemetryChart.tsx"}
        ]
    },
    {
        "num": "14. Validar indicadores tipo semáforo y mapas ambientales",
        "dev": "Se implementaron tarjetas con insignias cromáticas de calidad (valid en esmeralda, degraded en ámbar, invalid en rojo) y diagnóstico espacial de estratos térmicos del biorreactor.",
        "evidencias": [
            {"text": "MetricCard.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/MetricCard.tsx"},
            {"text": "BioreactorDigitalTwin.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/BioreactorDigitalTwin.tsx"}
        ]
    },
    {
        "num": "15. Validar criterios de accesibilidad, usabilidad y documentar proceso",
        "dev": "Se verificó el contraste tipográfico WCAG AA, tipografías estándar legibles (Plus Jakarta Sans y JetBrains Mono), iconografía científica apropiada y documentación completa de diseño.",
        "evidencias": [
            {"text": "README.md", "url": f"{GITHUB_BASE}/docs/README.md"},
            {"text": "CONTRIBUTING.md", "url": f"{GITHUB_BASE}/CONTRIBUTING.md"},
            {"text": "04_Indice_Documentacion_Tecnica.pdf", "url": None},
            {"text": "05_Estandares_Ingenieria_Contribucion.pdf", "url": None}
        ]
    },
    {
        "num": "16. Programar la interfaz web y conexión reactiva con variables",
        "dev": "Se codificó la aplicación cliente en React 19 con TypeScript y Vite, integrando el enlace reactivo por WebSocket y los clientes de API REST asíncronos con manejo de reconexión automática.",
        "evidencias": [
            {"text": "App.tsx", "url": f"{GITHUB_BASE}/frontend/src/App.tsx"},
            {"text": "websocket.ts", "url": f"{GITHUB_BASE}/frontend/src/services/websocket.ts"},
            {"text": "api.ts", "url": f"{GITHUB_BASE}/frontend/src/services/api.ts"}
        ]
    },
    {
        "num": "17. Validar módulos: Captura, visualización en tiempo real y consulta histórica",
        "dev": "Se programó el búfer dinámico en memoria de hasta 80 puntos temporales por sensor, sincronizado continuamente con los endpoints REST y la base de datos PostgreSQL.",
        "evidencias": [
            {"text": "DATA_MODEL.md", "url": f"{GITHUB_BASE}/docs/DATA_MODEL.md"},
            {"text": "API_SPECIFICATION.md", "url": f"{GITHUB_BASE}/docs/API_SPECIFICATION.md"},
            {"text": "02_Especificacion_API_REST_WebSockets.pdf", "url": None},
            {"text": "03_Modelo_Datos_Esquema_PostgreSQL.pdf", "url": None}
        ]
    },
    {
        "num": "18. Validar módulos: Generación de reportes y trazabilidad de lotes",
        "dev": "Se desarrolló el módulo de exportación de telemetría a formato CSV y la tabla de trazabilidad de lotes con formulario modal para registrar masas de sustrato y dietas nutricionales.",
        "evidencias": [
            {"text": "BatchManagerModal.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/BatchManagerModal.tsx"},
            {"text": "batches.py", "url": f"{GITHUB_BASE}/backend/app/api/v1/batches.py"}
        ]
    },
    {
        "num": "19. Integrar servicios de almacenamiento de datos y archivo multimedia",
        "dev": "Se implementó el servicio de subida y almacenamiento de fotografías reales de colonias (/api/v1/media/upload), persistencia en disco y catálogo visual con previsualización en vivo.",
        "evidencias": [
            {"text": "CameraUploadModal.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/CameraUploadModal.tsx"},
            {"text": "ADR-005-media-storage.md", "url": f"{GITHUB_BASE}/docs/DECISIONS/ADR-005-media-storage.md"},
            {"text": "08_ADR-005_Almacenamiento_Multimedia.pdf", "url": None}
        ]
    },
    {
        "num": "20. Definir escenarios y realizar pruebas de usabilidad del sistema gráfico",
        "dev": "Se diseñaron flujos de prueba de usuario para la navegación en caliente, simulación de fallas de sensores desde el frontend (SimulatorControls) y respuesta visual inmediata sin recarga de página.",
        "evidencias": [
            {"text": "SimulatorControls.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/SimulatorControls.tsx"},
            {"text": "ADR-006-simulation-first.md", "url": f"{GITHUB_BASE}/docs/DECISIONS/ADR-006-simulation-first.md"},
            {"text": "09_ADR-006_Filosofia_Simulation_First.pdf", "url": None}
        ]
    },
    {
        "num": "21. Ajustar parámetros de visualización, escala milimétrica y alarmas",
        "dev": "Se calibró la retícula milimétrica calibrada a 5.0 mm en el visor macroscópico, el factor de zoom de 50 % a 250 % y la presentación visual de alertas críticas en la cabecera.",
        "evidencias": [
            {"text": "MacroInspectionViewer.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/MacroInspectionViewer.tsx"},
            {"text": "LiveTelemetryChart.tsx", "url": f"{GITHUB_BASE}/frontend/src/components/LiveTelemetryChart.tsx"}
        ]
    },
    {
        "num": "22. Analizar resultados y consolidar documentación técnica",
        "dev": "Se elaboró el registro histórico de versiones, las especificaciones arquitectónicas y la consolidación de entregables del sistema en el repositorio oficial de GitHub.",
        "evidencias": [
            {"text": "CHANGELOG.md", "url": f"{GITHUB_BASE}/docs/CHANGELOG.md"},
            {"text": "README.md", "url": f"{GITHUB_BASE}/docs/README.md"},
            {"text": "06_Historial_Versiones_Changelog.pdf", "url": None},
            {"text": "04_Indice_Documentacion_Tecnica.pdf", "url": None}
        ]
    }
]

def add_hyperlink(paragraph, url, text):
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = parse_xml(r'<w:hyperlink xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
                          r'r:id="%s" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>' % r_id)
    new_run = parse_xml(r'<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
    rPr = parse_xml(r'<w:rPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:color w:val="0563C1"/><w:u w:val="single"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>')
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

def format_cell_paragraph(p, text=None, bold=False, font_size_pt=10):
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    if text:
        run = p.add_run(text)
        run.bold = bold
        run.font.name = "Times New Roman"
        run.font.size = Pt(font_size_pt)
        return run
    return None

def build_docx():
    print("Leyendo plantilla DOCX...")
    buf = io.BytesIO()
    with zipfile.ZipFile(TEMPLATE_PATH) as zin:
        with zipfile.ZipFile(buf, 'w') as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == 'word/document.xml':
                    data = data.decode('utf-8').replace('w:val="end"', 'w:val="right"').replace('w:val="start"', 'w:val="left"').encode('utf-8')
                zout.writestr(item, data)

    buf.seek(0)
    doc = docx.Document(buf)

    tbl_act = doc.tables[0]
    
    # Conservamos la fila 0 (encabezado) y borramos las filas de Carlos
    while len(tbl_act.rows) > 1:
        tr = tbl_act.rows[-1]._tr
        tbl_act._tbl.remove(tr)

    print("Insertando actividades de Miguel Alejandro Chávez Porras...")
    for act in ACTIVITIES_DATA:
        row = tbl_act.add_row()
        
        # Columna 1: Actividad
        p0 = row.cells[0].paragraphs[0]
        format_cell_paragraph(p0, act["num"], bold=False, font_size_pt=9.5)
        
        # Columna 2: Desarrollo
        p1 = row.cells[1].paragraphs[0]
        format_cell_paragraph(p1, act["dev"], bold=False, font_size_pt=9.5)
        
        # Columna 3: Evidencia
        p2 = row.cells[2].paragraphs[0]
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = 1.15
        
        for i, ev in enumerate(act["evidencias"]):
            if ev["url"]:
                add_hyperlink(p2, ev["url"], ev["text"])
            else:
                run = p2.add_run(ev["text"])
                run.font.name = "Times New Roman"
                run.font.size = Pt(9.5)
            if i < len(act["evidencias"]) - 1:
                run_sep = p2.add_run("; ")
                run_sep.font.name = "Times New Roman"
                run_sep.font.size = Pt(9.5)

    # Actualizamos la tabla de firmas (Table 1)
    tbl_sig = doc.tables[1]
    cell_student = tbl_sig.rows[1].cells[0]
    cell_student.text = ""  # Limpiamos el texto previo
    
    p_sig = cell_student.paragraphs[0]
    p_sig.paragraph_format.space_before = Pt(0)
    p_sig.paragraph_format.space_after = Pt(0)
    p_sig.paragraph_format.line_spacing = 1.15
    
    r1 = p_sig.add_run("Miguel Alejandro Chávez Porras\n")
    r1.bold = True
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(10)
    
    r2 = p_sig.add_run("C.C. ---------\nCódigo: 20212020033\nCelular: ------------\nCorreo: machavezp@udistrital.edu.co\nAuxiliar de Investigación")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(10)

    # Guardar DOCX
    out_docx_1 = os.path.join(OUT_DIR, "INFORME_ACTIVIDADES_INTEGRANTE_2.docx")
    out_docx_2 = os.path.join(OUT_DIR, "INFORME_ACTIVIDADES_AUXILIAR_INVESTIGACION_MIGUEL_CHAVEZ.docx")
    
    doc.save(out_docx_1)
    doc.save(out_docx_2)
    print(f"[OK] Guardado DOCX: {out_docx_1}")
    print(f"[OK] Guardado DOCX: {out_docx_2}")

def build_pdf_from_html():
    print("Compilando version PDF idéntica a la plantilla DOCX...")
    
    rows_html = []
    for act in ACTIVITIES_DATA:
        ev_items = []
        for ev in act["evidencias"]:
            if ev["url"]:
                ev_items.append(f'<a href="{ev["url"]}">{ev["text"]}</a>')
            else:
                ev_items.append(f'<span>{ev["text"]}</span>')
        ev_html = "; ".join(ev_items)
        
        rows_html.append(f"""
        <tr>
            <td style="width: 35%;">{act["num"]}</td>
            <td style="width: 32%; text-align: justify;">{act["dev"]}</td>
            <td style="width: 33%;">{ev_html}</td>
        </tr>
        """)
        
    all_rows = "\n".join(rows_html)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>INFORME DE ACTIVIDADES AUXILIAR DE INVESTIGACIÓN 2026-3</title>
<style>
@page {{
    size: A4;
    margin: 25mm 30mm 25mm 30mm;
}}
body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 11pt;
    line-height: 1.25;
    color: #000000;
    margin: 0;
    padding: 0;
}}
p {{
    margin: 0 0 11pt 0;
    text-align: justify;
}}
.title-bold {{
    font-weight: bold;
}}
table.actividades {{
    width: 100%;
    border-collapse: collapse;
    margin: 12pt 0 16pt 0;
    font-size: 9.5pt;
}}
table.actividades th {{
    border: 1px solid #000000;
    padding: 6pt 6pt;
    font-weight: bold;
    text-align: left;
    background-color: #f2f2f2;
}}
table.actividades td {{
    border: 1px solid #000000;
    padding: 5pt 6pt;
    vertical-align: top;
}}
table.actividades tr {{
    page-break-inside: avoid;
}}
table.firmas {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20pt;
    page-break-inside: avoid;
}}
table.firmas td {{
    width: 50%;
    border: 1px solid #000000;
    padding: 10pt 12pt;
    vertical-align: top;
    font-size: 10pt;
    line-height: 1.3;
}}
a {{
    color: #0563C1;
    text-decoration: underline;
    word-break: break-all;
}}
</style>
</head>
<body>

<p>Bogotá D.C., 24 de noviembre del 2026</p>

<p>Doctora<br>
<span class="title-bold">LILIA EDIT APARICIO PICO</span><br>
Jefe Oficina de Investigaciones</p>

<p class="title-bold">Asunto: INFORME DE ACTIVIDADES AUXILIAR DE INVESTIGACIÓN 2026-3</p>

<p>Respetada doctora, me permito relacionar las actividades desarrolladas a lo largo de la vinculación como auxiliar de investigación 2026-3 vinculado en el proyecto de investigación</p>

<p>Optimización de biorreactores para el tratamiento de residuos orgánicos con larvas de mosca soldado negro en Bogotá y zonas de bajas temperaturas</p>

<p>Cuyo investigador principal es Paulo Alonso Gaona García</p>

<p class="title-bold">Desarrollo de actividades</p>

<table class="actividades">
    <thead>
        <tr>
            <th style="width: 35%;">Actividad</th>
            <th style="width: 32%;">Desarrollo</th>
            <th style="width: 33%;">Evidencia</th>
        </tr>
    </thead>
    <tbody>
        {all_rows}
    </tbody>
</table>

<p>Cordialmente,</p>

<p>Por lo anterior, las partes firman</p>

<table class="firmas">
    <tr style="height: 45pt;">
        <td style="border-bottom: none;">&nbsp;</td>
        <td style="border-bottom: none;">&nbsp;</td>
    </tr>
    <tr>
        <td style="border-top: none;">
            <strong>Miguel Alejandro Chávez Porras</strong><br>
            C.C. ---------<br>
            Código: 20212020033<br>
            Celular: ------------<br>
            Correo: machavezp@udistrital.edu.co<br>
            Auxiliar de Investigación
        </td>
        <td style="border-top: none;">
            <strong>Paulo Alonso Gaona García</strong><br>
            C.C. ---------<br>
            Investigador Principal<br>
            Universidad Distrital Francisco José de Caldas
        </td>
    </tr>
</table>

</body>
</html>
"""

    temp_html = os.path.join(OUT_DIR, "_temp_print.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    out_pdf_1 = os.path.join(OUT_DIR, "INFORME_ACTIVIDADES_INTEGRANTE_2.pdf")
    out_pdf_2 = os.path.join(OUT_DIR, "INFORME_ACTIVIDADES_AUXILIAR_INVESTIGACION_MIGUEL_CHAVEZ.pdf")
    
    cmd1 = [CHROME_PATH, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out_pdf_1}", f"file:///{os.path.abspath(temp_html)}"]
    subprocess.run(cmd1, capture_output=True, text=True)

    cmd2 = [CHROME_PATH, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out_pdf_2}", f"file:///{os.path.abspath(temp_html)}"]
    subprocess.run(cmd2, capture_output=True, text=True)

    if os.path.exists(temp_html):
        os.remove(temp_html)

    print(f"[OK] Generado PDF: {out_pdf_1} ({os.path.getsize(out_pdf_1) / 1024:.1f} KB)")
    print(f"[OK] Generado PDF: {out_pdf_2} ({os.path.getsize(out_pdf_2) / 1024:.1f} KB)")

if __name__ == "__main__":
    build_docx()
    build_pdf_from_html()
    print("Proceso completado exitosamente.")
