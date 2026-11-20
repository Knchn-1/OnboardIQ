"""
Phase 7: Build RAG Metadata Manifests & Registers
Extracts document, section, and chunk level records from the 15 finalized DOCX & PDF files.
Generates:
  - output/05_rag_metadata/document_manifest.jsonl
  - output/05_rag_metadata/section_index.jsonl
  - output/05_rag_metadata/chunk_manifest.jsonl
  - output/04_registers_and_reports/policy_registry.json & .md
"""
import os
import json
import hashlib
import docx
import fitz

OUTPUT_META_DIR = "output/05_rag_metadata"
OUTPUT_REG_DIR = "output/04_registers_and_reports"
os.makedirs(OUTPUT_META_DIR, exist_ok=True)
os.makedirs(OUTPUT_REG_DIR, exist_ok=True)

with open("output/01_master_data/northstar_master_data.json", "r", encoding="utf-8") as f:
    MD = json.load(f)

DEMO_LABEL = MD["_metadata"]["demonstration_label"]
ACCESS_MATRIX = MD["Access_Control_Matrix"]

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

# Load doc map
doc_map_lookup = {item["policy_id"]: item for item in MD["Document_Number_Map"]}

docx_dir = "output/02_documents_docx"
pdf_dir = "output/03_documents_pdf"
docx_files = sorted(os.listdir(docx_dir))

document_manifest = []
section_index = []
chunk_manifest = []

global_chunk_counter = 0

for df in docx_files:
    if not df.endswith(".docx"):
        continue
    base = os.path.splitext(df)[0]
    policy_id = base.split("_")[0]
    
    docx_path = os.path.join(docx_dir, df)
    pdf_path = os.path.join(pdf_dir, base + ".pdf")
    
    docx_hash = sha256_file(docx_path)
    pdf_hash = sha256_file(pdf_path) if os.path.exists(pdf_path) else None
    
    # Document info
    doc_info = doc_map_lookup.get(policy_id, {
        "title": base,
        "owner_emp": "EMP-002",
        "owner_name": "Ishita Rao",
        "audience": "ALL_EMPLOYEES"
    })
    
    doc_audience = doc_info["audience"]
    resolved_doc_groups = ACCESS_MATRIX.get(doc_audience, {}).get("groups", ["GRP_ALL_EMPLOYEES"])
    
    # Whole file serving audience rule:
    # If the document contains a restricted unit, whole file download must require the restricted audience
    file_audience = doc_audience
    if policy_id == "NST-HR-POL-001":
        file_audience = "HR_ONLY"
    elif policy_id == "NST-IT-POL-001":
        file_audience = "IT_ONLY"
    elif policy_id == "NST-FIN-POL-001":
        file_audience = "FINANCE_ONLY"
        
    resolved_file_groups = ACCESS_MATRIX.get(file_audience, {}).get("groups", resolved_doc_groups)

    doc_entry = {
        "document_id": f"DOC-{policy_id}",
        "policy_id": policy_id,
        "title": doc_info["title"],
        "version": "1.0",
        "lifecycle_state": "CURRENT",
        "demonstration_label": DEMO_LABEL,
        "source_docx_filename": df,
        "source_docx_sha256": docx_hash,
        "pdf_filename": base + ".pdf",
        "pdf_sha256": pdf_hash,
        "owner_employee_id": doc_info["owner_emp"],
        "owner_name": doc_info["owner_name"],
        "document_audience": doc_audience,
        "document_allowed_groups": resolved_doc_groups,
        "file_serving_audience": file_audience,
        "file_serving_allowed_groups": resolved_file_groups,
        "access_policy_version": "v1.0",
        "index_flag": "INDEX",
        "provenance": "L3-FINAL-DERIVED",
        "total_pages": len(fitz.open(pdf_path)) if os.path.exists(pdf_path) else 1
    }
    document_manifest.append(doc_entry)
    
    # Parse DOCX into sections
    doc_obj = docx.Document(docx_path)
    
    current_sec_num = "0"
    current_sec_title = "Overview & Metadata"
    current_sec_text = []
    current_sec_audience = doc_audience
    current_sec_restricted_unit = None
    
    # Track sections
    sections = []
    
    for p in doc_obj.paragraphs:
        txt = p.text.strip()
        if not txt:
            continue
        style_name = p.style.name if p.style else ""
        
        if "Heading 1" in style_name:
            # Save previous section
            if current_sec_text:
                sections.append({
                    "sec_num": current_sec_num,
                    "title": current_sec_title,
                    "text": "\n".join(current_sec_text),
                    "audience": current_sec_audience,
                    "restricted_unit": current_sec_restricted_unit
                })
            # Start new section
            parts = txt.split(".", 1)
            if len(parts) == 2 and parts[0].isdigit():
                current_sec_num = parts[0].strip()
                current_sec_title = parts[1].strip()
            else:
                current_sec_num = str(len(sections) + 1)
                current_sec_title = txt
                
            current_sec_text = [txt]
            
            # Check restricted section triggers
            if "Disciplinary Action and Termination" in txt:
                current_sec_audience = "HR_ONLY"
                current_sec_restricted_unit = "RU-001"
            elif "Security Incident Response Procedures" in txt:
                current_sec_audience = "IT_ONLY"
                current_sec_restricted_unit = "RU-002"
            elif "Finance Audit Controls and Fraud" in txt:
                current_sec_audience = "FINANCE_ONLY"
                current_sec_restricted_unit = "RU-003"
            else:
                current_sec_audience = doc_audience
                current_sec_restricted_unit = None
        else:
            current_sec_text.append(txt)
            
    # Include tables text into current section
    for tbl in doc_obj.tables:
        tbl_text = []
        for row in tbl.rows:
            tbl_text.append(" | ".join(c.text.strip().replace("\n", " ") for c in row.cells))
        if tbl_text:
            current_sec_text.append("\n[Table Data]\n" + "\n".join(tbl_text))

    if current_sec_text:
        sections.append({
            "sec_num": current_sec_num,
            "title": current_sec_title,
            "text": "\n".join(current_sec_text),
            "audience": current_sec_audience,
            "restricted_unit": current_sec_restricted_unit
        })

    # Page mapping helper from PyMuPDF
    pdf_doc = fitz.open(pdf_path) if os.path.exists(pdf_path) else None
    
    def find_page_range(sec_title):
        if not pdf_doc:
            return 1, 1
        matches = []
        key = sec_title[:20].lower()
        for idx, page in enumerate(pdf_doc):
            if key in page.get_text().lower():
                matches.append(idx + 1)
        if matches:
            return min(matches), max(matches)
        return 1, len(pdf_doc)

    for sec in sections:
        sec_id = f"SEC-{policy_id}-{sec['sec_num']}"
        heading_path = f"{doc_info['title']} > {sec['sec_num']}. {sec['title']}"
        sec_aud = sec["audience"]
        sec_groups = ACCESS_MATRIX.get(sec_aud, {}).get("groups", resolved_doc_groups)
        
        # Audience narrowing validation: section groups must be a subset of document groups
        # Note: If doc is ALL_EMPLOYEES, section can narrow to HR_ONLY, IT_ONLY, etc.
        # This is valid narrowing: child audience is more restrictive.
        
        p_start, p_end = find_page_range(sec["title"])
        
        sec_entry = {
            "section_id": sec_id,
            "document_id": f"DOC-{policy_id}",
            "policy_id": policy_id,
            "section_number": sec["sec_num"],
            "heading_path": heading_path,
            "section_title": sec["title"],
            "page_start": p_start,
            "page_end": p_end,
            "classification_audience": sec_aud,
            "allowed_groups": sec_groups,
            "restricted_unit_id": sec["restricted_unit"],
            "index_flag": "INDEX",
            "lifecycle_state": "CURRENT"
        }
        section_index.append(sec_entry)
        
        # Chunking: Break section text into structure-aware chunks (~300-500 words)
        full_text = sec["text"]
        paragraphs = full_text.split("\n\n")
        
        chunk_buffer = []
        current_chunk_words = 0
        sec_chunk_idx = 1
        
        for p in paragraphs:
            p_words = len(p.split())
            if current_chunk_words + p_words > 450 and chunk_buffer:
                # Flush chunk
                global_chunk_counter += 1
                chunk_id = f"CHK-{policy_id}-{sec['sec_num']}-{sec_chunk_idx:02d}"
                chunk_text = "\n\n".join(chunk_buffer)
                chunk_entry = {
                    "chunk_id": chunk_id,
                    "global_chunk_id": f"CHK-{global_chunk_counter:04d}",
                    "document_id": f"DOC-{policy_id}",
                    "policy_id": policy_id,
                    "section_id": sec_id,
                    "heading_path": heading_path,
                    "page_number": p_start,
                    "classification_audience": sec_aud,
                    "allowed_groups": sec_groups,
                    "restricted_unit_id": sec["restricted_unit"],
                    "word_count": len(chunk_text.split()),
                    "content": chunk_text,
                    "demonstration_label": DEMO_LABEL,
                    "index_flag": "INDEX",
                    "lifecycle_state": "CURRENT",
                    "provenance": "L3-FINAL-PROSE"
                }
                chunk_manifest.append(chunk_entry)
                sec_chunk_idx += 1
                chunk_buffer = [p]
                current_chunk_words = p_words
            else:
                chunk_buffer.append(p)
                current_chunk_words += p_words
                
        if chunk_buffer:
            global_chunk_counter += 1
            chunk_id = f"CHK-{policy_id}-{sec['sec_num']}-{sec_chunk_idx:02d}"
            chunk_text = "\n\n".join(chunk_buffer)
            chunk_entry = {
                "chunk_id": chunk_id,
                "global_chunk_id": f"CHK-{global_chunk_counter:04d}",
                "document_id": f"DOC-{policy_id}",
                "policy_id": policy_id,
                "section_id": sec_id,
                "heading_path": heading_path,
                "page_number": p_start,
                "classification_audience": sec_aud,
                "allowed_groups": sec_groups,
                "restricted_unit_id": sec["restricted_unit"],
                "word_count": len(chunk_text.split()),
                "content": chunk_text,
                "demonstration_label": DEMO_LABEL,
                "index_flag": "INDEX",
                "lifecycle_state": "CURRENT",
                "provenance": "L3-FINAL-PROSE"
            }
            chunk_manifest.append(chunk_entry)

# Write JSONL manifests
with open("output/05_rag_metadata/document_manifest.jsonl", "w", encoding="utf-8") as f:
    for doc in document_manifest:
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

with open("output/05_rag_metadata/section_index.jsonl", "w", encoding="utf-8") as f:
    for sec in section_index:
        f.write(json.dumps(sec, ensure_ascii=False) + "\n")

with open("output/05_rag_metadata/chunk_manifest.jsonl", "w", encoding="utf-8") as f:
    for chk in chunk_manifest:
        f.write(json.dumps(chk, ensure_ascii=False) + "\n")

# Write Policy Registry in 04_registers_and_reports
with open("output/04_registers_and_reports/policy_registry.json", "w", encoding="utf-8") as f:
    json.dump(document_manifest, f, indent=2, ensure_ascii=False)

# Markdown table version
with open("output/04_registers_and_reports/policy_registry.md", "w", encoding="utf-8") as f:
    f.write(f"# Northstar Technologies — Policy & Document Registry\n\n")
    f.write(f"**{DEMO_LABEL}**\n\n")
    f.write("| Policy ID | Title | Owner | Audience | File Serving Audience | Total Pages | DOCX SHA-256 (prefix) |\n")
    f.write("|---|---|---|---|---|---|---|\n")
    for doc in document_manifest:
        f.write(f"| {doc['policy_id']} | {doc['title']} | {doc['owner_name']} | `{doc['document_audience']}` | `{doc['file_serving_audience']}` | {doc['total_pages']} | `{doc['source_docx_sha256'][:12]}...` |\n")

print(f"Manifest generation complete:")
print(f"  Documents: {len(document_manifest)}")
print(f"  Sections:  {len(section_index)}")
print(f"  Chunks:    {len(chunk_manifest)}")

