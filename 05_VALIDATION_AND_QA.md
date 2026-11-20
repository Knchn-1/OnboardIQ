# Validation and QA Checklist

## 1. Evidence rule
Every validation result must include:
- check ID;
- command/script and version;
- timestamp;
- result (`PASS`, `FAIL`, `PARTIAL`, `NOT_RUN`);
- output/evidence path;
- defects and remediation.

A check not run is `NOT_RUN`, never PASS. Reopen generated files before claiming they exist and are usable.

## 2. Source and directory checks
- Source inventory matches files actually present.
- Every source file has an extraction report.
- Extracted paragraphs and table text are reconciled against a secondary method where feasible.
- Element census records body, tables, headers, footers, comments, tracked changes, footnotes, text boxes, hyperlinks, fields, content controls, images, charts, properties and watermarks as present/absent/not accessible.
- Directory employee row count matches source tables.
- Verbatim source columns are unchanged.
- Directory anomalies and hierarchy status are documented.

## 3. Master Data and document checks
- Exactly six departments and only six department codes in department lists.
- All invented values have provenance and decision IDs.
- All document owners/role-holders are Directory employees or explicitly unassigned.
- Policy IDs are unique and use valid department codes.
- Document titles, IDs, versions, owners, audiences and lifecycle state agree across files and registry.
- No unresolved placeholders, tokens or template boilerplate.
- Demonstration label appears exactly and consistently.
- No wording claims formal approval.
- Every cross-reference resolves.
- Critical numeric values match Master Data.
- No contradictions across documents.
- Legal-adjacent topics have the verification note and Legal Review Register entry.
- Originality flags are dispositioned.

## 4. PDF checks
- Prefer conversion from final DOCX.
- Record converter name/version and generation method.
- Check text parity, tables, headings, page count, blank pages, ₹ glyph and metadata.
- Run automated geometry checks on all pages.
- Render and visually inspect first/last pages, restricted-unit starts and all non-trivial table pages.
- Save PNGs and per-page inspection records.
- If a PDF is rebuilt from source or visual inspection is incomplete, mark `PARTIALLY_VERIFIED` and list parity gaps.

## 5. RAG and access checks
- Required metadata exists at file/document/section/chunk level.
- Allowed groups are valid and child audiences only narrow parent audiences.
- Unknown, missing or malformed metadata denies access.
- Database retrieval filters unauthorized chunks before ranking/reranking.
- Authorization is rechecked before prompt assembly.
- No unauthorized chunk ID appears in candidate or final context logs.
- No restricted facts appear in broad-audience content.
- Citations map to exact document, section and page.
- Superseded material is not indexed as current.
- Chunk boundaries do not cross audience boundaries.

## 6. Originality checks
Run n-gram/paragraph similarity against provided templates. Suggested severity:
- NOTE: short common phrase match.
- REVIEW: meaningful phrase or paragraph similarity.
- SUSPICIOUS: long verbatim passage or consecutive highly similar sentences.

Use a narrow allowlist for common terminology and standard disclaimers. Do not use the allowlist to mask long copied passages. Record every REVIEW/SUSPICIOUS item and its disposition. This scan does not prove copyright/licence compliance.

## 7. Evaluation dataset checks
- At least 90 questions overall, with coverage across all categories in `04_RAG_AND_ACCESS_CONTROL.md`.
- Follow-up questions form real dependent pairs.
- Gold evidence quotes exist verbatim in cited sections.
- Page references are verified against final PDFs.
- ANSWER questions use sources accessible to the persona.
- REFUSE_ACCESS questions do not reveal restricted facts.
- NOT_FOUND questions have no supporting passage in the corpus.
- Synthetic principals are used only for fail-closed tests.
- Track retrieval hit rate, citation correctness, faithfulness, refusal correctness and context-leak rate. Context-leak rate must be zero.

## 8. Completion labels
Use:
- `NOT_STARTED`
- `IN_PROGRESS`
- `CREATED_NOT_FULLY_VERIFIED`
- `PARTIALLY_VERIFIED`
- `VERIFIED`
- `STALE`
- `PARTIAL`
- `FAILED`

Keep `verified_scope` separate:
- `NONE`
- `DOCUMENT_LEVEL`
- `CORPUS_LEVEL`

Do not use `VERIFIED` for a corpus if corpus-level checks have not run. A Directory with unresolved structural anomalies is not a verified organization structure.
