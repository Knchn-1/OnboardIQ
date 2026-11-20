import json
with open(r'd:\Projects1\OnboardIQ\output\09_source_extracts\template_inspection_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
it_manual = [f for f in data['files'] if 'IT-policies' in f['filename']][0]
print('IT Manual:')
print(f"  Paragraphs: {it_manual['paragraph_count']}")
print(f"  Tables: {it_manual['table_count']}")
print(f"  Words: {it_manual['word_count']}")
print(f"  Headings: {len(it_manual['heading_list'])}")
print(f"  Section outline entries: {len(it_manual.get('detailed_section_outline', []))}")
print(f"  Foreign refs: {len(it_manual['foreign_references']['foreign_jurisdiction_references'])}")
print(f"  Outdated tech: {len(it_manual['outdated_tech_references'])}")
print()
print('First 20 headings:')
for h in it_manual['heading_list'][:20]:
    print(f'  - {h}')
print(f'  ... ({len(it_manual["heading_list"])} total)')
print()
print('Outdated tech details:')
for t in it_manual['outdated_tech_references']:
    print(f"  - {t['technology']}: {t['mentions']} mentions - {t['matched_text']}")
print()
print('Branding:')
b = it_manual['template_branding']
for k, v in b.items():
    print(f"  {k}: {v}")
