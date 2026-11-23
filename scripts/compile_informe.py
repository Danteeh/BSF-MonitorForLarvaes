import os
import subprocess
import markdown

base_dir = r"E:\BSF Moscas\Integrante 2"
md_path = os.path.join(base_dir, "INFORME_ACTIVIDADES_INTEGRANTE_2.md")
pdf_path = os.path.join(base_dir, "INFORME_ACTIVIDADES_INTEGRANTE_2.pdf")
html_path = os.path.join(base_dir, "_temp_informe.html")

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

html_body = markdown.markdown(text, extensions=["extra", "sane_lists"])

css = """
@page {
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    color: #1e293b;
    line-height: 1.5;
    font-size: 8.5pt;
    margin: 0;
    padding: 0;
}
h1, h2, h3 {
    color: #065f46;
    margin-top: 12px;
    margin-bottom: 6px;
    page-break-after: avoid;
}
p {
    margin: 6px 0;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 8pt;
}
tr {
    page-break-inside: avoid;
}
th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
    text-align: left;
    padding: 5px 7px;
    border: 1px solid #cbd5e1;
}
td {
    padding: 4px 7px;
    border: 1px solid #e2e8f0;
    color: #334155;
    vertical-align: top;
}
tr:nth-child(even) td {
    background: #f8fafc;
}
a {
    color: #047857;
    text-decoration: underline;
    font-family: Consolas, monospace;
    font-size: 7.5pt;
}
code {
    font-family: Consolas, monospace;
    font-size: 7.5pt;
    background: #f1f5f9;
    padding: 1px 3px;
    border-radius: 3px;
}
"""

full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Informe de Actividades - Miguel Alejandro Chavez Porras</title>
<style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", f"file:///{html_path}"]
res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(html_path):
    os.remove(html_path)

if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
    print(f"PDF generado exitosamente: {pdf_path} ({os.path.getsize(pdf_path) / 1024:.1f} KB)")
else:
    print(f"Error generando PDF: {res.stderr}")
