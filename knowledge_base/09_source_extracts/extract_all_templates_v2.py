"""
Enhanced extraction: fix topic detection and add deeper IT manual analysis.
"""
import json
import re
import os
from docx import Document

SOURCE_DIR = r"d:\Projects1\OnboardIQ\source"
OUTPUT_DIR = r"d:\Projects1\OnboardIQ\output\09_source_extracts"

def extract_docx_info(filepath):
    filename = os.path.basename(filepath)
    doc = Document(filepath)
    
    paragraphs = []
    headings = []
    all_text = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        style_name = para.style.name if para.style else "Normal"
        if text:
            paragraphs.append({"style": style_name, "text": text})
            all_text.append(text)
        if style_name and ("Heading" in style_name or "heading" in style_name or "Title" in style_name or "title" in style_name or "TOC" in style_name):
            if text:
                headings.append({"level": style_name, "text": text})
    
    # Also check for lines that look like headings by formatting (all caps, short, etc.)
    # but only add if no style-based headings were found
    if not headings:
        for p in paragraphs:
            t = p["text"]
            if len(t) < 80 and (t.isupper() or t.endswith(':')):
                headings.append({"level": "Implicit", "text": t})
    
    # Extract tables
    table_data = []
    table_text_words = []
    for tidx, table in enumerate(doc.tables):
        rows_data = []
        for row in table.rows:
            row_cells = []
            for cell in row.cells:
                cell_text = cell.text.strip()
                row_cells.append(cell_text)
                if cell_text:
                    table_text_words.extend(cell_text.split())
            rows_data.append(row_cells)
        table_data.append({
            "table_index": tidx,
            "row_count": len(rows_data),
            "col_count": len(rows_data[0]) if rows_data else 0,
            "headers": rows_data[0] if rows_data else [],
            "sample_rows": rows_data[1:4] if len(rows_data) > 1 else []
        })
    
    full_text = "\n".join(all_text)
    word_count = len(full_text.split()) + len(table_text_words)
    
    actual_topic = detect_topic(full_text, headings, filename)
    key_policy_values = extract_policy_values(full_text)
    foreign_refs = extract_foreign_references(full_text)
    branding = extract_branding(full_text)
    outdated_tech = extract_outdated_tech(full_text)
    content_summary = generate_summary(full_text, headings, filename, actual_topic)
    
    result = {
        "filename": filename,
        "file_size_bytes": os.path.getsize(filepath),
        "actual_topic": actual_topic,
        "heading_list": [h["text"] for h in headings],
        "heading_details": headings,
        "paragraph_count": len(paragraphs),
        "table_count": len(doc.tables),
        "table_details": table_data,
        "word_count": word_count,
        "key_policy_values": key_policy_values,
        "foreign_references": foreign_refs,
        "template_branding": branding,
        "outdated_tech_references": outdated_tech,
        "content_summary": content_summary,
        "all_paragraph_styles": list(set(p["style"] for p in paragraphs)),
    }
    
    # For IT manual, add detailed section outline
    if "IT-policies" in filename:
        result["detailed_section_outline"] = extract_it_manual_outline(doc, paragraphs, headings)
    
    # For project spec, fix topic
    if "OnboardIQ_Project" in filename:
        result["actual_topic"] = "Project Master Specification (OnboardIQ)"
    
    return result

def detect_topic(text, headings, filename):
    """Better topic detection using filename as primary signal + content validation."""
    fname_lower = filename.lower()
    text_lower = text.lower()
    
    # Direct filename-to-topic mapping (more reliable than pure content analysis)
    filename_map = {
        "attendance": "Attendance Policy",
        "code-of-conduct": "Code of Conduct",
        "employee-handbook": "Employee Handbook",
        "employee-referral": "Employee Referral Policy",
        "expense-reimbursement": "Expense Reimbursement Policy",
        "hr-policy-manual": "HR Policy Manual",
        "information-security": "Information Security Policy",
        "it-acceptable-use": "IT Acceptable Use Policy",
        "it-policies-and-procedures": "IT Policies and Procedures Manual",
        "laptop-usage": "Laptop Usage Policy",
        "leave-policy": "Leave Policy",
        "onboarding": "Onboarding Policy",
        "overtime": "Overtime Policy",
        "promotion": "Promotion Policy",
        "remote-work": "Remote Work Policy",
        "salary-administration": "Salary Administration Policy",
        "shift-work": "Shift Work Policy",
        "training-development": "Training and Development Policy",
        "travel-policy": "Travel Policy",
        "work-from-home": "Work from Home Policy",
        "working-hours": "Working Hours Policy",
        "northstar": "Company Overview and Employee Directory",
        "onboardiq_project": "Project Master Specification (OnboardIQ)",
    }
    
    for key, topic in filename_map.items():
        if key in fname_lower:
            return topic
    
    # Fallback: content-based detection
    # Check first 500 chars and headings for topic clues
    heading_text = " ".join(h["text"] for h in headings).lower()
    first_text = text_lower[:1000]
    
    content_topics = [
        ("Attendance Policy", ["attendance policy", "attendance management"]),
        ("Code of Conduct", ["code of conduct", "professional conduct"]),
        ("Employee Handbook", ["employee handbook"]),
        ("Leave Policy", ["leave policy", "annual leave"]),
        ("IT Policies and Procedures Manual", ["it policies", "it procedures manual"]),
        ("Remote Work Policy", ["remote work policy"]),
        ("Working Hours Policy", ["working hours policy"]),
    ]
    
    for topic, keywords in content_topics:
        for kw in keywords:
            if kw in first_text or kw in heading_text:
                return topic
    
    return "Unknown Policy Document"

def extract_it_manual_outline(doc, paragraphs, headings):
    """Detailed section outline for the large IT manual."""
    outline = []
    current_section = None
    
    for p in paragraphs:
        style = p["style"]
        text = p["text"]
        
        if "Heading" in style or "Title" in style:
            level = 0
            if "1" in style:
                level = 1
            elif "2" in style:
                level = 2
            elif "3" in style:
                level = 3
            elif "Title" in style:
                level = 0
            
            outline.append({
                "level": level,
                "style": style,
                "title": text,
            })
    
    return outline

def extract_policy_values(text):
    values = []
    
    # Find numbers with context (e.g. "30 days", "Rs. 5,000", "90%")
    # Days
    for m in re.finditer(r'(\d+)\s*(?:calendar\s+|working\s+|business\s+)?days?', text, re.IGNORECASE):
        context_start = max(0, m.start() - 40)
        context = text[context_start:m.end() + 20].strip()
        values.append({"value": m.group(0), "context": context})
    
    # Currency amounts
    for m in re.finditer(r'(?:Rs\.?|INR|₹|\$|USD)\s*[\d,]+(?:\.\d+)?', text, re.IGNORECASE):
        context_start = max(0, m.start() - 40)
        context = text[context_start:m.end() + 20].strip()
        values.append({"value": m.group(0), "context": context})
    
    # Percentages
    for m in re.finditer(r'\d+(?:\.\d+)?\s*%', text):
        context_start = max(0, m.start() - 40)
        context = text[context_start:m.end() + 20].strip()
        values.append({"value": m.group(0), "context": context})
    
    # Hours
    for m in re.finditer(r'(\d+)\s*hours?', text, re.IGNORECASE):
        context_start = max(0, m.start() - 40)
        context = text[context_start:m.end() + 20].strip()
        values.append({"value": m.group(0), "context": context})
    
    # Deduplicate by value
    seen = set()
    deduped = []
    for v in values:
        if v["value"] not in seen:
            seen.add(v["value"])
            deduped.append(v)
    
    return deduped

def extract_foreign_references(text):
    foreign_refs = []
    
    foreign_patterns = [
        (r'(?:United States|U\.S\.|USA|American)\s+(?:law|regulation|statute|act)', "US law reference"),
        (r'(?:UK|United Kingdom|British|English)\s+(?:law|regulation|statute|act)', "UK law reference"),
        (r'GDPR', "GDPR (EU)"),
        (r'(?:European Union|EU)\s+(?:law|regulation|directive)', "EU law reference"),
        (r'FLSA|Fair Labor Standards Act', "US FLSA"),
        (r'FMLA|Family and Medical Leave Act', "US FMLA"),
        (r'SOX|Sarbanes.Oxley', "US SOX"),
        (r'HIPAA', "US HIPAA"),
        (r'ADA|Americans with Disabilities', "US ADA"),
        (r'EEOC', "US EEOC"),
        (r'OSHA', "US OSHA"),
        (r'at.will employment', "US at-will employment concept"),
        (r'Title VII', "US Title VII"),
        (r'(?:state law|federal law|state and federal)', "US state/federal law reference"),
        (r'Department of Labor', "US Dept of Labor"),
        (r'(?<!Section\s)IRS(?!\s+Act)', "US IRS"),
        (r'401\(?k\)?', "US 401(k)"),
        (r'COBRA', "US COBRA"),
        (r'Workers.?\s*Compensation', "Workers Compensation (US concept)"),
        (r'Employment Standards Act', "Canadian ESA"),
        (r'PCI\s*DSS', "PCI DSS"),
        (r'SOC\s*2', "SOC 2"),
        (r'ISO\s*27001', "ISO 27001"),
        (r'NIST', "NIST (US)"),
        (r'CAN-SPAM', "US CAN-SPAM"),
        (r'CCPA', "US CCPA"),
        (r'FERPA', "US FERPA"),
    ]
    
    for pattern, label in foreign_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            foreign_refs.append({"type": label, "matches": list(set(matches)), "count": len(matches)})
    
    # Indian law references
    indian_refs = []
    indian_patterns = [
        (r'Factories Act', "Factories Act"),
        (r'Shops and Establishments', "Shops and Establishments Act"),
        (r'Payment of Wages', "Payment of Wages Act"),
        (r'Minimum Wages Act', "Minimum Wages Act"),
        (r'Industrial Disputes', "Industrial Disputes Act"),
        (r'(?:PF Act|Provident Fund)', "Provident Fund Act"),
        (r'ESI Act', "ESI Act"),
        (r'(?:Payment of )?Gratuity Act', "Payment of Gratuity Act"),
        (r'Maternity Benefit Act', "Maternity Benefit Act"),
        (r'(?:Sexual Harassment|POSH)', "POSH Act"),
        (r'IT Act.*?(?:India|2000)', "IT Act (India)"),
        (r'Indian Penal', "Indian Penal Code"),
        (r'Companies Act.*?(?:India|2013)', "Companies Act (India)"),
        (r'Income Tax Act', "Income Tax Act"),
        (r'(?:Labor|Labour) Code', "Labour Code"),
        (r'Contract Act', "Contract Act"),
        (r'Information Technology Act', "IT Act (India)"),
    ]
    
    for pattern, label in indian_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            indian_refs.append({"type": label, "count": len(matches)})
    
    return {
        "foreign_jurisdiction_references": foreign_refs,
        "indian_law_references": indian_refs,
    }

def extract_branding(text):
    branding = {}
    
    # BetterJobs mentions
    bj = re.findall(r'BetterJobs', text)
    if bj:
        branding["BetterJobs_mentions"] = len(bj)
    
    # All bracket placeholders
    all_brackets = re.findall(r'\[[^\]]{2,50}\]', text)
    if all_brackets:
        branding["all_placeholders"] = list(set(all_brackets))
        branding["placeholder_count"] = len(all_brackets)
    
    # Company Name variants
    cn = [b for b in all_brackets if 'company' in b.lower() or 'organization' in b.lower() or 'employer' in b.lower()]
    if cn:
        branding["company_name_placeholders"] = len(cn)
        branding["company_name_variants"] = list(set(cn))
    
    # Insert placeholders
    inserts = [b for b in all_brackets if 'insert' in b.lower()]
    if inserts:
        branding["insert_placeholders"] = list(set(inserts))
    
    # Date placeholders
    dates = [b for b in all_brackets if 'date' in b.lower()]
    if dates:
        branding["date_placeholders"] = list(set(dates))
    
    # Specific template brand names
    template_brands = re.findall(r'(?:TemplateLab|Template\.net|BetterTeam|Betterteam|Workable|SHRM|Indeed)', text, re.IGNORECASE)
    if template_brands:
        branding["third_party_template_brands"] = list(set(template_brands))
    
    return branding

def extract_outdated_tech(text):
    outdated = []
    patterns = {
        "fax machine/fax": r'\bfax(?:es|ing)?\b',
        "floppy disk": r'floppy',
        "CD-ROM/DVD": r'\b(?:CD-ROM|DVD|optical disc|optical disk)\b',
        "dial-up": r'dial.up',
        "pager/beeper": r'\b(?:pager|beeper)\b',
        "BlackBerry": r'BlackBerry',
        "Windows XP/Vista/7": r'Windows\s+(?:XP|Vista|7\b)',
        "Internet Explorer": r'Internet Explorer',
        "Lotus Notes": r'Lotus Notes',
        "tape backup": r'tape\s+backup',
        "PDA": r'\bPDA\b',
        "typewriter": r'typewriter',
        "telex": r'\btelex\b',
        "magnetic media": r'magnetic\s+(?:media|tape|disk)',
        "zip drive": r'zip\s+drive',
        "USB/pen/flash drive": r'\b(?:USB\s+drive|thumb\s+drive|pen\s+drive|flash\s+drive)\b',
        "modem": r'\bmodem\b',
        "Telnet": r'\btelnet\b',
        "FTP (unencrypted)": r'\bFTP\b(?!\s*S)',
    }
    
    for tech, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            outdated.append({"technology": tech, "mentions": len(matches), "matched_text": list(set(m.strip() for m in matches))[:3]})
    
    return outdated

def generate_summary(text, headings, filename, topic):
    heading_list = [h["text"] for h in headings[:8]]
    heading_str = ", ".join(heading_list) if heading_list else "no clearly styled section headings"
    word_count = len(text.split())
    
    # Get first substantive paragraph
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 30]
    first_content = lines[0][:150] + "..." if lines else ""
    
    summary = f"Document covering '{topic}' with sections including: {heading_str}. "
    summary += f"Contains approximately {word_count} words in body text. "
    
    if "BetterJobs" in text:
        summary += "Uses BetterJobs template branding requiring replacement with actual company identity."
    elif "[Company Name]" in text or "[company name]" in text.lower():
        summary += "Contains placeholder text requiring organization-specific customization."
    else:
        summary += f"Opening content: '{first_content}'"
    
    return summary

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    docx_files = sorted([f for f in os.listdir(SOURCE_DIR) if f.endswith('.docx')])
    print(f"Found {len(docx_files)} DOCX files to process.")
    
    results = []
    errors = []
    
    for i, fname in enumerate(docx_files):
        filepath = os.path.join(SOURCE_DIR, fname)
        print(f"[{i+1}/{len(docx_files)}] Processing: {fname}")
        try:
            info = extract_docx_info(filepath)
            results.append(info)
            print(f"  -> OK: {info['paragraph_count']} paras, {info['table_count']} tables, {info['word_count']} words")
            print(f"     Topic: {info['actual_topic']}")
            print(f"     Headings: {len(info['heading_list'])}")
            if info.get('template_branding', {}).get('BetterJobs_mentions'):
                print(f"     BetterJobs mentions: {info['template_branding']['BetterJobs_mentions']}")
            fr = info.get('foreign_references', {}).get('foreign_jurisdiction_references', [])
            if fr:
                print(f"     Foreign refs: {[r['type'] for r in fr]}")
            ot = info.get('outdated_tech_references', [])
            if ot:
                print(f"     Outdated tech: {[t['technology'] for t in ot]}")
        except Exception as e:
            import traceback
            error_msg = f"Error processing {fname}: {traceback.format_exc()}"
            print(f"  -> ERROR: {error_msg}")
            errors.append(error_msg)
            results.append({"filename": fname, "error": str(e)})
    
    # Write JSON
    output_json = os.path.join(OUTPUT_DIR, "template_inspection_results.json")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump({
            "extraction_metadata": {
                "total_files_processed": len(docx_files),
                "successful": len([r for r in results if "error" not in r]),
                "errors": len(errors),
                "source_directory": SOURCE_DIR,
            },
            "files": results,
            "errors": errors,
        }, f, indent=2, ensure_ascii=False)
    print(f"\nJSON written to: {output_json}")
    
    # Write markdown summary
    write_markdown_summary(results, errors, docx_files)

def write_markdown_summary(results, errors, docx_files):
    output_md = os.path.join(OUTPUT_DIR, "template_inspection_summary.md")
    
    L = []
    L.append("# Template Document Inspection Summary\n")
    L.append(f"**Total files processed:** {len(docx_files)}  ")
    L.append(f"**Successful:** {len([r for r in results if 'error' not in r])}  ")
    L.append(f"**Errors:** {len(errors)}\n")
    
    # Overview table
    L.append("## 1. File Overview\n")
    L.append("| # | Filename | Detected Topic | ¶ | Tables | Words | Size (KB) |")
    L.append("|---|---------|---------------|---|--------|-------|-----------|")
    total_words = 0
    total_paras = 0
    total_tables = 0
    for i, r in enumerate(results):
        if "error" in r:
            L.append(f"| {i+1} | {r['filename']} | ⚠️ ERROR | - | - | - | - |")
        else:
            size_kb = r.get('file_size_bytes', 0) / 1024
            L.append(f"| {i+1} | {r['filename']} | {r['actual_topic']} | {r['paragraph_count']} | {r['table_count']} | {r['word_count']} | {size_kb:.1f} |")
            total_words += r['word_count']
            total_paras += r['paragraph_count']
            total_tables += r['table_count']
    L.append(f"| | **TOTALS** | | **{total_paras}** | **{total_tables}** | **{total_words}** | |")
    L.append("")
    
    # Branding analysis
    L.append("## 2. Template Branding Analysis\n")
    L.append("| Filename | BetterJobs Mentions | Total Placeholders | Placeholder Examples |")
    L.append("|----------|-------------------:|-------------------:|---------------------|")
    for r in results:
        if "error" in r: continue
        b = r.get("template_branding", {})
        bj = b.get("BetterJobs_mentions", 0)
        pc = b.get("placeholder_count", 0)
        examples = b.get("all_placeholders", [])[:5]
        ex_str = ", ".join(examples) if examples else "-"
        L.append(f"| {r['filename']} | {bj} | {pc} | {ex_str} |")
    L.append("")
    
    # Foreign references
    L.append("## 3. Foreign Legal/Jurisdiction References (Non-Indian)\n")
    has_foreign = False
    for r in results:
        if "error" in r: continue
        fr = r.get("foreign_references", {}).get("foreign_jurisdiction_references", [])
        if fr:
            has_foreign = True
            L.append(f"### {r['filename']}")
            for ref in fr:
                L.append(f"- **{ref['type']}**: {', '.join(ref['matches'])} ({ref['count']} occurrence(s))")
            L.append("")
    if not has_foreign:
        L.append("✅ No foreign legal references found in any document.\n")
    
    # Indian law references
    L.append("## 4. Indian Law References\n")
    has_indian = False
    for r in results:
        if "error" in r: continue
        ir = r.get("foreign_references", {}).get("indian_law_references", [])
        if ir:
            has_indian = True
            L.append(f"### {r['filename']}")
            for ref in ir:
                L.append(f"- {ref['type']} ({ref['count']} occurrence(s))")
            L.append("")
    if not has_indian:
        L.append("No Indian law references found.\n")
    
    # Outdated tech
    L.append("## 5. Outdated Technology References\n")
    has_outdated = False
    for r in results:
        if "error" in r: continue
        ot = r.get("outdated_tech_references", [])
        if ot:
            has_outdated = True
            L.append(f"### {r['filename']}")
            for t in ot:
                L.append(f"- **{t['technology']}**: {t['mentions']} mention(s) — e.g., {', '.join(t['matched_text'])}")
            L.append("")
    if not has_outdated:
        L.append("✅ No outdated technology references found.\n")
    
    # Key policy values
    L.append("## 6. Key Policy Values and Thresholds\n")
    for r in results:
        if "error" in r: continue
        kpv = r.get("key_policy_values", [])
        if kpv:
            L.append(f"### {r['filename']} ({r['actual_topic']})")
            for v in kpv[:20]:
                L.append(f"- **{v['value']}** — _{v['context']}_")
            if len(kpv) > 20:
                L.append(f"- ... and {len(kpv) - 20} more values")
            L.append("")
    
    # Section headings
    L.append("## 7. Document Section Outlines\n")
    for r in results:
        if "error" in r: continue
        L.append(f"### {r['filename']}")
        hl = r.get("heading_list", [])
        hd = r.get("heading_details", [])
        if hd:
            for h in hd:
                indent = ""
                if "2" in h.get("level", ""):
                    indent = "  "
                elif "3" in h.get("level", ""):
                    indent = "    "
                elif "4" in h.get("level", ""):
                    indent = "      "
                L.append(f"{indent}- [{h['level']}] {h['text']}")
        else:
            L.append("- _(No headings detected)_")
        L.append("")
    
    # IT Manual detailed outline
    for r in results:
        if r.get("detailed_section_outline"):
            L.append("## 8. IT Manual Detailed Section Outline\n")
            for s in r["detailed_section_outline"]:
                indent = "  " * s["level"]
                L.append(f"{indent}- **[{s['style']}]** {s['title']}")
            L.append("")
    
    # Errors
    if errors:
        L.append("## Errors\n")
        for e in errors:
            L.append(f"- {e}")
        L.append("")
    
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write("\n".join(L))
    print(f"Markdown written to: {output_md}")

if __name__ == "__main__":
    main()
