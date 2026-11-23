import docx

doc_path = r"C:\Users\Danteeh\.gemini\antigravity\brain\bdf2aa3e-3592-461d-9e64-4229e08555cf\.user_uploaded\media_1795473207225_eff193f6.docx"
doc = docx.Document(doc_path)

print("--- PARAGRAPHS ---")
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        print(f"P{i}: [{p.style.name}] '{p.text}'")

print(f"\n--- TABLES ({len(doc.tables)}) ---")
for t_idx, table in enumerate(doc.tables):
    print(f"\nTable {t_idx} (rows: {len(table.rows)}, cols: {len(table.columns)}):")
    for r_idx, row in enumerate(table.rows):
        cells = [c.text.replace('\n', ' ') for c in row.cells]
        print(f"  R{r_idx}: {cells}")

print("\n--- SECTIONS ---")
for s in doc.sections:
    print(f"Page width: {s.page_width}, height: {s.page_height}, top: {s.top_margin}, bottom: {s.bottom_margin}, left: {s.left_margin}, right: {s.right_margin}")
