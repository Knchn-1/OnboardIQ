# Master Data, Source Authority and Governance Rules

## 1. Source authority
Use this precedence:

1. **L1 — Company Overview & Employee Directory DOCX:** employee names, IDs, designations, departments, reporting managers, locations, email addresses and company facts explicitly present.
2. **L2 — Northstar Company Master Data:** fictional company rules, policy values, approval limits, SLAs, role assignments, contact routing, audiences and demonstration status.
3. **L3 — Final documents:** derived from L1/L2 only.
4. **L4 — Downloaded templates:** structural inspiration only; lowest authority.

Never let a lower level override a higher one.

## 2. Directory integrity
- Preserve the original Directory file unchanged and hash it.
- Parse all employee rows and relevant fields, including table continuations and merged cells.
- Retain verbatim source columns; put normalization in separate derived columns.
- Detect duplicate IDs/emails, malformed values, missing managers, cycles, self-reporting, orphaned employees, inconsistent departments/locations and multiple roots.
- Record each anomaly with evidence, affected employee IDs, severity, proposed resolution and `PROPOSED, awaiting human approval`.
- Never silently repair employee or reporting data.
- Integrity status must be one of:
  - `CLEAN`
  - `FLAGGED`
  - `UNRESOLVED_STRUCTURE`
  - `NOT_YET_ASSESSED`
- Do not call organizational structure verified unless status is `CLEAN`.

## 3. Provenance tags
Every Master Data value and decision must use exactly one:
- `DIR` — copied from Directory.
- `TEMPLATE-ADAPTED` — adapted from a template and linked to a decision.
- `FICTIONAL-DECISION` — newly created fictional rule/value and linked to a decision.
- `STATUTORY-FLAGGED` — fictional company rule touching a legal/regulatory topic; link to a decision and Legal Review Register entry.

## 4. Decision log
For each decision record:
- Decision ID;
- topic/key;
- question or gap;
- source evidence;
- options considered;
- chosen decision;
- rationale;
- provenance tag;
- affected documents/sections;
- legal-review flag;
- date and status.

Every invented threshold, date, amount, role assignment, mailbox, SLA, leave rule, working-hour rule, security parameter or approval path must be defined once in Master Data and referenced from there.

## 5. Master Data design
Create a workbook or structured set of files with, at minimum:
- Company_Profile
- Departments
- Offices
- Employee_Directory_Source (verbatim source fields)
- Employee_Directory_Derived (separate normalized fields only)
- Role_Assignments
- Policy_Values
- Leave_and_Attendance
- Working_Hours
- Remote_Work
- Approval_Authority_Matrix
- Expense_Limits
- Travel_Rules
- Referral_Rules
- IT_Security_Parameters
- Incident_SLA
- Systems_and_Tools
- Access_Control_Matrix
- Restricted_Units
- Corporate_Codes (only if justified; not a department)
- Legal_Review_Register
- Decision_Log
- Superseded_Values

Include the canonical demonstration label exactly:
`DEMONSTRATION ONLY — NOT APPROVED FOR REAL-WORLD USE`

Keep document status, lifecycle state and verification status as separate fields.

## 6. Indian legal context
Do not state statutory figures, section numbers, penalties or legal interpretations unless independently verified by qualified counsel (not part of this task). For topics such as leave, hours, overtime, POSH, social security, gratuity, minimum wages, privacy/data protection, tax treatment, termination and contractors:
1. state only the fictional Northstar company rule;
2. add: “Statutory position to be verified by qualified legal/HR counsel before real-world use.”;
3. add a Legal Review Register entry identifying the topic and appropriate reviewer.

Flag Maharashtra/Karnataka variation rather than assuming one rule applies everywhere.

## 7. Template use and originality
- Inspect every template; filenames may not match contents.
- Remove foreign legal references, old technology references and template branding.
- Rewrite in original Northstar wording.
- Record each source's use/disposition.
- Run similarity checks with common corporate phrases allowlisted narrowly.
- Flag suspicious similarity for human review; do not treat a similarity score as proof of infringement.
- Record that the user must verify source-template licensing.
