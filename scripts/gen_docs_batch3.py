"""
Phase 5: Generate Batch 3 Northstar Technologies policy/guide DOCX documents.
Documents 9 to 12:
  - NST-IT-GDE-001: Laptop, Software & Account Setup Guide
  - NST-ENG-GDE-001: Engineering Development Workflow, Git & Code Review Guide
  - NST-DA-GDE-001: Data Handling, Access & Analytics Delivery Guide
  - NST-FIN-POL-001: Expense Reimbursement Policy (with RU-003 FINANCE_ONLY section)
"""
import json
import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUTPUT_DIR = "knowledge_base/02_documents_docx"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open("knowledge_base/01_master_data/northstar_master_data.json", "r", encoding="utf-8") as f:
    MD = json.load(f)

DEMO_LABEL = MD["_metadata"]["demonstration_label"]
STAT_NOTE = MD["_metadata"]["statutory_note"]
VERSION = "1.0"
EFF_DATE = "01 November 2026"

def add_demo_banner(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(DEMO_LABEL)
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

def add_title_block(doc, policy_id, title, owner, approver, audience, version=VERSION, eff_date=EFF_DATE):
    doc.add_heading(title, level=0)
    table = doc.add_table(rows=7, cols=2)
    table.style = "Table Grid"
    cells = [
        ("Policy ID", policy_id),
        ("Version", version),
        ("Effective Date", eff_date),
        ("Document Owner", owner),
        ("Designated Approver", approver),
        ("Audience", audience),
        ("Lifecycle State", "CURRENT"),
    ]
    for i, (label, value) in enumerate(cells):
        table.rows[i].cells[0].text = label
        table.rows[i].cells[1].text = value
        for cell in table.rows[i].cells:
            for paragraph in cell.paragraphs:
                paragraph.style.font.size = Pt(10)
    doc.add_paragraph()

def add_revision_history(doc, policy_id):
    doc.add_heading("Revision History", level=2)
    table = doc.add_table(rows=2, cols=4)
    table.style = "Table Grid"
    headers = ["Version", "Date", "Author", "Description"]
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
    table.rows[1].cells[0].text = "1.0"
    table.rows[1].cells[1].text = EFF_DATE
    table.rows[1].cells[2].text = "Northstar Technologies"
    table.rows[1].cells[3].text = "Initial release (demonstration version)"

def add_statutory_note(doc):
    p = doc.add_paragraph()
    run = p.add_run("Note: " + STAT_NOTE)
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x88, 0x00, 0x00)

def add_demo_footer(doc):
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("— End of Document —")
    run.italic = True
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run(DEMO_LABEL)
    run2.bold = True
    run2.font.size = Pt(9)
    run2.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

def save_doc(doc, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    doc.save(path)
    print(f"  Created: {path}")
    return path

# ============================================================================
# DOCUMENT 9: Laptop, Software & Account Setup Guide (NST-IT-GDE-001)
# ============================================================================
def build_laptop_software_guide():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-IT-GDE-001", "Laptop, Software & Account Setup Guide",
                    "Neha Kulkarni, IT Manager (EMP-004)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This guide provides step-by-step instructions for onboarding employees on device configuration, standard software "
        "installations, corporate account provisioning, and software procurement approval workflows at Northstar Technologies. "
        "It applies to all personnel across Nagpur, Pune, and Bengaluru offices.")

    doc.add_heading("2. Standard Hardware Provisioning", level=1)
    doc.add_paragraph(
        "Upon joining, every employee is issued a standardized corporate workstation calibrated to their departmental needs:")
    table_hw = doc.add_table(rows=3, cols=3)
    table_hw.style = "Table Grid"
    hw_data = [
        ("Department Track", "Standard Configuration", "Operating System"),
        ("Engineering (ENG) & Data (DA)", "Intel Core i7/AMD Ryzen 7, 32 GB RAM, 1 TB NVMe SSD", "Ubuntu Linux LTS or macOS Enterprise"),
        ("HR, Finance, SCS & Operations", "Intel Core i5/AMD Ryzen 5, 16 GB RAM, 512 GB NVMe SSD", "Windows 11 Enterprise or macOS"),
    ]
    for i, row in enumerate(hw_data):
        for j, val in enumerate(row):
            table_hw.rows[i].cells[j].text = val
    doc.add_paragraph()
    doc.add_paragraph(
        "All workstations are pre-configured with full disk encryption (BitLocker / FileVault / LUKS), centralized MDM agents, "
        "and automated security patch management managed by IT Support Specialist Kabir Shah (EMP-005).")

    doc.add_heading("3. Corporate Account Provisioning and Setup", level=1)
    doc.add_paragraph(
        "New employees receive access to core collaboration platforms during their Day One onboarding session:")
    acc_items = [
        ("Google Workspace (workspace.google.example):", "Single sign-on (SSO) email, calendar, Google Drive, and Meet."),
        ("Slack (northstar.slack.example):", "Real-time communication, announcement channels (#announcements, #general), and departmental channels."),
        ("HRMS Portal (hrms.northstar.example):", "Daily attendance marking, leave management, and monthly payslips."),
        ("GitLab (gitlab.northstar.example):", "Engineering source repositories and CI/CD pipelines (for ENG and DA staff)."),
        ("Jira & Confluence (jira.northstar.example):", "Agile task tracking, sprint planning, and corporate knowledge base."),
        ("WireGuard VPN (vpn.northstar.example):", "Secure gateway connection required for all remote access."),
    ]
    for name, desc in acc_items:
        p = doc.add_paragraph()
        run = p.add_run(name + " ")
        run.bold = True
        p.add_run(desc)

    doc.add_heading("4. Software Procurement and Installation Rules", level=1)
    doc.add_heading("4.1 Pre-Approved Software Catalog", level=2)
    doc.add_paragraph(
        "Employees may install pre-approved development and productivity packages (VS Code, Docker Desktop, PyCharm CE, "
        "Postman, DBeaver, Google Chrome, LibreOffice) via the company software portal without separate approval.")

    doc.add_heading("4.2 Commercial Software Purchase Approvals", level=2)
    doc.add_paragraph(
        "Purchasing commercial software licenses, cloud SaaS subscriptions, or specialized development tools requires "
        "structured sign-off based on expenditure thresholds defined in the Master Data Approval Authority Matrix:")
    table_soft = doc.add_table(rows=3, cols=3)
    table_soft.style = "Table Grid"
    soft_data = [
        ("Expenditure Level", "Approval Requirement", "Workflow"),
        ("Up to ₹10,000", "IT Manager Approval", "Submit Jira Service Desk ticket to Neha Kulkarni (EMP-004)"),
        ("Above ₹10,000", "IT Manager + Finance Manager Approval", "Joint authorization by Neha Kulkarni and Arjun Bhat (EMP-011)"),
    ]
    for i, row in enumerate(soft_data):
        for j, val in enumerate(row):
            table_soft.rows[i].cells[j].text = val

    doc.add_heading("5. IT Support and Troubleshooting Contacts", level=1)
    doc.add_paragraph(
        "For device malfunctions, access lockouts, or hardware replacement requests:")
    support_items = [
        "Primary Contact: Kabir Shah, IT Support Specialist (EMP-005) at it.support@northstar.example / kabir.shah@northstar.example.",
        "Escalation Contact: Neha Kulkarni, IT Manager (EMP-004) at neha.kulkarni@northstar.example.",
        "Slack Channel: #it-helpdesk for live support during core hours (10:00 AM – 7:00 PM).",
    ]
    for si in support_items:
        doc.add_paragraph(si, style="List Bullet")

    doc.add_heading("6. Related Documents", level=1)
    for ref in ["NST-IT-POL-001 — Information Security & Acceptable Use Policy",
                "NST-IT-GDE-003 — IT Incident Management & Emergency Procedures",
                "NST-HR-POL-006 — Onboarding & Employee Development Policy"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("7. Frequently Asked Questions", level=1)
    faqs = [
        ("Can I request administrative (root/sudo) access on my developer laptop?", "Yes, engineering and data team members are granted managed sudo privileges upon completing security onboarding."),
        ("What is the approval process for a paid software subscription under ₹10,000?", "Submit a Jira Service Desk request citing business need and pricing; it requires sign-off from IT Manager Neha Kulkarni."),
        ("What should I do if my laptop is damaged or stops booting?", "Immediately report the issue to Kabir Shah via it.support@northstar.example or #it-helpdesk. A replacement device will be dispatched or provisioned from the nearest office."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-IT-GDE-001")
    add_demo_footer(doc)
    return save_doc(doc, "NST-IT-GDE-001_Laptop_Software_Setup_v1.0.docx")

# ============================================================================
# DOCUMENT 10: Engineering Development Workflow, Git & Code Review Guide (NST-ENG-GDE-001)
# ============================================================================
def build_engineering_guide():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-ENG-GDE-001", "Engineering Development Workflow, Git & Code Review Guide",
                    "Ananya Iyer, Engineering Manager (EMP-006)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This guide defines technical development standards, version control branching conventions, code review criteria, "
        "continuous integration/continuous deployment (CI/CD) pipelines, and production release procedures at Northstar "
        "Technologies. It governs all software engineering activities across Nagpur, Pune, and Bengaluru.")

    doc.add_heading("2. Git Repository & Branching Strategy", level=1)
    doc.add_paragraph(
        "Northstar uses enterprise GitLab (gitlab.northstar.example) for source code hosting. Teams follow a standardized "
        "Git branching model:")
    branches = [
        ("main / production:", "Represents production-ready code. Direct commits and force pushes are strictly disabled. Changes enter solely via merged pull/merge requests."),
        ("release/*:", "Release staging branches for final system testing, QA sign-off, and hotfix stabilization before scheduled deployment."),
        ("develop:", "Active development branch for integrated feature testing across sprint iterations."),
        ("feature/*:", "Individual feature work branches created from develop. Named according to convention: feature/JIRA-123-short-description."),
        ("hotfix/*:", "Urgent production patch branches branched directly from main, requiring expedited manager approval."),
    ]
    for b_title, b_desc in branches:
        p = doc.add_paragraph()
        run = p.add_run(b_title + " ")
        run.bold = True
        p.add_run(b_desc)

    doc.add_heading("3. Merge Request (MR) & Code Review Protocol", level=1)
    doc.add_paragraph(
        "High software quality and security require rigorous peer review. Every Merge Request must meet these criteria before merging:")
    mr_rules = [
        "Peer Review Approval: At least one mandatory approving review from a designated senior engineer (Vikram Joshi EMP-007, Mira Nair EMP-008, or Engineering Manager Ananya Iyer EMP-006).",
        "Automated CI Validation: All automated pipeline checks (unit tests, static linting, security scans) must pass completely with green status.",
        "Test Coverage Threshold: Code changes must demonstrate at least 80% automated test coverage for new business logic.",
        "No Sensitive Credentials: Zero embedded secrets, API keys, or plaintext connection strings (verified via pre-commit trufflehog/gitleaks scan).",
        "Commit Standards: Clear, conventional commit messages referencing active Jira issue tickets (e.g., 'feat(auth): add MFA session validation #NST-452').",
    ]
    for r in mr_rules:
        doc.add_paragraph(r, style="List Bullet")

    doc.add_heading("4. CI/CD and Release Deployment Procedures", level=1)
    doc.add_heading("4.1 Deployment Environments", level=2)
    doc.add_paragraph("Software progresses through three isolated deployment tiers:")
    env_tiers = [
        ("Development (Dev):", "Continuous deployment triggered on every merge into develop branch."),
        ("Staging (UAT):", "Automated deployment from release/* branches for stakeholder verification and load testing."),
        ("Production (Prod):", "Scheduled releases approved by Engineering Manager Ananya Iyer during approved maintenance windows."),
    ]
    for et, ed in env_tiers:
        p = doc.add_paragraph()
        run = p.add_run(et + " ")
        run.bold = True
        p.add_run(ed)

    doc.add_heading("4.2 Production Release Windows & Rollback", level=2)
    doc.add_paragraph(
        "Production releases are scheduled on Tuesday and Thursday mornings between 06:00 AM and 08:00 AM IST to minimize "
        "customer disruption. Deployments on Friday afternoons or preceding public holidays are strictly prohibited without "
        "written CEO exception. Every production deployment must include an automated, tested rollback script and an on-call "
        "incident lead.")

    doc.add_heading("5. Technical Documentation Standards", level=1)
    doc.add_paragraph(
        "Engineers must maintain up-to-date architectural documentation in Confluence and generate API interface specs "
        "following OpenAPI (Swagger) specifications. Readme files must document local container setup and test execution steps.")

    doc.add_heading("6. Related Documents", level=1)
    for ref in ["NST-IT-POL-001 — Information Security & Acceptable Use Policy",
                "NST-DA-GDE-001 — Data Handling, Access & Analytics Delivery Guide",
                "NST-IT-GDE-003 — IT Incident Management & Emergency Procedures"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("7. Frequently Asked Questions", level=1)
    faqs = [
        ("Who can approve my Merge Request?", "Any designated peer engineer (such as Vikram Joshi or Mira Nair) or Engineering Manager Ananya Iyer."),
        ("What is the minimum unit test coverage required?", "All new code and modified business logic must maintain at least 80% automated unit test coverage."),
        ("Can we deploy to production on Friday?", "No. Production releases are restricted to Tuesday and Thursday maintenance windows (06:00 AM – 08:00 AM IST) to prevent weekend incidents."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-ENG-GDE-001")
    add_demo_footer(doc)
    return save_doc(doc, "NST-ENG-GDE-001_Engineering_Workflow_v1.0.docx")

# ============================================================================
# DOCUMENT 11: Data Handling, Access & Analytics Delivery Guide (NST-DA-GDE-001)
# ============================================================================
def build_data_analytics_guide():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-DA-GDE-001", "Data Handling, Access & Analytics Delivery Guide",
                    "Dev Patel, Data & Analytics Manager (EMP-009)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This guide defines protocols for accessing corporate and client data repositories, developing analytical pipelines, "
        "ensuring data quality and privacy compliance, and publishing business intelligence dashboards at Northstar Technologies. "
        "It governs all data engineering and business analytics operations across Nagpur, Pune, and Bengaluru.")

    doc.add_heading("2. Data Access Governance & Role-Based Access Control (RBAC)", level=1)
    doc.add_paragraph(
        "Data repository access is governed strictly under least-privilege RBAC principles:")
    table_access = doc.add_table(rows=4, cols=3)
    table_access.style = "Table Grid"
    da_access = [
        ("Environment / Tier", "Permitted Access Level", "Authorization Required"),
        ("Development & Staging Data", "Read-Write with synthetic/anonymized data only", "Assigned Project Team Lead"),
        ("Production Analytics Warehouse", "Read-Only queried via service account", "Data & Analytics Manager Dev Patel (EMP-009)"),
        ("Production Raw Customer Data", "Strictly Restricted / Direct access prohibited", "Dev Patel + IT Manager Neha Kulkarni + CEO"),
    ]
    for i, row in enumerate(da_access):
        for j, val in enumerate(row):
            table_access.rows[i].cells[j].text = val
    doc.add_paragraph()
    doc.add_paragraph(
        "Direct export of customer datasets to personal workstations or unmanaged cloud storage is strictly prohibited.")

    doc.add_heading("3. Personally Identifiable Information (PII) Protection & Anonymization", level=1)
    doc.add_paragraph(
        "Under India's Digital Personal Data Protection Act, 2023 (DPDP) and corporate privacy standards, all datasets "
        "used in analytics, model training, or QA testing must undergo cryptographic tokenization or masking:")
    pii_rules = [
        "Masking Protocols: Phone numbers, email handles, and national identifiers (Aadhaar, PAN) must be SHA-256 hashed or dynamic-masked.",
        "Synthetic Data Generation: Analytics pipelines in non-production environments must utilize synthetic data generated via approved scripts.",
        "Data Retention & Purging: Temporary staging tables containing sensitive raw extracts must automatically purge after 14 calendar days.",
    ]
    for pr in pii_rules:
        doc.add_paragraph(pr, style="List Bullet")
    add_statutory_note(doc)

    doc.add_heading("4. Data Pipeline Engineering & Quality Assurance", level=1)
    doc.add_paragraph(
        "Data pipelines (ELT/ETL) authored by Data Analysts (such as Sana Khan EMP-010) and engineers must conform to "
        "standard automated validation checkpoints:")
    qa_checkpoints = [
        "Schema Validation: Automated schema checking on ingress to reject malformed records.",
        "Null Rate Tolerances: Critical business keys must maintain 0% null tolerance; non-critical attributes must alert if nulls exceed 5%.",
        "Idempotency: All extraction and transformation pipelines must be strictly idempotent to allow seamless replay without duplicate records.",
        "Lineage Documentation: Data transformations and business definitions must be cataloged in the centralized Confluence data dictionary.",
    ]
    for qc in qa_checkpoints:
        doc.add_paragraph(qc, style="List Bullet")

    doc.add_heading("5. Dashboard Delivery and Client Reporting", level=1)
    doc.add_paragraph(
        "Customer-facing reporting dashboards and analytical insights delivered to external stakeholders require peer review "
        "by Sana Khan (EMP-010) and formal sign-off from Data & Analytics Manager Dev Patel (EMP-009) prior to deployment.")

    doc.add_heading("6. Related Documents", level=1)
    for ref in ["NST-IT-POL-001 — Information Security & Acceptable Use Policy",
                "NST-ENG-GDE-001 — Engineering Development Workflow Guide",
                "NST-HR-POL-003 — Code of Conduct & Workplace Ethics"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("7. Frequently Asked Questions", level=1)
    faqs = [
        ("Can I query production customer databases directly from my laptop?", "No. Direct connection to production databases from developer laptops is prohibited. Queries must execute through secure analytics warehouses with role-based masking."),
        ("Who approves access to internal analytics platforms?", "Data & Analytics Manager Dev Patel (EMP-009) reviews and authorizes all internal analytics warehouse access requests."),
        ("How long are temporary staging tables retained?", "Temporary pipeline staging tables are automatically purged after 14 days."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-DA-GDE-001")
    add_demo_footer(doc)
    return save_doc(doc, "NST-DA-GDE-001_Data_Handling_Guide_v1.0.docx")

# ============================================================================
# DOCUMENT 12: Expense Reimbursement Policy (NST-FIN-POL-001)
# ============================================================================
def build_expense_policy():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-FIN-POL-001", "Expense Reimbursement Policy",
                    "Arjun Bhat, Finance Manager (EMP-011)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES (Sections marked FINANCE_ONLY are restricted)")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This policy defines allowable business expenses, reimbursable thresholds, submission deadlines, receipt requirements, "
        "and approval matrices for employees incurring valid business expenditures on behalf of Northstar Technologies. "
        "It applies to all personnel across Nagpur, Pune, and Bengaluru.")

    doc.add_heading("2. Allowable Expenses and Standard Reimbursable Limits", level=1)
    doc.add_paragraph(
        "Expenditures incurred strictly in the course of company business are reimbursable according to the Master Data limits:")
    table_limits = doc.add_table(rows=5, cols=3)
    table_limits.style = "Table Grid"
    exp_limits = [
        ("Expense Category", "Standard Limit (INR)", "Conditions & Documentation"),
        ("Daily Meal Allowance", "₹500 per day", "Valid during authorized overtime (>2 hours past shift) or official off-site client duty"),
        ("Local Business Transport", "₹1,500 per trip", "App-based cabs (Ola/Uber) or pre-paid taxis for official client visits; receipt required"),
        ("Mobile / Internet Reimbursement", "₹500 per month", "For eligible client-facing, on-call, and managerial roles; monthly bill copy required"),
        ("Client Entertainment / Meals", "Subject to pre-approval", "Requires prior written email sign-off from Department Head citing client name and objective"),
    ]
    for i, row in enumerate(exp_limits):
        for j, val in enumerate(row):
            table_limits.rows[i].cells[j].text = val

    doc.add_heading("3. Claim Submission Deadlines and Receipt Verification", level=1)
    doc.add_paragraph(
        "Employees must adhere strictly to documentation and filing schedules:")
    rules = [
        "Filing Window: Expense claims must be submitted via the Expense Portal (expenses.northstar.example) within 30 calendar days of incurring the expenditure. Claims submitted beyond 30 days are automatically rejected.",
        "Receipt Mandate: Original itemized tax invoices or digital receipts are mandatory for all individual expense line items exceeding ₹250.",
        "Payment Processing SLA: Validated and approved reimbursement claims are disbursed within 15 working days directly to the employee's registered payroll bank account.",
    ]
    for r in rules:
        doc.add_paragraph(r, style="List Bullet")

    doc.add_heading("4. Approval Authority Matrix for Expenses", level=1)
    doc.add_paragraph(
        "Expense approval follows tiered authorization thresholds defined in the company Master Data:")
    table_app = doc.add_table(rows=4, cols=2)
    table_app.style = "Table Grid"
    app_data = [
        ("Claim Amount Tier", "Required Approval Authority"),
        ("Up to ₹5,000", "Reporting Manager Approval"),
        ("₹5,001 to ₹25,000", "Department Head + Finance Manager (Arjun Bhat, EMP-011)"),
        ("Above ₹25,000", "Department Head + Finance Manager (Arjun Bhat) + CEO (Aarav Mehta, EMP-001)"),
    ]
    for i, row in enumerate(app_data):
        for j, val in enumerate(row):
            table_app.rows[i].cells[j].text = val

    # RESTRICTED UNIT 3: RU-003
    doc.add_heading("5. Finance Audit Controls and Fraud Detection Procedures", level=1)
    p_rest = doc.add_paragraph()
    run_rest = p_rest.add_run("ACCESS RESTRICTION: This section is classified FINANCE_ONLY. "
                              "Only members of the Finance & Administration department (GRP_DEPT_FIN) may access this content.")
    run_rest.bold = True
    run_rest.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

    doc.add_heading("5.1 Fraud Detection Red Flags and Trigger Criteria", level=2)
    doc.add_paragraph(
        "The internal finance verification team must audit claims against specific automated red-flag criteria:")
    red_flags = [
        "Duplicate Invoice Numbers: Automated hash matching detects duplicate submissions across multiple employee expense claims.",
        "Weekend & Non-Working Day Filings: Meal or transport claims filed on weekends without logged project work or manager pre-authorization.",
        "Rounded Amounts: Repeated claims submitted at exactly ₹500, ₹1,500, or just under the ₹250 receipt-free threshold.",
        "Vendor Mismatch: Commercial bills from out-of-town vendors that conflict with logged office attendance records.",
    ]
    for rf in red_flags:
        doc.add_paragraph(rf, style="List Bullet")

    doc.add_heading("5.2 Random Audit Sampling & Investigation", level=2)
    doc.add_paragraph(
        "The Finance team enforces mandatory compliance sampling:")
    audit_rules = [
        "15% Random Sampling: An automated algorithm randomly selects 15% of all claims below ₹20,000 for full manual receipt validation.",
        "100% Comprehensive Audit: 100% of all expense claims exceeding ₹20,000 are subject to forensic invoice verification.",
        "Escalation of Suspected Fraud: Confirmed fraudulent claims trigger immediate denial, payroll deduction of any pre-disbursed funds, and referral to Head of HR Ishita Rao and CEO Aarav Mehta for disciplinary action under NST-HR-POL-001.",
    ]
    for ar in audit_rules:
        doc.add_paragraph(ar, style="List Bullet")

    doc.add_heading("6. Related Documents", level=1)
    for ref in ["NST-FIN-POL-002 — Business Travel & Travel Expense Policy",
                "NST-HR-POL-001 — Employee Handbook",
                "NST-HR-POL-003 — Code of Conduct & Workplace Ethics"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("7. Frequently Asked Questions", level=1)
    faqs = [
        ("What is the maximum time to submit an expense claim?", "Claims must be submitted within 30 calendar days from the date of expenditure on the Expense Portal."),
        ("Do I need receipts for expenses under ₹250?", "Receipts are not mandatory for minor incidental expenses of ₹250 or less, but business justification must be stated."),
        ("Who approves an expense claim of ₹12,000?", "Claims between ₹5,001 and ₹25,000 require approval from your Department Head and Finance Manager Arjun Bhat."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-FIN-POL-001")
    add_demo_footer(doc)
    return save_doc(doc, "NST-FIN-POL-001_Expense_Reimbursement_v1.0.docx")

print("Starting Batch 3 document generation...")
files = []
files.append(build_laptop_software_guide())
files.append(build_engineering_guide())
files.append(build_data_analytics_guide())
files.append(build_expense_policy())
print(f"\nBatch 3 complete: {len(files)} documents generated.")

