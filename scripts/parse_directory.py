"""Parse the Northstar Company Overview & Employee Directory DOCX."""
import docx
import json
import os

doc = docx.Document('source/Northstar_Company_Overview_Employee_Directory.docx')

# 1. Element census
census = {
    'paragraphs': len(doc.paragraphs),
    'tables': len(doc.tables),
    'sections': len(doc.sections),
    'core_properties': {},
    'styles_count': len(doc.styles),
}

cp = doc.core_properties
for attr in ['author', 'title', 'subject', 'category', 'comments', 'created', 'modified', 'last_modified_by', 'revision']:
    val = getattr(cp, attr, None)
    census['core_properties'][attr] = str(val) if val else None

# 2. Extract all paragraphs with style
paras = []
for i, p in enumerate(doc.paragraphs):
    paras.append({
        'index': i,
        'text': p.text,
        'style': p.style.name if p.style else None,
        'level': p.style.name if p.style and 'Heading' in p.style.name else None
    })

# 3. Extract all tables
tables_data = []
for ti, table in enumerate(doc.tables):
    rows = []
    for ri, row in enumerate(table.rows):
        cells = [cell.text.strip() for cell in row.cells]
        rows.append(cells)
    tables_data.append({
        'table_index': ti,
        'row_count': len(rows),
        'col_count': len(rows[0]) if rows else 0,
        'rows': rows
    })

print(json.dumps(census, indent=2))
print(f"\nParagraphs extracted: {len(paras)}")
print(f"Tables extracted: {len(tables_data)}")
for t in tables_data:
    idx = t["table_index"]
    rc = t["row_count"]
    cc = t["col_count"]
    print(f"  Table {idx}: {rc} rows x {cc} cols")
    if t['rows']:
        print(f"    Header: {t['rows'][0]}")

# Save extractions
os.makedirs('output/09_source_extracts', exist_ok=True)
with open('output/09_source_extracts/directory_paragraphs.json', 'w', encoding='utf-8') as f:
    json.dump(paras, f, indent=2, ensure_ascii=False)
with open('output/09_source_extracts/directory_tables.json', 'w', encoding='utf-8') as f:
    json.dump(tables_data, f, indent=2, ensure_ascii=False)
with open('output/09_source_extracts/directory_census.json', 'w', encoding='utf-8') as f:
    json.dump(census, f, indent=2, ensure_ascii=False)

print("\nDirectory extraction complete.")

