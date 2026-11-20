# Northstar Technologies — Architecture Decision Log

**DEMONSTRATION ONLY — NOT APPROVED FOR REAL-WORLD USE**

| Decision ID | Topic | Question / Gap | Chosen Resolution | Provenance | Affected Docs | Status |
|---|---|---|---|---|---|---|
| DEC-001 | Missing C-suite roles | CTO, COO, CFO titles referenced as reporting managers but no employees listed | Leave unassigned, flag hierarchy as UNRESOLVED_STRUCTURE | `DIR` | `All documents referencing org hierarchy` | FINAL |
| DEC-002 | POSH IC Chairperson | Who chairs the Internal Committee? | Leave unassigned with functional mailbox posh.committee@northstar.example | `FICTIONAL-DECISION` | `['NST-HR-POL-003']` | FINAL |
| DEC-003 | Information Security Officer | Who is responsible for information security? | Assign dual-hat to IT Manager (EMP-004, Neha Kulkarni) | `FICTIONAL-DECISION` | `['NST-IT-POL-001', 'NST-IT-GDE-003']` | FINAL |
| DEC-004 | Probation and Notice Periods | What are the probation and notice periods? | 6-month probation, 30-day notice (probation), 60-day notice (confirmed) | `FICTIONAL-DECISION` | `['NST-HR-POL-001']` | FINAL |
| DEC-005 | Retirement Age | What is the company retirement age? | 60 years | `STATUTORY-FLAGGED` | `['NST-HR-POL-001']` | FINAL |
| DEC-006 | Dress Code | What is the dress code? | Business casual, formal for client meetings | `FICTIONAL-DECISION` | `['NST-HR-POL-001', 'NST-HR-POL-003']` | FINAL |
| DEC-007 | Pay Cycle | When is salary paid? | Last working day of each calendar month | `FICTIONAL-DECISION` | `['NST-HR-POL-001']` | FINAL |
| DEC-008 | Leave Entitlements | How many leave days per type? | CL:12, SL:12, EL:15 per year, carry-forward 5 days, leave year Jan-Dec | `FICTIONAL-DECISION` | `['NST-HR-POL-002']` | FINAL |
| DEC-009 | Maternity/Paternity Leave | What parental leave is offered? | 26 weeks maternity, 5 days paternity (company benefit) | `STATUTORY-FLAGGED` | `['NST-HR-POL-002']` | FINAL |
| DEC-010 | Bereavement and Comp-off | Bereavement leave days? Comp-off validity? | 5 days bereavement, 30-day comp-off validity | `FICTIONAL-DECISION` | `['NST-HR-POL-002']` | FINAL |
| DEC-011 | Leave Approval Chain | Who approves leave? | Manager for ≤3 days; Manager + HR for >3 consecutive days | `FICTIONAL-DECISION` | `['NST-HR-POL-002']` | FINAL |
| DEC-012 | Attendance Rules | Attendance marking and grace period? | Daily HRMS marking by 10:30 AM, 15-min grace, 3-day unauthorized absence threshold | `FICTIONAL-DECISION` | `['NST-HR-POL-002']` | FINAL |
| DEC-013 | Working Hours | Standard working hours? | 9h/day (incl. 1h lunch), 45h/week, Mon-Fri, core 10AM-7PM, flex 9-10:30AM | `FICTIONAL-DECISION` | `['NST-HR-POL-002']` | FINAL |
| DEC-014 | Overtime Compensation | How is overtime compensated? | Comp-off within 30 days; no direct overtime pay by default | `FICTIONAL-DECISION` | `['NST-HR-POL-002']` | FINAL |
| DEC-015 | Remote Work Policy | Remote work rules? | Max 2 days/week remote for confirmed employees, manager-approved, full remote exceptional | `FICTIONAL-DECISION` | `['NST-HR-POL-004']` | FINAL |
| DEC-016 | Expense Approval Thresholds | Expense claim approval levels? | ≤₹5K: Manager; ₹5K-₹25K: Dept Head + Finance; >₹25K: Dept Head + Finance + CEO | `FICTIONAL-DECISION` | `['NST-FIN-POL-001']` | FINAL |
| DEC-017 | Travel Approval | Travel request approval? | Domestic: Manager + Finance; International: Dept Head + Finance + CEO | `FICTIONAL-DECISION` | `['NST-FIN-POL-002']` | FINAL |
| DEC-018 | Software Purchase Approval | Who approves software purchases? | ≤₹10K: IT Manager; >₹10K: IT Manager + Finance Manager | `FICTIONAL-DECISION` | `['NST-IT-GDE-001']` | FINAL |
| DEC-019 | Hiring Approval | Who approves new hires? | Department Head + HR + CEO | `FICTIONAL-DECISION` | `['NST-HR-POL-005']` | FINAL |
| DEC-020 | Promotion Approval | Who approves promotions? | Manager + Dept Head + HR + CEO | `FICTIONAL-DECISION` | `['NST-HR-POL-007']` | FINAL |
| DEC-021 | Policy Exception Process | How are policy exceptions handled? | Department Head + HR + CEO | `FICTIONAL-DECISION` | `['All policies']` | FINAL |
| DEC-022 | Meal and Transport Allowances | Daily meal and transport limits? | ₹500 daily meal, ₹1,500 local transport per trip, ₹500/month mobile | `FICTIONAL-DECISION` | `['NST-FIN-POL-001']` | FINAL |
| DEC-023 | Expense Claim Deadlines | Claim submission and processing timelines? | 30-day submission deadline, receipt >₹250, 15 working days processing | `FICTIONAL-DECISION` | `['NST-FIN-POL-001']` | FINAL |
| DEC-024 | Travel Class and Hotel Limits | Travel class and per-night hotel rates? | Economy (business >4h with approval), Hotel: ₹5K metro/₹3.5K non-metro, Diem: ₹1.5K/₹1K | `FICTIONAL-DECISION` | `['NST-FIN-POL-002']` | FINAL |
| DEC-025 | Travel Advance and Settlement | Travel advance and settlement rules? | 80% advance max, 7-day advance request lead, 7 working days settlement deadline | `FICTIONAL-DECISION` | `['NST-FIN-POL-002']` | FINAL |
| DEC-026 | Employee Referral Bonus | Referral bonus amount and rules? | ₹15,000 after 6-month completion, max 5 per quarter, HR/hiring managers excluded | `FICTIONAL-DECISION` | `['NST-HR-POL-005']` | FINAL |
| DEC-027 | Password Policy | Password length, expiry, MFA? | 12-char minimum, 90-day expiry, MFA required for all systems | `FICTIONAL-DECISION` | `['NST-IT-POL-001']` | FINAL |
| DEC-028 | USB and BYOD Policy | USB and personal device rules? | USB disabled by default (IT exception), BYOD requires MDM enrollment | `FICTIONAL-DECISION` | `['NST-IT-POL-001']` | FINAL |
| DEC-029 | VPN Requirement | VPN for remote work? | Required for all remote access | `FICTIONAL-DECISION` | `['NST-IT-POL-001', 'NST-HR-POL-004']` | FINAL |
| DEC-030 | Data Classification | Data classification levels? | Public, Internal, Confidential, Restricted | `FICTIONAL-DECISION` | `['NST-IT-POL-001', 'NST-DA-GDE-001']` | FINAL |
| DEC-031 | Security Incident Reporting | Incident reporting channel? | security@northstar.example, escalation IT Manager → HR → CEO | `FICTIONAL-DECISION` | `['NST-IT-POL-001', 'NST-IT-GDE-003']` | FINAL |
| DEC-032 | Incident SLA | Response and resolution SLAs? | P1: 30min/4h, P2: 1h/8h, P3: 4h/24h, P4: 8h/48h | `FICTIONAL-DECISION` | `['NST-IT-GDE-003']` | FINAL |
| DEC-033 | Internal Systems and Tools | Which tools does the company use? | HRMS, GitLab, Jira, Confluence, Slack, Google Workspace, VPN, Expense Portal | `FICTIONAL-DECISION` | `['NST-IT-GDE-001', 'NST-ENG-GDE-001']` | FINAL |
| DEC-034 | Restricted Unit: Disciplinary Procedures | Should disciplinary action details be HR-only? | HR_ONLY | `FICTIONAL-DECISION` | `['NST-HR-POL-001']` | FINAL |
| DEC-035 | Restricted Unit: Security Incident Playbook | Should incident response playbook be IT-only? | IT_ONLY | `FICTIONAL-DECISION` | `['NST-IT-POL-001']` | FINAL |
| DEC-036 | Restricted Unit: Finance Audit Controls | Should fraud detection criteria be Finance-only? | FINANCE_ONLY | `FICTIONAL-DECISION` | `['NST-FIN-POL-001']` | FINAL |
| DEC-037 | Executive Leadership classification | Is Executive Leadership a 7th department? | Classification tag only; not a department. EMP-001 is in GRP_ALL_EMPLOYEES but no department group. | `FICTIONAL-DECISION` | `['All documents']` | FINAL |
