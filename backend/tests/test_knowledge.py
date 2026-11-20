"""
Knowledge tables and chunk authorization tests.

Tests:
  a) Row counts (15 docs, 137 sections, 139 chunks); every chunk has non-null
     content, allowed_groups, access_policy_version.
  b) SHA-256 of physical DOCX and PDF files matches DB values for all 15 docs.
  c) 13 employees × 139 chunks = 1807 parity comparisons against
     ReferenceAuthorizer.authorize_chunk.
  d) Restricted-unit spot checks (HR RU-001, IT RU-002, FIN RU-003).
  e) Fail-closed: unknown employee → 0 rows; inactive employee → 0 rows.
  f) File-serving allowed_groups verification for selected documents.
  g) Full-text tsquery on content_tsv returns ≥ 1 chunk.
  h) Real stale-policy / stale-state filter tests via UPDATE inside a rolled-back
     transaction: access_policy_version='v0.9', lifecycle_state='SUPERSEDED',
     index_flag='ARCHIVE'.
  i) seed_knowledge validate_knowledge_manifests raises on corrupted records.
"""
import hashlib
import json
import sys
from pathlib import Path

import pytest
from sqlalchemy import func, select, text, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.seed_knowledge import validate_knowledge_manifests
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.document_section import DocumentSection
from app.models.employee import Employee
from app.repositories.chunk_access import fetch_authorized_chunk_codes

REPO_ROOT = Path(__file__).resolve().parents[2]
MASTER_DATA_PATH = REPO_ROOT / "knowledge_base" / "01_master_data" / "northstar_master_data.json"
CHUNK_MANIFEST_PATH = REPO_ROOT / "knowledge_base" / "05_rag_metadata" / "chunk_manifest.jsonl"

# Import ReferenceAuthorizer from scripts/ (read-only)
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from reference_authorizer import ReferenceAuthorizer  # noqa: E402


def _compute_sha256(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while block := f.read(65536):
            hasher.update(block)
    return hasher.hexdigest()


# ---------------------------------------------------------------------------
# (a) Row counts and non-null invariants
# ---------------------------------------------------------------------------
def test_a_row_counts_and_invariants(db_session: Session):
    doc_count = db_session.scalar(select(func.count()).select_from(Document))
    sec_count = db_session.scalar(select(func.count()).select_from(DocumentSection))
    chk_count = db_session.scalar(select(func.count()).select_from(DocumentChunk))

    assert doc_count == 15, f"Expected 15 documents, got {doc_count}"
    assert sec_count == 137, f"Expected 137 sections, got {sec_count}"
    assert chk_count == 139, f"Expected 139 chunks, got {chk_count}"

    # Every chunk has non-null content, allowed_groups, access_policy_version
    null_content = db_session.scalar(
        select(func.count()).select_from(DocumentChunk).where(DocumentChunk.content.is_(None))
    )
    null_groups = db_session.scalar(
        select(func.count()).select_from(DocumentChunk).where(DocumentChunk.allowed_groups.is_(None))
    )
    null_apv = db_session.scalar(
        select(func.count()).select_from(DocumentChunk).where(DocumentChunk.access_policy_version.is_(None))
    )
    assert null_content == 0
    assert null_groups == 0
    assert null_apv == 0


# ---------------------------------------------------------------------------
# (b) SHA-256 disk verification
# ---------------------------------------------------------------------------
def test_b_sha256_disk_match(db_session: Session):
    kb_dir = settings.KNOWLEDGE_BASE_DIR
    docx_dir = kb_dir / "02_documents_docx"
    pdf_dir = kb_dir / "03_documents_pdf"

    docs = db_session.execute(select(Document)).scalars().all()
    assert len(docs) == 15

    for doc in docs:
        docx_path = docx_dir / doc.source_docx_filename
        assert docx_path.exists(), f"DOCX missing: {docx_path}"
        assert _compute_sha256(docx_path) == doc.source_docx_sha256, (
            f"{doc.document_code}: DOCX SHA-256 mismatch"
        )

        pdf_path = pdf_dir / doc.pdf_filename
        assert pdf_path.exists(), f"PDF missing: {pdf_path}"
        assert _compute_sha256(pdf_path) == doc.pdf_sha256, (
            f"{doc.document_code}: PDF SHA-256 mismatch"
        )


# ---------------------------------------------------------------------------
# (c) 13×139 = 1807 parity comparisons
# ---------------------------------------------------------------------------
def test_c_authorizer_parity(db_session: Session):
    authorizer = ReferenceAuthorizer(str(MASTER_DATA_PATH))

    employees = db_session.execute(
        select(Employee).order_by(Employee.employee_code)
    ).scalars().all()
    assert len(employees) == 13

    chunks = db_session.execute(
        select(DocumentChunk).order_by(DocumentChunk.chunk_code)
    ).scalars().all()
    assert len(chunks) == 139

    total_comparisons = 0
    mismatches: list[str] = []

    for emp in employees:
        db_allowed_codes = fetch_authorized_chunk_codes(db_session, emp.employee_code)

        for chunk in chunks:
            chunk_meta = {
                "classification_audience": chunk.classification_audience,
                "allowed_groups": list(chunk.allowed_groups),
                "access_policy_version": chunk.access_policy_version,
            }
            ref_allowed, _reason = authorizer.authorize_chunk(emp.employee_code, chunk_meta)
            db_allowed = chunk.chunk_code in db_allowed_codes

            if ref_allowed != db_allowed:
                mismatches.append(
                    f"{emp.employee_code} x {chunk.chunk_code}: "
                    f"ref={ref_allowed}, db={db_allowed}"
                )
            total_comparisons += 1

    assert total_comparisons == 13 * 139, f"Expected {13 * 139} comparisons, got {total_comparisons}"
    assert len(mismatches) == 0, (
        f"{len(mismatches)} parity mismatches:\n" + "\n".join(mismatches[:20])
    )


# ---------------------------------------------------------------------------
# (d) Restricted-unit spot checks
# ---------------------------------------------------------------------------
def test_d_restricted_unit_access(db_session: Session):
    # RU-001 (HR_ONLY): EMP-002 (HR) can see it, EMP-007 (ENG) cannot
    emp_002_chunks = fetch_authorized_chunk_codes(db_session, "EMP-002")
    emp_007_chunks = fetch_authorized_chunk_codes(db_session, "EMP-007")

    ru001_chunks = db_session.execute(
        select(DocumentChunk.chunk_code).where(DocumentChunk.restricted_unit_id == "RU-001")
    ).scalars().all()
    assert len(ru001_chunks) >= 1
    for cc in ru001_chunks:
        assert cc in emp_002_chunks, f"EMP-002 (HR) should see RU-001 chunk {cc}"
        assert cc not in emp_007_chunks, f"EMP-007 (ENG) should NOT see RU-001 chunk {cc}"

    # RU-002 (IT_ONLY): EMP-004 (IT) can see it, EMP-010 (DA) cannot
    emp_004_chunks = fetch_authorized_chunk_codes(db_session, "EMP-004")
    emp_010_chunks = fetch_authorized_chunk_codes(db_session, "EMP-010")

    ru002_chunks = db_session.execute(
        select(DocumentChunk.chunk_code).where(DocumentChunk.restricted_unit_id == "RU-002")
    ).scalars().all()
    assert len(ru002_chunks) >= 1
    for cc in ru002_chunks:
        assert cc in emp_004_chunks, f"EMP-004 (IT) should see RU-002 chunk {cc}"
        assert cc not in emp_010_chunks, f"EMP-010 (DA) should NOT see RU-002 chunk {cc}"

    # RU-003 (FINANCE_ONLY): EMP-011 (FIN) can see it, EMP-013 (SCS) cannot
    emp_011_chunks = fetch_authorized_chunk_codes(db_session, "EMP-011")
    emp_013_chunks = fetch_authorized_chunk_codes(db_session, "EMP-013")

    ru003_chunks = db_session.execute(
        select(DocumentChunk.chunk_code).where(DocumentChunk.restricted_unit_id == "RU-003")
    ).scalars().all()
    assert len(ru003_chunks) >= 1
    for cc in ru003_chunks:
        assert cc in emp_011_chunks, f"EMP-011 (FIN) should see RU-003 chunk {cc}"
        assert cc not in emp_013_chunks, f"EMP-013 (SCS) should NOT see RU-003 chunk {cc}"


# ---------------------------------------------------------------------------
# (e) Fail-closed checks
# ---------------------------------------------------------------------------
def test_e_fail_closed(db_session: Session):
    # Unknown employee → 0 rows
    unknown_chunks = fetch_authorized_chunk_codes(db_session, "EMP-999")
    assert len(unknown_chunks) == 0, f"Unknown employee should see 0 chunks, got {len(unknown_chunks)}"

    # Inactive employee → 0 rows
    emp_005 = db_session.execute(
        select(Employee).where(Employee.employee_code == "EMP-005")
    ).scalar_one()
    emp_005.is_active = False
    db_session.flush()

    inactive_chunks = fetch_authorized_chunk_codes(db_session, "EMP-005")
    assert len(inactive_chunks) == 0, f"Inactive employee should see 0 chunks, got {len(inactive_chunks)}"

    # Restore
    emp_005.is_active = True
    db_session.flush()

    # Chunk with non-current policy version → excluded
    # (Tested via authorizer parity: the reference authorizer also denies v0.9)
    # DB-level: check constraints reject NULL policy version, empty groups, unknown groups
    with pytest.raises(Exception):
        bad = DocumentChunk(
            chunk_code="BAD-NULL-APV",
            document_id=1,
            section_id=1,
            heading_path="bad",
            page_number=1,
            content="bad content",
            word_count=2,
            classification_audience="ALL_EMPLOYEES",
            allowed_groups=["GRP_ALL_EMPLOYEES"],
            restricted_unit_id=None,
            access_policy_version=None,
            lifecycle_state="CURRENT",
            index_flag="INDEX",
        )
        db_session.add(bad)
        db_session.flush()
    db_session.rollback()

    with pytest.raises(Exception):
        bad2 = DocumentChunk(
            chunk_code="BAD-EMPTY-GROUPS",
            document_id=1,
            section_id=1,
            heading_path="bad",
            page_number=1,
            content="bad content",
            word_count=2,
            classification_audience="ALL_EMPLOYEES",
            allowed_groups=[],
            restricted_unit_id=None,
            access_policy_version="v1.0",
            lifecycle_state="CURRENT",
            index_flag="INDEX",
        )
        db_session.add(bad2)
        db_session.flush()
    db_session.rollback()

    with pytest.raises(Exception):
        bad3 = DocumentChunk(
            chunk_code="BAD-UNKNOWN-GROUP",
            document_id=1,
            section_id=1,
            heading_path="bad",
            page_number=1,
            content="bad content",
            word_count=2,
            classification_audience="ALL_EMPLOYEES",
            allowed_groups=["GRP_SUPERADMIN_INVENTED"],
            restricted_unit_id=None,
            access_policy_version="v1.0",
            lifecycle_state="CURRENT",
            index_flag="INDEX",
        )
        db_session.add(bad3)
        db_session.flush()
    db_session.rollback()


# ---------------------------------------------------------------------------
# (f) File-serving allowed_groups verification
# ---------------------------------------------------------------------------
def test_f_file_serving_groups(db_session: Session):
    with open(MASTER_DATA_PATH, "r", encoding="utf-8") as f:
        md = json.load(f)
    matrix = md["Access_Control_Matrix"]

    checks = {
        "DOC-NST-HR-POL-001": "HR_ONLY",
        "DOC-NST-IT-POL-001": "IT_ONLY",
        "DOC-NST-FIN-POL-001": "FINANCE_ONLY",
        "DOC-NST-HR-POL-007": "MANAGERS_AND_HR",
    }

    for doc_code, expected_audience in checks.items():
        doc = db_session.execute(
            select(Document).where(Document.document_code == doc_code)
        ).scalar_one()

        expected_groups = set(matrix[expected_audience]["groups"])
        assert doc.file_serving_audience == expected_audience, (
            f"{doc_code}: expected file_serving_audience={expected_audience}, got {doc.file_serving_audience}"
        )
        assert set(doc.file_serving_allowed_groups) == expected_groups, (
            f"{doc_code}: file_serving_allowed_groups mismatch"
        )


# ---------------------------------------------------------------------------
# (g) Full-text search
# ---------------------------------------------------------------------------
def test_g_fulltext_tsquery(db_session: Session):
    result = db_session.execute(
        select(DocumentChunk.chunk_code).where(
            DocumentChunk.content_tsv.op("@@")(
                func.to_tsquery("english", "remote & work")
            )
        )
    ).scalars().all()
    assert len(result) >= 1, "Expected at least 1 chunk matching 'remote & work'"


# ---------------------------------------------------------------------------
# (h) Real stale-policy / stale-state UPDATE tests inside rolled-back txn
# ---------------------------------------------------------------------------
def test_h_stale_filters_real_update(db_session: Session):
    """UPDATE a chunk's access_policy_version / lifecycle_state / index_flag inside
    a savepoint, verify fetch_authorized_chunk_codes returns 0 for all 13 employees,
    then roll back and verify the chunk IS returned to its allowed employees."""

    employees = db_session.execute(
        select(Employee).order_by(Employee.employee_code)
    ).scalars().all()
    assert len(employees) == 13

    # Pick an ALL_EMPLOYEES CURRENT/INDEX chunk as the target.
    target = db_session.execute(
        select(DocumentChunk)
        .where(
            DocumentChunk.lifecycle_state == "CURRENT",
            DocumentChunk.index_flag == "INDEX",
            DocumentChunk.classification_audience == "ALL_EMPLOYEES",
        )
        .limit(1)
    ).scalar_one()
    target_code = target.chunk_code

    # Confirm the chunk IS visible to all 13 employees before mutation.
    for emp in employees:
        allowed = fetch_authorized_chunk_codes(db_session, emp.employee_code)
        assert target_code in allowed, (
            f"Before update: {emp.employee_code} should see {target_code}"
        )

    # --- Sub-test 1: access_policy_version = 'v0.9' ---
    # v0.9 matches the regex ^v[0-9]+\.[0-9]+$ so the CHECK constraint allows it.
    sp1 = db_session.begin_nested()
    db_session.execute(
        text("UPDATE document_chunks SET access_policy_version = 'v0.9' WHERE chunk_code = :code"),
        {"code": target_code},
    )
    db_session.flush()
    for emp in employees:
        allowed = fetch_authorized_chunk_codes(db_session, emp.employee_code)
        assert target_code not in allowed, (
            f"access_policy_version=v0.9: {emp.employee_code} should NOT see {target_code}"
        )
    sp1.rollback()

    # Confirm restored.
    for emp in employees:
        allowed = fetch_authorized_chunk_codes(db_session, emp.employee_code)
        assert target_code in allowed, (
            f"After rollback (apv): {emp.employee_code} should again see {target_code}"
        )

    # --- Sub-test 2: lifecycle_state = 'SUPERSEDED' ---
    sp2 = db_session.begin_nested()
    db_session.execute(
        text("UPDATE document_chunks SET lifecycle_state = 'SUPERSEDED' WHERE chunk_code = :code"),
        {"code": target_code},
    )
    db_session.flush()
    for emp in employees:
        allowed = fetch_authorized_chunk_codes(db_session, emp.employee_code)
        assert target_code not in allowed, (
            f"lifecycle_state=SUPERSEDED: {emp.employee_code} should NOT see {target_code}"
        )
    sp2.rollback()

    for emp in employees:
        allowed = fetch_authorized_chunk_codes(db_session, emp.employee_code)
        assert target_code in allowed, (
            f"After rollback (lifecycle): {emp.employee_code} should again see {target_code}"
        )

    # --- Sub-test 3: index_flag = 'ARCHIVE' ---
    sp3 = db_session.begin_nested()
    db_session.execute(
        text("UPDATE document_chunks SET index_flag = 'ARCHIVE' WHERE chunk_code = :code"),
        {"code": target_code},
    )
    db_session.flush()
    for emp in employees:
        allowed = fetch_authorized_chunk_codes(db_session, emp.employee_code)
        assert target_code not in allowed, (
            f"index_flag=ARCHIVE: {emp.employee_code} should NOT see {target_code}"
        )
    sp3.rollback()

    for emp in employees:
        allowed = fetch_authorized_chunk_codes(db_session, emp.employee_code)
        assert target_code in allowed, (
            f"After rollback (index_flag): {emp.employee_code} should again see {target_code}"
        )


# ---------------------------------------------------------------------------
# (i) validate_knowledge_manifests raises on corrupted in-memory records
# ---------------------------------------------------------------------------
def test_i_validate_knowledge_manifests_raises(db_session: Session):
    """Feed deliberately corrupted in-memory records to validate_knowledge_manifests
    and assert each violation causes a ValueError. No knowledge_base files are modified."""
    import copy

    with open(MASTER_DATA_PATH, "r", encoding="utf-8") as f:
        md = json.load(f)

    kb_dir = settings.KNOWLEDGE_BASE_DIR
    meta_dir = kb_dir / "05_rag_metadata"

    # Load real manifests (read-only)
    docs = [json.loads(l) for l in open(meta_dir / "document_manifest.jsonl") if l.strip()]
    sections = [json.loads(l) for l in open(meta_dir / "section_index.jsonl") if l.strip()]
    chunks = [json.loads(l) for l in open(meta_dir / "chunk_manifest.jsonl") if l.strip()]
    access_matrix = md["Access_Control_Matrix"]

    # --- Corruption 1: allowed_groups does not match the audience label ---
    bad_docs = copy.deepcopy(docs)
    bad_docs[0]["document_allowed_groups"] = ["GRP_DEPT_HR"]  # wrong for ALL_EMPLOYEES doc
    # Ensure the doc has ALL_EMPLOYEES audience so this is definitely a mismatch.
    bad_docs[0]["document_audience"] = "ALL_EMPLOYEES"
    with pytest.raises(ValueError, match="violation"):
        validate_knowledge_manifests(
            docs=bad_docs,
            sections=sections,
            chunks=chunks,
            access_matrix=access_matrix,
            kb_dir=kb_dir,
        )

    # --- Corruption 2: chunk allowed_groups wider than its parent section ---
    # Find a chunk whose section is HR_ONLY, then give the chunk ALL_EMPLOYEES groups.
    bad_chunks = copy.deepcopy(chunks)
    ru_chunk = next((c for c in bad_chunks if c.get("restricted_unit_id") == "RU-001"), None)
    assert ru_chunk is not None, "Expected at least one RU-001 chunk in manifest"
    original_groups = ru_chunk["allowed_groups"]
    ru_chunk["allowed_groups"] = ["GRP_ALL_EMPLOYEES"]  # wider than section's HR_ONLY
    ru_chunk["classification_audience"] = "ALL_EMPLOYEES"  # make audience match groups
    with pytest.raises(ValueError, match="violation"):
        validate_knowledge_manifests(
            docs=docs,
            sections=sections,
            chunks=bad_chunks,
            access_matrix=access_matrix,
            kb_dir=kb_dir,
        )
    ru_chunk["allowed_groups"] = original_groups
    ru_chunk["classification_audience"] = "HR_ONLY"

    # --- Corruption 3: wrong SHA-256 in manifest ---
    bad_docs2 = copy.deepcopy(docs)
    bad_docs2[0]["source_docx_sha256"] = "a" * 64  # all-'a' is a valid hex-64 but wrong hash
    with pytest.raises(ValueError, match="violation"):
        validate_knowledge_manifests(
            docs=bad_docs2,
            sections=sections,
            chunks=chunks,
            access_matrix=access_matrix,
            kb_dir=kb_dir,
        )
