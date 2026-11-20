# Northstar Technologies — RAG Access-Control Specification

**DEMONSTRATION ONLY — NOT APPROVED FOR REAL-WORLD USE**

## 1. Core Principles
Access control in OnboardIQ is strictly **fail-closed** and enforced at multiple structural levels: whole-file downloads, document retrieval, section inspection, and individual text chunk assembly. Unauthorized candidates are pruned at the retrieval database query level before ranking, reranking, or LLM context assembly.

## 2. Controlled Groups
All group memberships are deterministically derived from the verified fields of the Employee Directory:
- `GRP_ALL_EMPLOYEES`: All 13 employees present in the company directory.
- `GRP_MANAGERS`: Employees with at least one active direct report within the directory hierarchy (`EMP-001`, `EMP-002`, `EMP-004`, `EMP-006`, `EMP-009`, `EMP-011`).
- `GRP_DEPT_HR`: Members of the Human Resources department (`EMP-002`, `EMP-003`).
- `GRP_DEPT_IT`: Members of the Information Technology department (`EMP-004`, `EMP-005`).
- `GRP_DEPT_ENG`: Members of the Engineering department (`EMP-006`, `EMP-007`, `EMP-008`).
- `GRP_DEPT_DA`: Members of the Data & Analytics department (`EMP-009`, `EMP-010`).
- `GRP_DEPT_FIN`: Members of the Finance & Administration department (`EMP-011`, `EMP-012`).
- `GRP_DEPT_SCS`: Members of the Sales & Customer Success department (`EMP-013`).

*Note on CEO:* EMP-001 Aarav Mehta is in `GRP_ALL_EMPLOYEES` and `GRP_MANAGERS`. The CEO is not forced into any single departmental group.

## 3. Audience Classification Labels
- `ALL_EMPLOYEES`: Resolved to `["GRP_ALL_EMPLOYEES"]` (any employee may access).
- `MANAGERS`: Resolved to `["GRP_MANAGERS"]` (people managers only).
- `MANAGERS_AND_HR`: Resolved to `["GRP_MANAGERS", "GRP_DEPT_HR"]` with `any-of` semantics.
- `HR_ONLY`: Resolved to `["GRP_DEPT_HR"]`.
- `IT_ONLY`: Resolved to `["GRP_DEPT_IT"]`.
- `FINANCE_ONLY`: Resolved to `["GRP_DEPT_FIN"]`.
- `ENGINEERING_ONLY`: Resolved to `["GRP_DEPT_ENG"]`.
- `DA_ONLY`: Resolved to `["GRP_DEPT_DA"]`.
- `SALES_ONLY`: Resolved to `["GRP_DEPT_SCS"]`.

## 4. Hierarchy and Narrowing Rule
Metadata resolution enforces strict audience narrowing down the hierarchy tree:
$$\text{chunk\_allowed\_groups} \subseteq \text{section\_allowed\_groups} \subseteq \text{document\_allowed\_groups} \subseteq \text{file\_allowed\_groups}$$

- A child section or chunk can only restrict access further; it cannot widen access beyond its parent.
- **Mixed-Audience File Serving Rule:** Where a document contains one or more restricted sections (e.g. RU-001 in NST-HR-POL-001), the whole-file serving audience is set to the most restrictive audience (`HR_ONLY`). Section-level retrieval allows general employees to retrieve unclassified sections, but downloading the complete mixed-audience DOCX/PDF file is restricted to authorized personnel.

## 5. Mandatory Fail-Closed Enforcement Order
1. **Authentication:** Authenticate principal identity (e.g. `EMP-007`).
2. **Group Resolution:** Map principal to directory-derived group set (e.g. `['GRP_ALL_EMPLOYEES', 'GRP_DEPT_ENG']`).
3. **Pre-Query Filtering:** Inject authorization predicates directly into vector and full-text database queries:
   $$\text{WHERE } \text{allowed\_groups} \cap \text{principal\_groups} \neq \emptyset$$
4. **Candidate Retrieval:** Retrieve only authorized candidate chunks.
5. **Reranking:** Cross-encoder reranks only pre-filtered authorized chunks.
6. **Pre-Prompt Verification:** Re-verify chunk authorization immediately before assembling LLM context prompt.
7. **Safe Refusal:** When a user requests restricted material or when no authorized chunks are found, return a generic refusal:
   > *"I couldn’t find information I can share for that request. Please contact the relevant authorized team."*
   Never acknowledge the existence of restricted documents or disclose hidden section headings.

## 6. Restricted Units Registry
| Unit ID | Parent Document | Section Title | Audience | Allowed Groups | Business Rationale | Authorized Persona | Unauthorized Persona |
|---|---|---|---|---|---|---|---|
| `RU-001` | NST-HR-POL-001 | Section 13: Disciplinary Action and Termination Procedures | `HR_ONLY` | `["GRP_DEPT_HR"]` | Sensitive progressive discipline steps, termination checklist, suspension rules | Ishita Rao (EMP-002, HR) | Vikram Joshi (EMP-007, ENG) |
| `RU-002` | NST-IT-POL-001 | Section 7: Security Incident Response Procedures — Internal Playbook | `IT_ONLY` | `["GRP_DEPT_IT"]` | Incident containment steps, forensic RAM imaging, breach notification criteria | Neha Kulkarni (EMP-004, IT) | Sana Khan (EMP-010, DA) |
| `RU-003` | NST-FIN-POL-001 | Section 5: Finance Audit Controls and Fraud Detection Procedures | `FINANCE_ONLY` | `["GRP_DEPT_FIN"]` | Fraud detection red flags, 15% random audit algorithm, 100% forensic audit thresholds | Arjun Bhat (EMP-011, FIN) | Rahul Sethi (EMP-013, SCS) |

