# Document Requirements

## 1. Target corpus
Create 12–15 substantive documents. Consolidation is allowed where it improves clarity, but do not drop a source topic without recording its disposition and ensuring relevant employee questions remain answerable.

Recommended target set:

| # | Document | Primary owner domain |
|---|---|---|
| 1 | Company Overview & Employee Directory | Corporate reference |
| 2 | Employee Handbook | HR |
| 3 | Leave, Attendance & Working Hours Policy | HR |
| 4 | Remote Work & Work From Home Policy | HR |
| 5 | Code of Conduct & Workplace Ethics | HR |
| 6 | Recruitment & Employee Referral Policy | HR |
| 7 | Onboarding & Employee Development Policy | HR |
| 8 | Performance Review & Promotion Policy | HR |
| 9 | Information Security & Acceptable Use Policy | IT |
| 10 | Laptop, Software & Account Setup Guide | IT |
| 11 | Engineering Development Workflow, Git & Code Review Guide | ENG |
| 12 | Data Handling, Access & Analytics Delivery Guide | DA |
| 13 | Expense Reimbursement Policy | FIN |
| 14 | Business Travel & Travel Expense Policy | FIN |
| 15 | IT Incident Management & Emergency Procedures | IT |

If the company Directory or available sources make a named owner impossible, record the owner as unassigned/flagged rather than inventing a person.

## 2. Document structure
Use a consistent, professional layout. As relevant, each document should include:
- first-page demonstration banner;
- document title and unique Policy ID;
- version and lifecycle state;
- document owner and designated approver (fictional role);
- document audience;
- purpose and scope;
- definitions;
- roles and responsibilities;
- policy rules or procedure;
- workflow/approval matrix where applicable;
- exceptions and escalation;
- related documents;
- revision history;
- employee FAQs;
- statutory verification note where required.

Do not force irrelevant sections into every document. Avoid empty sections and filler.

## 3. IDs and naming
Use Policy IDs in the form `NST-<DEPT>-<TYPE>-<NNN>`, where `<DEPT>` is one of `HR`, `IT`, `ENG`, `DA`, `FIN`, `SCS` and corresponds to the Policy Owner's department. Define document-number mapping before drafting. Use stable IDs and section keys.

Suggested filenames:
`NST-HR-POL-001_Employee_Handbook_v1.0.docx`

Use the actual assigned ID and title in all metadata and citations.

## 4. Writing standard
- Indian English and INR (`₹`) where appropriate.
- Clear, professional language suitable for employees.
- Use actionable instructions and define terms.
- State who performs each step, when, how and where escalation goes.
- Use tables for thresholds, responsibilities and workflows.
- Keep each section self-contained for retrieval.
- Avoid vague phrases such as “as per management discretion” unless the decision process is actually defined.
- Never leave placeholders, template boilerplate or unresolved tokens in final files.

## 5. Realism and fictional values
Reasonable fictional company rules may be created when sources are silent. Every such value must first be defined in Master Data and logged. Ensure consistency across documents. Do not present fictional values as statutory minima or legal requirements.

## 6. Restricted content
At least three meaningful sections/units should have restricted audiences (for example HR case handling, IT security response details, finance approval controls). Keep restricted facts out of broader-audience documents, FAQs and chunks. Each restricted unit must have a clear business reason and test cases for authorized and unauthorized personas.

## 7. FAQs and competency coverage
Each document should include useful, non-duplicative employee FAQs where appropriate. Create a competency map linking employee questions to the exact document section that answers them. Use questions that test exact lookup, paraphrase, multi-step procedure, numeric/table lookup, follow-up, insufficient evidence and access denial.

## 8. PDF expectations
Prefer converting the actual final DOCX to PDF using a reliable converter. Record tool and version. If the PDF must be rebuilt separately from source text, label it `REBUILT_FROM_SOURCE`; do not call it equivalent to a DOCX conversion and do not mark it fully verified.
