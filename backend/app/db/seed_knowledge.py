import hashlib
import json
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.document_section import DocumentSection
from app.models.employee import Employee


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file on disk."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def validate_knowledge_manifests(
    docs: list[dict],
    sections: list[dict],
    chunks: list[dict],
    access_matrix: dict[str, dict],
    kb_dir: Path,
) -> None:
    """Validate all integrity and access-control rules BEFORE inserting into the database."""
    violations: list[str] = []

    # 1. SHA-256 verification of physical files on disk
    docx_dir = kb_dir / "02_documents_docx"
    pdf_dir = kb_dir / "03_documents_pdf"

    for doc in docs:
        doc_code = doc["document_id"]

        # DOCX check
        docx_file = docx_dir / doc["source_docx_filename"]
        if not docx_file.exists():
            violations.append(f"Document {doc_code}: DOCX file missing at {docx_file}")
        else:
            actual_docx_sha = compute_sha256(docx_file)
            if actual_docx_sha != doc["source_docx_sha256"]:
                violations.append(
                    f"Document {doc_code}: DOCX SHA-256 mismatch: {actual_docx_sha} != {doc['source_docx_sha256']}"
                )

        # PDF check
        pdf_file = pdf_dir / doc["pdf_filename"]
        if not pdf_file.exists():
            violations.append(f"Document {doc_code}: PDF file missing at {pdf_file}")
        else:
            actual_pdf_sha = compute_sha256(pdf_file)
            if actual_pdf_sha != doc["pdf_sha256"]:
                violations.append(
                    f"Document {doc_code}: PDF SHA-256 mismatch: {actual_pdf_sha} != {doc['pdf_sha256']}"
                )

    # 2. Validation (i): allowed_groups equals groups listed for audience label in Access_Control_Matrix
    matrix_groups = {aud: set(data["groups"]) for aud, data in access_matrix.items()}

    for doc in docs:
        doc_code = doc["document_id"]
        doc_aud = doc["document_audience"]
        if doc_aud not in matrix_groups:
            violations.append(f"Document {doc_code}: Unknown document_audience '{doc_aud}'")
        elif set(doc["document_allowed_groups"]) != matrix_groups[doc_aud]:
            violations.append(
                f"Document {doc_code}: document_allowed_groups mismatch for audience '{doc_aud}': "
                f"{set(doc['document_allowed_groups'])} != {matrix_groups[doc_aud]}"
            )

        file_aud = doc["file_serving_audience"]
        if file_aud not in matrix_groups:
            violations.append(f"Document {doc_code}: Unknown file_serving_audience '{file_aud}'")
        elif set(doc["file_serving_allowed_groups"]) != matrix_groups[file_aud]:
            violations.append(
                f"Document {doc_code}: file_serving_allowed_groups mismatch for audience '{file_aud}': "
                f"{set(doc['file_serving_allowed_groups'])} != {matrix_groups[file_aud]}"
            )

    for sec in sections:
        sec_code = sec["section_id"]
        sec_aud = sec["classification_audience"]
        if sec_aud not in matrix_groups:
            violations.append(f"Section {sec_code}: Unknown classification_audience '{sec_aud}'")
        elif set(sec["allowed_groups"]) != matrix_groups[sec_aud]:
            violations.append(
                f"Section {sec_code}: allowed_groups mismatch for audience '{sec_aud}': "
                f"{set(sec['allowed_groups'])} != {matrix_groups[sec_aud]}"
            )

    for chunk in chunks:
        chk_code = chunk["chunk_id"]
        chk_aud = chunk["classification_audience"]
        if chk_aud not in matrix_groups:
            violations.append(f"Chunk {chk_code}: Unknown classification_audience '{chk_aud}'")
        elif set(chunk["allowed_groups"]) != matrix_groups[chk_aud]:
            violations.append(
                f"Chunk {chk_code}: allowed_groups mismatch for audience '{chk_aud}': "
                f"{set(chunk['allowed_groups'])} != {matrix_groups[chk_aud]}"
            )

    # 3. Validation (ii): chunk.allowed_groups is a subset of its section's,
    # and section's is a subset of its document's document_allowed_groups (or section is an authorized restricted unit)
    doc_map = {d["document_id"]: d for d in docs}
    sec_map = {s["section_id"]: s for s in sections}

    for sec in sections:
        sec_code = sec["section_id"]
        doc_code = sec["document_id"]
        if doc_code not in doc_map:
            violations.append(f"Section {sec_code}: parent document '{doc_code}' not found")
            continue
        parent_doc = doc_map[doc_code]
        sec_groups = set(sec["allowed_groups"])
        doc_groups = set(parent_doc["document_allowed_groups"])

        is_subset = sec_groups.issubset(doc_groups) or (
            sec.get("restricted_unit_id") is not None and "GRP_ALL_EMPLOYEES" in doc_groups
        )
        if not is_subset:
            violations.append(
                f"Section {sec_code}: allowed_groups {sec_groups} is not a valid subset of document {doc_code} groups {doc_groups}"
            )

    for chunk in chunks:
        chk_code = chunk["chunk_id"]
        sec_code = chunk["section_id"]
        if sec_code not in sec_map:
            violations.append(f"Chunk {chk_code}: parent section '{sec_code}' not found")
            continue
        parent_sec = sec_map[sec_code]
        chk_groups = set(chunk["allowed_groups"])
        sec_groups = set(parent_sec["allowed_groups"])

        if not chk_groups.issubset(sec_groups):
            violations.append(
                f"Chunk {chk_code}: allowed_groups {chk_groups} is not a subset of section {sec_code} groups {sec_groups}"
            )

    # 4. Validation (iii): chunk.restricted_unit_id equals its section's
    for chunk in chunks:
        chk_code = chunk["chunk_id"]
        sec_code = chunk["section_id"]
        if sec_code in sec_map:
            parent_sec = sec_map[sec_code]
            if chunk.get("restricted_unit_id") != parent_sec.get("restricted_unit_id"):
                violations.append(
                    f"Chunk {chk_code}: restricted_unit_id '{chunk.get('restricted_unit_id')}' != "
                    f"section '{sec_code}' restricted_unit_id '{parent_sec.get('restricted_unit_id')}'"
                )

    if violations:
        print(f"FAILED: Found {len(violations)} validation violation(s) before seeding:")
        for v in violations:
            print(f"  - {v}")
        raise ValueError(f"Aborting seed: {len(violations)} validation violation(s) found.")


def seed_knowledge(session: Session | None = None) -> None:
    """Seed documents, document_sections, and document_chunks idempotently in one transaction."""
    close_session = False
    if session is None:
        session = SessionLocal()
        close_session = True

    kb_dir = settings.KNOWLEDGE_BASE_DIR
    meta_dir = kb_dir / "05_rag_metadata"

    master_file = kb_dir / "01_master_data" / "northstar_master_data.json"
    doc_file = meta_dir / "document_manifest.jsonl"
    sec_file = meta_dir / "section_index.jsonl"
    chk_file = meta_dir / "chunk_manifest.jsonl"

    for req_file in [master_file, doc_file, sec_file, chk_file]:
        if not req_file.exists():
            raise FileNotFoundError(f"Required knowledge base file not found: {req_file}")

    with open(master_file, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    with open(doc_file, "r", encoding="utf-8") as f:
        docs = [json.loads(line) for line in f if line.strip()]

    with open(sec_file, "r", encoding="utf-8") as f:
        sections = [json.loads(line) for line in f if line.strip()]

    with open(chk_file, "r", encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f if line.strip()]

    # Validate everything BEFORE touching the database
    validate_knowledge_manifests(
        docs=docs,
        sections=sections,
        chunks=chunks,
        access_matrix=master_data["Access_Control_Matrix"],
        kb_dir=kb_dir,
    )

    try:
        # Resolve employees: employee_code -> employee.id
        emp_records = session.execute(select(Employee.id, Employee.employee_code)).all()
        emp_code_to_id = {code: eid for eid, code in emp_records}

        # 1. Documents
        doc_code_to_id: dict[str, int] = {}
        for d in docs:
            doc_code = d["document_id"]
            owner_code = d.get("owner_employee_id")
            owner_id = emp_code_to_id.get(owner_code) if owner_code else None

            doc_obj = session.execute(
                select(Document).where(Document.document_code == doc_code)
            ).scalar_one_or_none()

            if doc_obj is None:
                doc_obj = Document(
                    document_code=doc_code,
                    policy_id=d["policy_id"],
                    title=d["title"],
                    version=d["version"],
                    lifecycle_state=d["lifecycle_state"],
                    demonstration_label=d["demonstration_label"],
                    index_flag=d["index_flag"],
                    document_audience=d["document_audience"],
                    file_serving_audience=d["file_serving_audience"],
                    document_allowed_groups=d["document_allowed_groups"],
                    file_serving_allowed_groups=d["file_serving_allowed_groups"],
                    access_policy_version=d["access_policy_version"],
                    source_docx_filename=d["source_docx_filename"],
                    source_docx_sha256=d["source_docx_sha256"],
                    pdf_filename=d["pdf_filename"],
                    pdf_sha256=d["pdf_sha256"],
                    total_pages=d["total_pages"],
                    owner_employee_id=owner_id,
                    provenance=d["provenance"],
                )
                session.add(doc_obj)
                session.flush()
            else:
                doc_obj.policy_id = d["policy_id"]
                doc_obj.title = d["title"]
                doc_obj.version = d["version"]
                doc_obj.lifecycle_state = d["lifecycle_state"]
                doc_obj.demonstration_label = d["demonstration_label"]
                doc_obj.index_flag = d["index_flag"]
                doc_obj.document_audience = d["document_audience"]
                doc_obj.file_serving_audience = d["file_serving_audience"]
                doc_obj.document_allowed_groups = d["document_allowed_groups"]
                doc_obj.file_serving_allowed_groups = d["file_serving_allowed_groups"]
                doc_obj.access_policy_version = d["access_policy_version"]
                doc_obj.source_docx_filename = d["source_docx_filename"]
                doc_obj.source_docx_sha256 = d["source_docx_sha256"]
                doc_obj.pdf_filename = d["pdf_filename"]
                doc_obj.pdf_sha256 = d["pdf_sha256"]
                doc_obj.total_pages = d["total_pages"]
                doc_obj.owner_employee_id = owner_id
                doc_obj.provenance = d["provenance"]
                session.flush()

            doc_code_to_id[doc_code] = doc_obj.id

        # 2. Document Sections
        sec_code_to_id: dict[str, int] = {}
        for s in sections:
            sec_code = s["section_id"]
            doc_code = s["document_id"]
            doc_id = doc_code_to_id[doc_code]

            sec_obj = session.execute(
                select(DocumentSection).where(DocumentSection.section_code == sec_code)
            ).scalar_one_or_none()

            if sec_obj is None:
                sec_obj = DocumentSection(
                    section_code=sec_code,
                    document_id=doc_id,
                    section_number=s["section_number"],
                    section_title=s["section_title"],
                    heading_path=s["heading_path"],
                    page_start=s["page_start"],
                    page_end=s["page_end"],
                    classification_audience=s["classification_audience"],
                    allowed_groups=s["allowed_groups"],
                    restricted_unit_id=s.get("restricted_unit_id"),
                    index_flag=s["index_flag"],
                    lifecycle_state=s["lifecycle_state"],
                )
                session.add(sec_obj)
                session.flush()
            else:
                sec_obj.document_id = doc_id
                sec_obj.section_number = s["section_number"]
                sec_obj.section_title = s["section_title"]
                sec_obj.heading_path = s["heading_path"]
                sec_obj.page_start = s["page_start"]
                sec_obj.page_end = s["page_end"]
                sec_obj.classification_audience = s["classification_audience"]
                sec_obj.allowed_groups = s["allowed_groups"]
                sec_obj.restricted_unit_id = s.get("restricted_unit_id")
                sec_obj.index_flag = s["index_flag"]
                sec_obj.lifecycle_state = s["lifecycle_state"]
                session.flush()

            sec_code_to_id[sec_code] = sec_obj.id

        # 3. Document Chunks
        doc_manifest_map = {d["document_id"]: d for d in docs}

        for c in chunks:
            chk_code = c["chunk_id"]
            doc_code = c["document_id"]
            sec_code = c["section_id"]
            doc_id = doc_code_to_id[doc_code]
            sec_id = sec_code_to_id[sec_code]
            parent_policy_version = doc_manifest_map[doc_code]["access_policy_version"]

            chk_obj = session.execute(
                select(DocumentChunk).where(DocumentChunk.chunk_code == chk_code)
            ).scalar_one_or_none()

            if chk_obj is None:
                chk_obj = DocumentChunk(
                    chunk_code=chk_code,
                    global_chunk_id=c.get("global_chunk_id"),
                    document_id=doc_id,
                    section_id=sec_id,
                    heading_path=c["heading_path"],
                    page_number=c["page_number"],
                    content=c["content"],
                    word_count=c["word_count"],
                    classification_audience=c["classification_audience"],
                    allowed_groups=c["allowed_groups"],
                    restricted_unit_id=c.get("restricted_unit_id"),
                    access_policy_version=parent_policy_version,
                    lifecycle_state=c["lifecycle_state"],
                    index_flag=c["index_flag"],
                    embedding=None,
                    embedding_model=None,
                )
                session.add(chk_obj)
                session.flush()
            else:
                chk_obj.global_chunk_id = c.get("global_chunk_id")
                chk_obj.document_id = doc_id
                chk_obj.section_id = sec_id
                chk_obj.heading_path = c["heading_path"]
                chk_obj.page_number = c["page_number"]
                chk_obj.content = c["content"]
                chk_obj.word_count = c["word_count"]
                chk_obj.classification_audience = c["classification_audience"]
                chk_obj.allowed_groups = c["allowed_groups"]
                chk_obj.restricted_unit_id = c.get("restricted_unit_id")
                chk_obj.access_policy_version = parent_policy_version
                chk_obj.lifecycle_state = c["lifecycle_state"]
                chk_obj.index_flag = c["index_flag"]
                chk_obj.embedding = None
                chk_obj.embedding_model = None
                session.flush()

        session.commit()
        print("Knowledge seed completed successfully!")
        print(f"Seeded: {len(doc_code_to_id)} documents, {len(sec_code_to_id)} sections, {len(chunks)} chunks.")
    except Exception:
        session.rollback()
        raise
    finally:
        if close_session:
            session.close()


if __name__ == "__main__":
    seed_knowledge()
