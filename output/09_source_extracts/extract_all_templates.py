"""
Extract structured information from all DOCX template files in source directory.
"""
import json
import re
import os
from docx import Document

SOURCE_DIR = r"d:\Projects1\OnboardIQ\source"
OUTPUT_DIR = r"d:\Projects1\OnboardIQ\output\09_source_extracts"

def extract_docx_info(filepath):
    """Extract comprehensive information from a single DOCX file."""
    filename = os.path.basename(filepath)
    doc = Document(filepath)
    
    # Extract all paragraphs with styles
    paragraphs = []
    headings = []
    all_text = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        style_name = para.style.name if para.style else "Normal"
        if text:
            paragraphs.append({"style": style_name, "text": text})
            all_text.append(text)
        if style_name and ("Heading" in style_name or "heading" in style_name or "Title" in style_name or "title" in style_name):
            if text:
                headings.append({"level": style_name, "text": text})
    
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
        table_data.append({"table_index": tidx, "row_count": len(rows_data), "col_count": len(rows_data[0]) if rows_data else 0, "headers": rows_data[0] if rows_data else [], "sample_rows": rows_data[1:4] if len(rows_data) > 1 else []})
    
    # Full text for analysis
    full_text = "\n".join(all_text)
    word_count = len(full_text.split()) + len(table_text_words)
    
    # Detect actual topic from content
    actual_topic = detect_topic(full_text, headings, filename)
    
    # Key policy values - thresholds, amounts, days, percentages
    key_policy_values = extract_policy_values(full_text)
    
    # Foreign references (non-Indian jurisdictions)
    foreign_refs = extract_foreign_references(full_text)
    
    # Template branding
    branding = extract_branding(full_text)
    
    # Outdated tech references
    outdated_tech = extract_outdated_tech(full_text)
    
    # Content summary
    content_summary = generate_summary(full_text, headings, filename, actual_topic)
    
    return {
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

def detect_topic(text, headings, filename):
    """Detect the actual topic of the document based on content."""
    text_lower = text.lower()
    heading_texts = " ".join(h["text"].lower() for h in headings)
    combined = text_lower + " " + heading_texts
    
    topic_keywords = {
        "Attendance Policy": ["attendance", "punctuality", "tardiness", "absenteeism"],
        "Code of Conduct": ["code of conduct", "ethical", "workplace behavior", "professional conduct"],
        "Employee Handbook": ["employee handbook", "handbook", "employment relationship"],
        "Employee Referral Policy": ["referral", "refer a candidate", "referral bonus"],
        "Expense Reimbursement Policy": ["expense reimbursement", "reimbursement", "expense claim"],
        "HR Policy Manual": ["human resource", "hr policy", "hr manual"],
        "Information Security Policy": ["information security", "data protection", "cybersecurity", "data security"],
        "IT Acceptable Use Policy": ["acceptable use", "it resources", "it acceptable"],
        "IT Policies and Procedures Manual": ["it policies", "it procedures", "it manual", "disaster recovery", "change management", "it governance"],
        "Laptop Usage Policy": ["laptop", "laptop usage", "company laptop"],
        "Leave Policy": ["leave policy", "annual leave", "sick leave", "casual leave", "maternity leave"],
        "Onboarding Policy": ["onboarding", "new employee", "orientation", "induction"],
        "Overtime Policy": ["overtime", "extra hours", "overtime compensation"],
        "Promotion Policy": ["promotion", "career advancement", "career growth"],
        "Remote Work Policy": ["remote work", "remote working", "telecommuting"],
        "Salary Administration Policy": ["salary", "compensation", "pay structure", "salary administration"],
        "Shift Work Policy": ["shift work", "shift schedule", "rotating shift"],
        "Training and Development Policy": ["training", "development", "learning", "skill development"],
        "Travel Policy": ["travel", "business travel", "travel expense"],
        "Work from Home Policy": ["work from home", "wfh", "home office"],
        "Working Hours Policy": ["working hours", "work hours", "office hours", "work schedule"],
        "Company Overview and Employee Directory": ["company overview", "employee directory", "department", "organizational"],
        "Project Specification": ["project specification", "master specification", "onboardiq", "project scope"],
    }
    
    best_topic = "Unknown"
    best_score = 0
    for topic, keywords in topic_keywords.items():
        score = sum(1 for kw in keywords if kw in combined)
        if score > best_score:
            best_score = score
            best_topic = topic
    
    return best_topic

def extract_policy_values(text):
    """Extract key policy values like thresholds, amounts, days, percentages."""
    values = []
    
    # Days patterns
    day_patterns = re.findall(r'(\d+)\s*(?:calendar\s+|working\s+|business\s+)?days?', text, re.IGNORECASE)
    for d in day_patterns:
        values.append(f"{d} days")
    
    # Currency/amounts
    amount_patterns = re.findall(r'(?:Rs\.?|INR|₹|\$|USD)\s*[\d,]+(?:\.\d+)?', text, re.IGNORECASE)
    for a in amount_patterns:
        values.append(a.strip())
    
    # Percentages
    pct_patterns = re.findall(r'\d+(?:\.\d+)?\s*%', text)
    for p in pct_patterns:
        values.append(p.strip())
    
    # Hours
    hour_patterns = re.findall(r'(\d+)\s*hours?', text, re.IGNORECASE)
    for h in hour_patterns:
        values.append(f"{h} hours")
    
    # Specific thresholds with context
    contextual = re.findall(r'(?:minimum|maximum|at least|up to|not exceed|within|after)\s+(\d+[\d,]*(?:\.\d+)?)\s*(?:days?|hours?|weeks?|months?|years?|%|rupees|dollars?)?', text, re.IGNORECASE)
    for c in contextual:
        if c not in [v.split()[0] for v in values]:
            values.append(f"threshold: {c}")
    
    # Deduplicate
    return list(dict.fromkeys(values))

def extract_foreign_references(text):
    """Find references to non-Indian legal jurisdictions or laws."""
    foreign_refs = []
    
    foreign_patterns = [
        r'(?:United States|U\.S\.|USA|American)\s+(?:law|regulation|statute|act)',
        r'(?:UK|United Kingdom|British|English)\s+(?:law|regulation|statute|act)',
        r'(?:European|EU|GDPR)',
        r'(?:Australian|Canada|Canadian)',
        r'(?:FLSA|Fair Labor Standards Act)',
        r'(?:FMLA|Family and Medical Leave Act)',
        r'(?:SOX|Sarbanes.Oxley)',
        r'(?:HIPAA)',
        r'(?:ADA|Americans with Disabilities)',
        r'(?:EEOC)',
        r'(?:OSHA)',
        r'(?:at-will employment)',
        r'(?:Title VII)',
        r'(?:state law|federal law|state and federal)',
        r'(?:Department of Labor)',
        r'(?:IRS)',
        r'(?:401\(k\)|401k)',
        r'(?:Social Security Act)',
        r'(?:Workers.? Compensation)',
        r'(?:COBRA)',
        r'(?:Employment Standards Act)',
        r'(?:tribunal)',
        r'(?:arbitration)',
    ]
    
    for pattern in foreign_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            foreign_refs.extend(matches)
    
    # Also check for specific non-Indian jurisdiction mentions
    jurisdiction_patterns = re.findall(r'(?:governed by|subject to|in accordance with|comply with|compliant with)\s+(?:the\s+)?([^.]+?)(?:\.|$)', text, re.IGNORECASE)
    for j in jurisdiction_patterns:
        j_lower = j.lower()
        # Flag if it mentions non-Indian jurisdictions
        if any(term in j_lower for term in ['federal', 'state law', 'u.s.', 'usa', 'uk', 'european', 'gdpr']):
            foreign_refs.append(j.strip())
    
    # Indian law references (for context, not flagged as foreign)
    indian_refs = re.findall(r'(?:Factories Act|Shops and Establishments|Payment of Wages|Minimum Wages Act|Industrial Disputes|PF Act|ESI Act|Gratuity Act|Maternity Benefit Act|Sexual Harassment|POSH|IT Act.*India|Indian Penal|Companies Act.*India)', text, re.IGNORECASE)
    
    return {
        "foreign_jurisdiction_references": list(dict.fromkeys(foreign_refs)),
        "indian_law_references": list(dict.fromkeys(indian_refs)),
    }

def extract_branding(text):
    """Find template branding like BetterJobs, Company Name placeholders, etc."""
    branding = {}
    
    # BetterJobs mentions
    bj = re.findall(r'BetterJobs', text)
    if bj:
        branding["BetterJobs_mentions"] = len(bj)
    
    # Company Name placeholders
    cn = re.findall(r'\[Company Name\]|\[Company\]|\[Organization Name\]|\[Employer Name\]', text, re.IGNORECASE)
    if cn:
        branding["company_name_placeholders"] = len(cn)
        branding["company_name_placeholder_variants"] = list(set(cn))
    
    # Insert placeholders
    inserts = re.findall(r'\[Insert[^\]]*\]', text, re.IGNORECASE)
    if inserts:
        branding["insert_placeholders"] = list(set(inserts))
    
    # Date placeholders
    dates = re.findall(r'\[Date\]|\[Effective Date\]|\[Start Date\]', text, re.IGNORECASE)
    if dates:
        branding["date_placeholders"] = list(set(dates))
    
    # Other bracket placeholders
    other_brackets = re.findall(r'\[[A-Z][^\]]{2,30}\]', text)
    filtered = [b for b in other_brackets if b not in (['[Company Name]', '[Insert]', '[Date]'])]
    if filtered:
        branding["other_placeholders"] = list(set(filtered))
    
    # Logo/image references
    logos = re.findall(r'(?:logo|company logo|brand)', text, re.IGNORECASE)
    if logos:
        branding["logo_references"] = len(logos)
    
    return branding

def extract_outdated_tech(text):
    """Find references to potentially outdated technology."""
    outdated = []
    
    patterns = {
        "fax": r'\bfax\b',
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
        "Rolodex": r'Rolodex',
        "typewriter": r'typewriter',
        "telex": r'\btelex\b',
        "magnetic media": r'magnetic\s+(?:media|tape|disk)',
        "zip drive": r'zip\s+drive',
        "USB drive/thumb drive": r'\b(?:USB\s+drive|thumb\s+drive|pen\s+drive|flash\s+drive)\b',
        "modem": r'\bmodem\b',
    }
    
    for tech, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            outdated.append({"technology": tech, "mentions": len(matches)})
    
    return outdated

def generate_summary(text, headings, filename, topic):
    """Generate a brief 2-3 sentence summary of the document."""
    # Get first few meaningful paragraphs
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 20]
    
    heading_list = [h["text"] for h in headings[:8]]
    heading_str = ", ".join(heading_list) if heading_list else "no clear section headings"
    
    word_count = len(text.split())
    
    summary = f"This document covers {topic} with sections on {heading_str}. "
    summary += f"It contains approximately {word_count} words. "
    
    if "BetterJobs" in text:
        summary += "The document is branded as a BetterJobs template requiring customization."
    elif "[Company Name]" in text:
        summary += "The document uses placeholder text requiring organization-specific customization."
    
    return summary

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get all DOCX files
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
            print(f"  -> OK: {info['paragraph_count']} paragraphs, {info['table_count']} tables, {info['word_count']} words, topic: {info['actual_topic']}")
        except Exception as e:
            error_msg = f"Error processing {fname}: {str(e)}"
            print(f"  -> ERROR: {error_msg}")
            errors.append(error_msg)
            results.append({"filename": fname, "error": str(e)})
    
    # Write JSON results
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
    
    print(f"\nJSON results written to: {output_json}")
    
    # Write markdown summary
    write_markdown_summary(results, errors, docx_files)

def write_markdown_summary(results, errors, docx_files):
    output_md = os.path.join(OUTPUT_DIR, "template_inspection_summary.md")
    
    lines = []
    lines.append("# Template Document Inspection Summary")
    lines.append("")
    lines.append(f"**Total files processed:** {len(docx_files)}")
    lines.append(f"**Successful extractions:** {len([r for r in results if 'error' not in r])}")
    lines.append(f"**Errors:** {len(errors)}")
    lines.append("")
    
    # Overview table
    lines.append("## File Overview")
    lines.append("")
    lines.append("| # | Filename | Topic | Paragraphs | Tables | Words | Size |")
    lines.append("|---|---------|-------|------------|--------|-------|------|")
    for i, r in enumerate(results):
        if "error" in r:
            lines.append(f"| {i+1} | {r['filename']} | ERROR | - | - | - | - |")
        else:
            size_kb = r.get('file_size_bytes', 0) / 1024
            lines.append(f"| {i+1} | {r['filename']} | {r['actual_topic']} | {r['paragraph_count']} | {r['table_count']} | {r['word_count']} | {size_kb:.1f} KB |")
    lines.append("")
    
    # Branding analysis
    lines.append("## Template Branding Analysis")
    lines.append("")
    lines.append("| Filename | BetterJobs Mentions | Placeholders | Insert Tags |")
    lines.append("|----------|-------------------|--------------|-------------|")
    for r in results:
        if "error" in r:
            continue
        b = r.get("template_branding", {})
        bj = b.get("BetterJobs_mentions", 0)
        cn = b.get("company_name_placeholders", 0)
        ins = len(b.get("insert_placeholders", []))
        lines.append(f"| {r['filename']} | {bj} | {cn} | {ins} |")
    lines.append("")
    
    # Foreign references
    lines.append("## Foreign Legal References (Non-Indian)")
    lines.append("")
    has_foreign = False
    for r in results:
        if "error" in r:
            continue
        fr = r.get("foreign_references", {}).get("foreign_jurisdiction_references", [])
        if fr:
            has_foreign = True
            lines.append(f"### {r['filename']}")
            for ref in fr:
                lines.append(f"- {ref}")
            lines.append("")
    if not has_foreign:
        lines.append("No foreign legal references found in any document.")
        lines.append("")
    
    # Indian law references
    lines.append("## Indian Law References")
    lines.append("")
    for r in results:
        if "error" in r:
            continue
        ir = r.get("foreign_references", {}).get("indian_law_references", [])
        if ir:
            lines.append(f"### {r['filename']}")
            for ref in ir:
                lines.append(f"- {ref}")
            lines.append("")
    
    # Outdated tech
    lines.append("## Outdated Technology References")
    lines.append("")
    has_outdated = False
    for r in results:
        if "error" in r:
            continue
        ot = r.get("outdated_tech_references", [])
        if ot:
            has_outdated = True
            lines.append(f"### {r['filename']}")
            for t in ot:
                lines.append(f"- {t['technology']} ({t['mentions']} mention(s))")
            lines.append("")
    if not has_outdated:
        lines.append("No outdated technology references found.")
        lines.append("")
    
    # Key policy values
    lines.append("## Key Policy Values Summary")
    lines.append("")
    for r in results:
        if "error" in r:
            continue
        kpv = r.get("key_policy_values", [])
        if kpv:
            lines.append(f"### {r['filename']} ({r['actual_topic']})")
            for v in kpv[:15]:  # Limit to top 15
                lines.append(f"- {v}")
            if len(kpv) > 15:
                lines.append(f"- ... and {len(kpv) - 15} more values")
            lines.append("")
    
    # Section headings per document
    lines.append("## Document Section Outlines")
    lines.append("")
    for r in results:
        if "error" in r:
            continue
        lines.append(f"### {r['filename']}")
        hl = r.get("heading_list", [])
        if hl:
            for h in hl:
                lines.append(f"- {h}")
        else:
            lines.append("- (No headings detected)")
        lines.append("")
    
    # Errors section
    if errors:
        lines.append("## Errors")
        lines.append("")
        for e in errors:
            lines.append(f"- {e}")
        lines.append("")
    
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"Markdown summary written to: {output_md}")

if __name__ == "__main__":
    main()
