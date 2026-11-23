import os
import re
import sys

BASE_DIR = r"E:\BSF Moscas"

# Regex precisa para detectar verdaderos emojis unicode
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # Emoticonos
    "\U0001F300-\U0001F5FF"  # Simbolos y pictogramas diversos
    "\U0001F680-\U0001F6FF"  # Transporte y mapas
    "\U0001F1E6-\U0001F1FF"  # Banderas e indicadores regionales
    "\U00002700-\U000027BF"  # Dingbats
    "\U0001F900-\U0001F9FF"  # Simbolos y pictogramas complementarios
    "\U0001FA00-\U0001FA6F"  # Simbolos de ajedrez y juegos
    "\U0001FA70-\U0001FAFF"  # Simbolos y pictogramas extendidos
    "\U00002600-\U000026FF"  # Simbolos miscelaneos (caritas, clima, etc)
    "\U0000231A-\U0000231B"  # Relojes
    "\U000023E9-\U000023EC"  # Flechas de reproduccion
    "\U000023F0-\U000023F3"  # Temporizadores
    "\U000025CF"              # Circulo negro relleno
    "]+",
    flags=re.UNICODE
)

PATHS_TO_SCAN = [
    os.path.join(BASE_DIR, "Integrante 1"),
    os.path.join(BASE_DIR, "Integrante 2"),
    os.path.join(BASE_DIR, "scripts"),
    os.path.join(BASE_DIR, "docs"),
    os.path.join(BASE_DIR, "README.md"),
    os.path.join(BASE_DIR, "guia_agente.md")
]

def scan_file(filepath):
    found = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for idx, line in enumerate(f, 1):
                matches = EMOJI_PATTERN.findall(line)
                if matches:
                    found.append((idx, matches, line.strip()))
    except Exception as e:
        print(f"Error leyendo {filepath}: {e}")
    return found

def main():
    print("Iniciando escaneo estricto de emojis en el proyecto...")
    total_violations = 0
    scanned_files = 0
    
    for target in PATHS_TO_SCAN:
        if os.path.isfile(target):
            files = [target]
        elif os.path.isdir(target):
            files = []
            for root, _, filenames in os.walk(target):
                for fn in filenames:
                    if fn.endswith((".md", ".py", ".ts", ".tsx", ".js", ".json", ".html", ".css", ".txt")):
                        files.append(os.path.join(root, fn))
        else:
            continue
            
        for filepath in files:
            scanned_files += 1
            violations = scan_file(filepath)
            if violations:
                print(f"\n[ALERTA] Emojis detectados en: {filepath}")
                for line_num, emojis, content in violations:
                    print(f"  Linea {line_num}: {emojis} -> {content[:80]}")
                total_violations += len(violations)
                
    print(f"\nEscaneo finalizado:")
    print(f"- Archivos analizados: {scanned_files}")
    print(f"- Violaciones de emojis encontradas: {total_violations}")
    
    if total_violations == 0:
        print("[EXITO] Cero emojis detectados. Cumplimiento del 100%.")
        sys.exit(0)
    else:
        print("[FALLO] Se encontraron emojis que deben ser eliminados.")
        sys.exit(1)

if __name__ == "__main__":
    main()
