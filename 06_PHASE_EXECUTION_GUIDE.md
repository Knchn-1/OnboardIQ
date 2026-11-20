# Phase-by-Phase Execution Guide

Execute phases in order. Do not attempt to generate all final documents in one pass. At the end of each phase, update `progress.json`, append to `progress_log.md`, and record evidence in `verification_log.md`.

## Phase 0 — Bootstrap
1. Inspect workspace and `/source/`; list every file.
2. Probe Python, document libraries, spreadsheet libraries, PDF converter, PDF text extraction, image rendering/viewing and OCR availability.
3. Create output folder structure.
4. Hash every source file.
5. Copy the Directory DOCX unchanged to `01_master_data/source_of_truth/`; record hash.
6. Create progress and execution-plan files.
**Gate:** output is writable; source hashes recorded; tools/fallbacks documented.

## Phase 1 — Source inspection and extraction
1. Open every source file and inspect actual contents.
2. Create `source_inventory.xlsx`.
3. Extract paragraphs, tables, headings, headers/footers and accessible document elements.
4. Record element types absent, extracted, partially extracted or inaccessible.
5. Reconcile important text/tables using a secondary extraction method where possible.
6. Fully parse the employee Directory and build `Directory_Integrity_Report.xlsx`.
7. For the long IT manual, create a section-by-section outline and page references.
8. Create placeholder and foreign-reference registers.
**Gate:** inventory and extraction reports exist; Directory row parity and anomalies are reported honestly.

## Phase 2 — Conflict, overlap and coverage analysis
1. Map every source topic to a proposed final document.
2. Identify overlaps, contradictions, outdated/foreign references and missing information.
3. Create a source-to-document traceability matrix.
4. Create a conflict register and gap register.
5. Record proposed resolutions; do not overwrite Directory facts.
6. Identify legal-review topics.
**Gate:** every source has a disposition and every conflict/gap has an owner/decision path.

## Phase 3 — Company Master Data
1. Define the company profile and exactly six departments.
2. Preserve Directory source fields and create separate normalized fields.
3. Define fictional policies, contacts, approval limits, SLAs and workflows.
4. Assign existing Directory employees to roles only when supported by the Directory and anomaly-free.
5. Define access groups, audiences and restricted units.
6. Add provenance and Decision Log entries for every invented value.
7. Add Legal Review Register entries.
8. Freeze and hash Master Data.
**Gate:** no unresolved critical value; all fictional values are traceable; Directory integrity status is explicit.

## Phase 4 — Document architecture and outlines
1. Confirm 12–15 document titles and document-number map.
2. Assign Policy IDs using only HR, IT, ENG, DA, FIN, SCS.
3. Define stable section keys and headings for every document.
4. Map competency questions to sections.
5. Assign document/section audiences.
6. Resolve cross-document references from the outline map.
**Gate:** complete outlines and audience map are frozen before drafting.

## Phase 5 — Draft documents
1. Draft each document from Master Data and approved outlines.
2. Use tokens or controlled rendering for repeated values.
3. Write original prose; do not copy template passages.
4. Add self-contained sections, useful tables and FAQs.
5. Add the demonstration banner and required metadata.
6. Save DOCX files and reopen them.
7. Run document-level checks; fix defects before proceeding.
**Gate:** all planned DOCX files exist and pass document-level checks or are explicitly marked partial.

## Phase 6 — PDF generation and visual QA
1. Convert each final DOCX to PDF using a documented converter.
2. Record generation method and converter version.
3. Extract PDF text and compare against DOCX.
4. Run automated geometry/content checks on all pages.
5. Render and inspect first/last pages, restricted-unit starts and complex-table pages.
6. Save page inspection records and screenshots.
7. Mark rebuilt or incompletely inspected PDFs `PARTIALLY_VERIFIED`.
**Gate:** PDF status and parity gaps are explicit.

## Phase 7 — Registers and RAG metadata
1. Finalize Policy Registry and source/decision registers.
2. Generate document, section and chunk manifests from final files.
3. Generate stable chunk IDs and preserve heading/page metadata.
4. Validate all audience inheritance and narrowing.
5. Create access-control specification, schema and reference authorizer tests.
6. Confirm restricted facts do not leak into broad-audience content.
**Gate:** manifests match files and access metadata; fail-closed tests run.

## Phase 8 — RAG evaluation dataset
1. Create at least 90 test questions across the specified categories.
2. Include exact lookup, paraphrase, multi-document, follow-up, NOT_FOUND, superseded, numeric, location and access-control cases.
3. Verify every gold quote and citation against final files.
4. Record authorized and forbidden chunk IDs for personas.
5. Include scoring guide and expected behaviour.
**Gate:** evaluation data is traceable, citations are real, access expectations are correct.

## Phase 9 — Final corpus verification and README
1. Regenerate manifests from final files and compare with prior manifests.
2. Re-run all applicable validation checks.
3. Confirm source hashes unchanged.
4. Confirm registry, manifests, documents and PDFs agree.
5. Finalize README with paths, purpose, hashes, verification status and limitations.
6. Produce the final report using the master prompt's required structure.
**Gate:** no unsupported VERIFIED claims; all open issues are listed.

## Resume protocol
When a session restarts:
1. Read `progress.json`, `progress_log.md` and `verification_log.md`.
2. Recompute hashes for source files and verified outputs.
3. Mark changed outputs `STALE`.
4. Resume from the earliest incomplete or stale dependency.
5. Never overwrite a verified artifact without recording why and invalidating its prior verification.
