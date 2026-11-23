import os
import sys
import re
import subprocess
import markdown

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE_DIR = r"E:\BSF Moscas"

STUDENTS = {
    1: {
        "name": "Carlos Andres Pescador Castro",
        "code": "20182020139",
        "folder": os.path.join(BASE_DIR, "Integrante 1"),
        "specialty": "Ingenieria de Hardware, IoT, Capa HAL y Simulacion"
    },
    2: {
        "name": "Miguel Alejandro Chavez Porras",
        "code": "20212020033",
        "folder": os.path.join(BASE_DIR, "Integrante 2"),
        "specialty": "Ingenieria de Software, APIs REST, Datos y Gobernanza"
    }
}

ASSIGNMENTS = [
    # INTEGRANTE 1: Carlos Andres Pescador Castro (20182020139)
    {
        "student_id": 1,
        "src": "README.md",
        "pdf_name": "01_README_Sistema_BSF_Monitor.pdf",
        "title": "Arquitectura General y Resumen del Sistema BSF Monitor"
    },
    {
        "student_id": 1,
        "src": "docs/ARCHITECTURE.md",
        "pdf_name": "02_Arquitectura_Global_Sistema.pdf",
        "title": "Documento de Arquitectura de Software y Hardware"
    },
    {
        "student_id": 1,
        "src": "docs/HARDWARE_ABSTRACTION.md",
        "pdf_name": "03_Capa_Abstraccion_Hardware_HAL.pdf",
        "title": "Especificacion de la Capa de Abstraccion de Hardware (HAL)"
    },
    {
        "student_id": 1,
        "src": "docs/MQTT_SPECIFICATION.md",
        "pdf_name": "04_Especificacion_Protocolo_MQTT.pdf",
        "title": "Protocolo de Comunicacion y Matriz de Topicos MQTT"
    },
    {
        "student_id": 1,
        "src": "docs/SIMULATOR_DESIGN.md",
        "pdf_name": "05_Diseno_Motor_Simulacion.pdf",
        "title": "Diseno del Motor de Simulacion IoT y Fallas"
    },
    {
        "student_id": 1,
        "src": "docs/REQUIREMENTS.md",
        "pdf_name": "06_Especificacion_Requerimientos.pdf",
        "title": "Documento de Especificacion de Requerimientos del Sistema"
    },
    {
        "student_id": 1,
        "src": "docs/DECISIONS/ADR-001-centralized-raspberry.md",
        "pdf_name": "07_ADR-001_Arquitectura_Centralizada.pdf",
        "title": "ADR-001: Seleccion de Arquitectura Centralizada en Raspberry Pi"
    },
    {
        "student_id": 1,
        "src": "docs/DECISIONS/ADR-003-mqtt-communication.md",
        "pdf_name": "08_ADR-003_Protocolo_MQTT.pdf",
        "title": "ADR-003: Seleccion del Protocolo MQTT para Telemetria"
    },
    {
        "student_id": 1,
        "src": "docs/DECISIONS/ADR-004-hardware-abstraction.md",
        "pdf_name": "09_ADR-004_Abstraccion_Hardware.pdf",
        "title": "ADR-004: Adopcion de la Capa de Abstraccion de Hardware (HAL)"
    },

    # INTEGRANTE 2: Miguel Alejandro Chavez Porras (20212020033)
    {
        "student_id": 2,
        "src": "guia_agente.md",
        "pdf_name": "01_Guia_Maestra_Desarrollo_Zootecnico.pdf",
        "title": "Guia Maestra de Desarrollo y Especificaciones Zootecnicas"
    },
    {
        "student_id": 2,
        "src": "docs/API_SPECIFICATION.md",
        "pdf_name": "02_Especificacion_API_REST_WebSockets.pdf",
        "title": "Especificacion de Endpoints API REST y WebSockets"
    },
    {
        "student_id": 2,
        "src": "docs/DATA_MODEL.md",
        "pdf_name": "03_Modelo_Datos_Esquema_PostgreSQL.pdf",
        "title": "Modelo de Datos Relacional y Series Temporales en PostgreSQL"
    },
    {
        "student_id": 2,
        "src": "docs/README.md",
        "pdf_name": "04_Indice_Documentacion_Tecnica.pdf",
        "title": "Indice y Mapa General de la Documentacion Tecnica"
    },
    {
        "student_id": 2,
        "src": "CONTRIBUTING.md",
        "pdf_name": "05_Estandares_Ingenieria_Contribucion.pdf",
        "title": "Guia de Estandares de Ingenieria, Flujos Git y Contribucion"
    },
    {
        "student_id": 2,
        "src": "docs/CHANGELOG.md",
        "pdf_name": "06_Historial_Versiones_Changelog.pdf",
        "title": "Registro Historico de Versiones y Cambios (Changelog)"
    },
    {
        "student_id": 2,
        "src": "docs/DECISIONS/ADR-002-postgresql.md",
        "pdf_name": "07_ADR-002_Base_Datos_PostgreSQL.pdf",
        "title": "ADR-002: Seleccion de PostgreSQL para Persistencia Transaccional"
    },
    {
        "student_id": 2,
        "src": "docs/DECISIONS/ADR-005-media-storage.md",
        "pdf_name": "08_ADR-005_Almacenamiento_Multimedia.pdf",
        "title": "ADR-005: Estrategia de Almacenamiento Multimedia y Archivos"
    },
    {
        "student_id": 2,
        "src": "docs/DECISIONS/ADR-006-simulation-first.md",
        "pdf_name": "09_ADR-006_Filosofia_Simulation_First.pdf",
        "title": "ADR-006: Filosofia de Desarrollo Simulation-First"
    }
]

CSS_STYLES = """
@page {
    size: A4;
    margin: 18mm 15mm 18mm 15mm;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.6;
    font-size: 10pt;
    margin: 0;
    padding: 0;
}

.report-header {
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 2px solid #059669;
}

.report-meta-badge {
    display: inline-block;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #065f46;
    background-color: #ecfdf5;
    border: 1px solid #a7f3d0;
    padding: 3px 8px;
    border-radius: 4px;
    margin-bottom: 8px;
    font-family: Consolas, monospace;
}

.report-title {
    font-size: 19pt;
    font-weight: 800;
    color: #0f172a;
    margin: 6px 0;
    line-height: 1.25;
}

.report-subtitle {
    font-size: 10pt;
    color: #475569;
    margin-bottom: 14px;
}

.author-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 14px;
    margin-top: 10px;
}

.author-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 9pt;
    margin: 0 !important;
}

.author-table td {
    padding: 3px 6px !important;
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

/* Headings */
h1 { font-size: 15pt; color: #065f46; border-bottom: 1px solid #e2e8f0; padding-bottom: 5px; margin-top: 24px; margin-bottom: 12px; page-break-after: avoid; }
h2 { font-size: 13pt; color: #0f172a; margin-top: 20px; margin-bottom: 10px; page-break-after: avoid; }
h3 { font-size: 11pt; color: #1e293b; margin-top: 16px; margin-bottom: 8px; page-break-after: avoid; }
h4 { font-size: 10pt; color: #334155; margin-top: 12px; margin-bottom: 6px; page-break-after: avoid; }

p {
    color: #334155;
    margin: 8px 0;
}

ul, ol {
    margin: 8px 0;
    padding-left: 22px;
}

li {
    color: #334155;
    margin-bottom: 3px;
}

/* Code */
code {
    font-family: Consolas, "Courier New", monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    padding: 1px 4px;
    border-radius: 4px;
    color: #0f172a;
}

pre {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 10px 12px;
    overflow-x: auto;
    font-size: 8pt;
    line-height: 1.45;
    page-break-inside: avoid;
    margin: 12px 0;
}

pre code {
    background: transparent;
    border: none;
    padding: 0;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
}

th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
    text-align: left;
    padding: 6px 8px;
    border: 1px solid #cbd5e1;
}

td {
    padding: 5px 8px;
    border: 1px solid #e2e8f0;
    color: #334155;
}

tr:nth-child(even) td {
    background: #f8fafc;
}

/* Blockquotes */
blockquote {
    border-left: 4px solid #10b981;
    background: #f0fdf4;
    margin: 12px 0;
    padding: 8px 12px;
    color: #065f46;
    font-style: italic;
    page-break-inside: avoid;
}

/* Mermaid diagrams */
.mermaid {
    text-align: center;
    margin: 16px auto;
    page-break-inside: avoid;
}

hr {
    border: none;
    height: 1px;
    background: #e2e8f0;
    margin: 18px 0;
}
"""

def strip_emojis(text):
    clean = []
    for ch in text:
        code = ord(ch)
        if (0x1F300 <= code <= 0x1FAFF) or (0x2600 <= code <= 0x27BF) or (0x1F1E6 <= code <= 0x1F1FF) or (0x1F900 <= code <= 0x1F9FF):
            continue
        clean.append(ch)
    return "".join(clean)

def process_markdown(content):
    content = strip_emojis(content)
    
    # Process mermaid blocks
    pattern_mermaid = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
    content = pattern_mermaid.sub(r'<div class="mermaid">\n\1\n</div>', content)
    
    # Process GitHub alerts
    content = re.sub(r"^>\s*\[!NOTE\]\s*(.*)", r"<blockquote><strong>NOTA:</strong> \1", content, flags=re.MULTILINE)
    content = re.sub(r"^>\s*\[!TIP\]\s*(.*)", r"<blockquote><strong>CONSEJO:</strong> \1", content, flags=re.MULTILINE)
    content = re.sub(r"^>\s*\[!IMPORTANT\]\s*(.*)", r"<blockquote><strong>IMPORTANTE:</strong> \1", content, flags=re.MULTILINE)
    content = re.sub(r"^>\s*\[!WARNING\]\s*(.*)", r"<blockquote><strong>ADVERTENCIA:</strong> \1", content, flags=re.MULTILINE)
    
    # Convert MD to HTML
    html_body = markdown.markdown(content, extensions=['extra', 'toc', 'sane_lists'])
    return html_body

def build_pdf_document(item):
    student = STUDENTS[item["student_id"]]
    src_path = os.path.join(BASE_DIR, item["src"])
    out_pdf = os.path.join(student["folder"], item["pdf_name"])
    
    if not os.path.exists(src_path):
        print(f"Error: source file not found: {src_path}")
        return False
        
    with open(src_path, "r", encoding="utf-8") as f:
        raw_md = f.read()
        
    html_body = process_markdown(raw_md)
    
    full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{item["title"]}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true, theme: 'neutral'}});</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
{CSS_STYLES}
</style>
</head>
<body>

<div class="report-header">
    <div class="report-meta-badge">INFORME TECNICO DE INGENIERIA - PROYECTO BSF MONITOR</div>
    <div class="report-title">{item["title"]}</div>
    <div class="report-subtitle">Sistema de Monitoreo Biologico y Control de Biorreactor para <em>Hermetia illucens</em></div>
    
    <div class="author-card">
        <table class="author-table">
            <tr>
                <td class="author-label">Integrante:</td>
                <td class="author-value"><strong>{student["name"]}</strong></td>
                <td class="author-label">Codigo:</td>
                <td class="author-value"><strong>{student["code"]}</strong></td>
            </tr>
            <tr>
                <td class="author-label">Documento Origen:</td>
                <td class="author-value"><code>{item["src"]}</code></td>
                <td class="author-label">Especialidad:</td>
                <td class="author-value">{student["specialty"]}</td>
            </tr>
        </table>
    </div>
</div>

<div class="document-content">
{html_body}
</div>

</body>
</html>
"""

    temp_html = os.path.join(student["folder"], f"_temp_{os.path.basename(item['src'])}.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--virtual-time-budget=2000",
        f"--print-to-pdf={out_pdf}",
        f"file:///{os.path.abspath(temp_html)}"
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(temp_html):
        try:
            os.remove(temp_html)
        except Exception:
            pass
            
    if os.path.exists(out_pdf) and os.path.getsize(out_pdf) > 0:
        size_kb = os.path.getsize(out_pdf) / 1024
        print(f"[OK] Generado: {item['pdf_name']} ({size_kb:.1f} KB) -> {student['name']}")
        return True
    else:
        print(f"[FAIL] Error generando {item['pdf_name']} (code {res.returncode}): {res.stderr}")
        return False

def main():
    print("Iniciando generacion equitativa de PDFs para los 18 informes tecnicos...")
    for s_id, s_data in STUDENTS.items():
        os.makedirs(s_data["folder"], exist_ok=True)
        print(f"Directorio verificado: {s_data['folder']}")
        
    success_count = 0
    for idx, item in enumerate(ASSIGNMENTS, start=1):
        print(f"[{idx}/18] Procesando {item['src']}...")
        if build_pdf_document(item):
            success_count += 1
            
    print(f"\nFinalizado: {success_count}/18 PDFs generados exitosamente.")

if __name__ == "__main__":
    main()
