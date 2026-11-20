# OnboardIQ — Northstar Technologies Knowledge Base

**DEMONSTRATION ONLY — NOT APPROVED FOR REAL-WORLD USE**

## 1. Overview
This repository contains the complete, internally consistent fictional corporate knowledge base for **Northstar Technologies**, built to power **OnboardIQ**, an AI-powered employee onboarding and organizational knowledge assistant.

Northstar Technologies is a fictional India-based IT-services company (Head Office: Nagpur, Maharashtra; Branch Offices: Pune, Maharashtra; Bengaluru, Karnataka). The corpus encompasses company policies, technical guidelines, employee directory data, structured ingestion metadata, fail-closed access-control rules, and a comprehensive RAG evaluation benchmark.

## 2. Directory Structure & Inventory

```
/output/
├── 01_master_data/
│   ├── northstar_master_data.json         # Single source of truth for all fictional values & rules
│   └── source_of_truth/
│       └── Northstar_Company_Overview_Employee_Directory.docx  # Verbatim source copy (SHA-256 verified)
├── 02_documents_docx/                      # 15 authoritative corporate policy DOCX files
├── 03_documents_pdf/                       # 15 high-fidelity matching PDF files (ReportLab 4.5.0)
├── 04_registers_and_reports/
│   ├── policy_registry.json & .md          # Formal policy registry with IDs, owners, audiences
│   ├── decision_log.json & .md             # 37 documented architectural decisions with provenance
│   ├── legal_review_register.json & .md    # 8 statutory review items flagged for Indian counsel
│   ├── conflict_and_gap_register.json & .md# Reconciled source conflicts and template dispositions
│   └── traceability_matrix.json & .md      # Complete source-to-document authority mapping
├── 05_rag_metadata/
│   ├── document_manifest.jsonl             # Ingestion manifest for documents
│   ├── section_index.jsonl                 # Section index with heading paths and page boundaries
│   ├── chunk_manifest.jsonl                # 139 structure-preserving chunks with access metadata
│   ├── access_control_specification.md     # Access control architecture & enforcement rules
│   └── access_control_schema.json          # JSON Schema validating access metadata
├── 06_verification/
│   ├── progress.json                       # Live execution and verification status
│   ├── progress_log.md                     # Step-by-step phase execution log
│   ├── verification_log.md                 # Validation and QA log with evidence
│   ├── source_hashes.json                  # SHA-256 hashes of all source inputs
│   ├── pdf_qa_report.json                  # PDF geometry checks and page metrics
│   ├── pdf_visual_qa/                      # 30 rendered PNG screenshots (first/last pages)
│   └── authorizer_test_results.json        # Results from 16 automated authorizer unit tests
├── 07_archive_superseded/
│   ├── superseded_policy_index.json        # Obsolete template values isolated from RAG search
│   └── README.md                           # Governance notes on archived values
├── 08_evaluation/
│   ├── rag_evaluation_dataset.json & .jsonl# 95 verified test queries across 14 categories
│   └── rag_evaluation_summary.md           # Evaluation category breakdown and metrics
├── 09_source_extracts/
│   ├── directory_integrity_report.json     # Full employee directory parse and anomaly audit
│   ├── template_inspection_results.json    # Inspection of all 24 source templates
│   └── template_inspection_summary.md      # Summary of foreign references and template branding
└── README.md                               # This documentation
```

## 3. Document Register

| # | Policy ID | Title | Primary Owner | Target Audience | File Serving Audience | Pages |
|---|---|---|---|---|---|---|
| 1 | `CORP-001` | Company Overview & Employee Directory | Ishita Rao (EMP-002) | `ALL_EMPLOYEES` | `ALL_EMPLOYEES` | 4 |
| 2 | `NST-HR-POL-001` | Employee Handbook | Ishita Rao (EMP-002) | `ALL_EMPLOYEES` | `HR_ONLY` (Mixed) | 4 |
| 3 | `NST-HR-POL-002` | Leave, Attendance & Working Hours Policy | Ishita Rao (EMP-002) | `ALL_EMPLOYEES` | `ALL_EMPLOYEES` | 4 |
| 4 | `NST-HR-POL-003` | Code of Conduct & Workplace Ethics | Ishita Rao (EMP-002) | `ALL_EMPLOYEES` | `ALL_EMPLOYEES` | 3 |
| 5 | `NST-HR-POL-004` | Remote Work & Work From Home Policy | Ishita Rao (EMP-002) | `ALL_EMPLOYEES` | `ALL_EMPLOYEES` | 2 |
| 6 | `NST-HR-POL-005` | Recruitment & Employee Referral Policy | Ishita Rao (EMP-002) | `ALL_EMPLOYEES` | `ALL_EMPLOYEES` | 2 |
| 7 | `NST-HR-POL-006` | Onboarding & Employee Development Policy | Ishita Rao (EMP-002) | `ALL_EMPLOYEES` | `ALL_EMPLOYEES` | 2 |
| 8 | `NST-HR-POL-007` | Performance Review & Promotion Policy | Ishita Rao (EMP-002) | `MANAGERS_AND_HR` | `MANAGERS_AND_HR` | 2 |
| 9 | `NST-IT-POL-001` | Information Security & Acceptable Use Policy | Neha Kulkarni (EMP-004) | `ALL_EMPLOYEES` | `IT_ONLY` (Mixed) | 3 |
| 10 | `NST-IT-GDE-001` | Laptop, Software & Account Setup Guide | Neha Kulkarni (EMP-004) | `ALL_EMPLOYEES` | `ALL_EMPLOYEES` | 2 |
| 11 | `NST-ENG-GDE-001` | Engineering Development Workflow Guide | Ananya Iyer (EMP-006) | `ALL_EMPLOYEES` | `ALL_EMPLOYEES` | 2 |
| 12 | `NST-DA-GDE-001` | Data Handling, Access & Analytics Delivery Guide | Dev Patel (EMP-009) | `ALL_EMPLOYEES` | `ALL_EMPLOYEES` | 2 |
| 13 | `NST-FIN-POL-001` | Expense Reimbursement Policy | Arjun Bhat (EMP-011) | `ALL_EMPLOYEES` | `FINANCE_ONLY` (Mixed) | 3 |
| 14 | `NST-FIN-POL-002` | Business Travel & Travel Expense Policy | Arjun Bhat (EMP-011) | `ALL_EMPLOYEES` | `ALL_EMPLOYEES` | 2 |
| 15 | `NST-IT-GDE-003` | IT Incident Management & Emergency Procedures | Neha Kulkarni (EMP-004) | `ALL_EMPLOYEES` | `ALL_EMPLOYEES` | 2 |

## 4. Directory Integrity & Anomaly Status
- **Directory Integrity Status**: `UNRESOLVED_STRUCTURE`
- **Employee Roster**: 13 employees exactly matching source table rows.
- **Anomalies Documented**:
  - `ANOM-001`: EMP-001 (Aarav Mehta, CEO) has department *Executive Leadership*, which is treated as a corporate tag, not a 7th department.
  - `ANOM-002` to `ANOM-006`: Department heads (EMP-004, EMP-006, EMP-009, EMP-011, EMP-013) report to unlisted C-suite roles (CTO, COO, CFO).
  - `ANOM-007`: Incomplete organizational tree resulting in 6 apparent roots. Per project rules, these roles remain unassigned rather than fabricating employees.

## 5. Restricted Content Units & Access Control
Three restricted units ensure sensitive operational data is protected under fail-closed authorization:
1. `RU-001` (NST-HR-POL-001 Section 13): Disciplinary Action & Termination Procedures (`HR_ONLY`, `GRP_DEPT_HR`).
2. `RU-002` (NST-IT-POL-001 Section 7): Security Incident Response Procedures — Internal Playbook (`IT_ONLY`, `GRP_DEPT_IT`).
3. `RU-003` (NST-FIN-POL-001 Section 5): Finance Audit Controls & Fraud Detection Procedures (`FINANCE_ONLY`, `GRP_DEPT_FIN`).

## 6. RAG Evaluation Dataset
The evaluation dataset contains **95 verified queries** covering 14 distinct testing competencies:
- Exact Lookup, Paraphrase, Employee Lookup, Approval Workflows, Multi-Document Reasoning.
- 4 Dependent Follow-Up Pairs (8 questions total).
- 8 Insufficient Evidence (`NOT_FOUND`) queries.
- 6 Conflicting & Superseded queries.
- 10 Access Control queries (Authorized vs Refusal).
- 4 Chunk-Level Injection/Leak attempts.
- Onboarding, Numeric Lookup, Location Differences, and Demonstration Status queries.

## 7. Limitations & Human Review Requirements
1. **Demonstration Nature**: All documents carry the banner `DEMONSTRATION ONLY — NOT APPROVED FOR REAL-WORLD USE`. No legal validity or production readiness is claimed.
2. **PDF Rebuilt from Source**: Direct native DOCX conversion (via Word COM / docx2pdf) was unavailable in the sandboxed environment. PDFs were built via ReportLab 4.5.0 and inspected visually (`PARTIALLY_VERIFIED`).
3. **Statutory Position**: Indian statutory items (retirements, state leave differences, POSH, gratuity) carry mandatory legal review flags and must be formally verified by qualified legal counsel.
4. **Template Licensing**: Source structural templates from BetterJobs and generic IT manuals were completely rewritten into original Northstar prose. End users must independently verify licensing for third-party templates.
