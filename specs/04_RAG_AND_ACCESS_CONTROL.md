# RAG Metadata and Access-Control Specification

## 1. RAG-ready structure
For each document, section and chunk retain:
- `document_id`, `policy_id`, title, version;
- source filename and SHA-256;
- lifecycle state (`CURRENT` / `SUPERSEDED`);
- demonstration status label;
- section ID, section number and heading path;
- page start/end when reliably available;
- provenance references;
- classification/audience label;
- resolved `allowed_groups`;
- `access_policy_version`;
- `index_flag` (`INDEX`, `ARCHIVE`, `EXCLUDE`);
- stable chunk ID and chunking version.

Generate at least:
- `document_manifest.jsonl`
- `section_index.jsonl`
- `chunk_manifest.jsonl`
- `access_control_specification.md`
- access-control JSON Schema;
- reference authorizer and fail-closed tests;
- retrieval evaluation dataset.

## 2. Controlled groups
Define groups from the Directory only:
- `GRP_ALL_EMPLOYEES`
- `GRP_MANAGERS`
- `GRP_DEPT_HR`
- `GRP_DEPT_IT`
- `GRP_DEPT_ENG`
- `GRP_DEPT_DA`
- `GRP_DEPT_FIN`
- `GRP_DEPT_SCS`

Optional location groups may be introduced only when justified.

Membership rules:
- All employees: employees present in the Directory.
- Department groups: derived from the Directory department field.
- Managers: employees with at least one direct report, only where hierarchy is unambiguous.
- If a Directory anomaly makes membership uncertain, do not grant the group; log the reason.

## 3. Audience labels
Define labels only in the Access Control Matrix. Initial examples:
- `ALL_EMPLOYEES`
- `MANAGERS`
- `HR_ONLY`
- `IT_ONLY`
- `FINANCE_ONLY`
- `SALES_ONLY`
- `ENGINEERING_ONLY` (may include ENG and DA only if explicitly justified)
- combined labels such as `MANAGERS_AND_HR`

Use any-of semantics only if explicitly stated in the matrix. Unknown labels are invalid.

## 4. Metadata inheritance and narrowing
Every file, document, section and chunk must carry resolved `allowed_groups`.

A child can only narrow its parent's audience:
`chunk_allowed_groups ⊆ section_allowed_groups ⊆ document_allowed_groups ⊆ file_allowed_groups`

Do not infer missing permissions. If metadata is absent or inconsistent, deny access.

For a mixed-audience document, the file-serving audience must be the most restrictive audience required to protect all sections in a whole-file download. Section-level retrieval may return only authorized sections, but a user must not receive the entire mixed-audience file unless authorized for all its contents.

## 5. Enforcement order — mandatory
1. Authenticate the principal.
2. Resolve identity and group membership from trusted Directory-derived data.
3. Validate policy version and metadata schema.
4. Apply authorization filters inside the database retrieval query for both vector and full-text search.
5. Retrieve only authorized candidates.
6. Fuse and rerank only authorized candidates.
7. Re-check authorization immediately before context/prompt assembly.
8. Include only authorized chunks and citations in the LLM context.
9. Log IDs and decisions without storing unauthorized chunk text in logs.

Unauthorized content must never reach ranking, reranking, prompt construction, model memory, caches, summaries or user-visible citations.

## 6. Fail-closed decision table
Return DENY when:
- principal is missing or unresolved;
- group membership cannot be computed;
- access metadata is missing, malformed or uses an unknown label;
- document/section/chunk permissions conflict;
- policy version is missing or inconsistent;
- authorization service or database filter fails;
- cached authorization is stale or cannot be validated;
- user identity changes between retrieval and prompt assembly.

Do not fall back to `ALL_EMPLOYEES`.

## 7. Denial behaviour
Use a generic response that does not confirm restricted content exists. Example:
“I couldn’t find information I can share for that request. Please contact the relevant authorized team.”

Do not name restricted document titles, section names, facts or the existence of hidden material.

## 8. Restricted units and leak prevention
Create at least three restricted units with:
- unit ID;
- document/section;
- audience label and resolved groups;
- business rationale;
- list of restricted facts;
- authorized test persona;
- unauthorized test persona.

Restricted facts must not appear in broader-audience documents, FAQs, examples or chunks. Test for direct and paraphrased leakage.

## 9. Chunking
Use heading-aware, structure-preserving chunks. A target range around 300–600 tokens is a guideline, not a rigid requirement. Keep tables together where practical. Never merge chunks across sections with different audiences. Overlap must not cross an access boundary. Every chunk must be independently understandable and carry complete metadata.

## 10. Lifecycle and caching
- Current documents: `lifecycle_state=CURRENT`, `index_flag=INDEX`.
- Superseded documents: `lifecycle_state=SUPERSEDED`, `index_flag=ARCHIVE`.
- Provenance-only appendices or non-answerable source extracts: `index_flag=EXCLUDE`.
- Cache keys must include principal/group context and policy version, or cache only authorization-neutral data.
- Revalidate authorization before serving cached results.
- Do not retain restricted content in conversation memory or cross-user caches.

## 11. RAG evaluation
Include questions for:
- exact Policy ID/keyword lookup;
- semantic/paraphrased policy questions;
- employee and department lookups;
- approval workflows and thresholds;
- multi-document reasoning;
- follow-up pairs;
- insufficient evidence / NOT_FOUND;
- conflicting or superseded values;
- authorized and unauthorized access attempts;
- chunk-level leak attempts;
- onboarding tasks;
- numeric/table lookup;
- location-specific differences;
- demonstration-status questions.

Each row should include question ID, query, persona, expected behaviour (`ANSWER`, `NOT_FOUND`, `REFUSE_ACCESS`), gold answer, evidence quote, document/section/page, expected authorized chunk IDs, forbidden chunk IDs, and verification status. Do not invent gold citations or page numbers.
