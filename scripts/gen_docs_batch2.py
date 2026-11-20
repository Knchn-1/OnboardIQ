"""
Phase 5: Generate Batch 2 Northstar Technologies policy DOCX documents.
Documents 5 to 8:
  - NST-HR-POL-005: Recruitment & Employee Referral Policy
  - NST-HR-POL-006: Onboarding & Employee Development Policy
  - NST-HR-POL-007: Performance Review & Promotion Policy (MANAGERS_AND_HR)
  - NST-IT-POL-001: Information Security & Acceptable Use Policy (with RU-002 IT_ONLY section)
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
# DOCUMENT 5: Recruitment & Employee Referral Policy (NST-HR-POL-005)
# ============================================================================
def build_recruitment_referral():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-HR-POL-005", "Recruitment & Employee Referral Policy",
                    "Ishita Rao, Head of Human Resources (EMP-002)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This policy defines the principles, approval workflows and operational procedures for hiring talent "
        "at Northstar Technologies, as well as the rules governing the Employee Referral Scheme. It applies "
        "to all vacancies across Nagpur, Pune, and Bengaluru offices and covers both internal employees and "
        "prospective candidates.")

    doc.add_heading("2. Recruitment Principles and Hiring Authorization", level=1)
    doc.add_paragraph(
        "Northstar Technologies is committed to merit-based, non-discriminatory hiring. Every vacancy must be "
        "approved through the formal requisition process prior to public posting or candidate outreach.")
    
    table = doc.add_table(rows=4, cols=3)
    table.style = "Table Grid"
    steps = [
        ("Step", "Action", "Authorized Role"),
        ("1. Requisition", "Identify vacancy, draft Job Description, define budget", "Department Head / Hiring Manager"),
        ("2. Approval", "Budgetary review, headcount sign-off", "Department Head + HR (Ishita Rao) + CEO (Aarav Mehta)"),
        ("3. Sourcing & Screening", "Job portal posting, referral processing, initial HR interview", "HR Business Partner (Rohan Deshpande)"),
    ]
    for i, row in enumerate(steps):
        for j, val in enumerate(row):
            table.rows[i].cells[j].text = val
    doc.add_paragraph()
    doc.add_paragraph(
        "Technical assessments and departmental interviews are conducted by the respective engineering, data, "
        "or functional team leads before final candidate selection.")

    doc.add_heading("3. Employee Referral Program", level=1)
    doc.add_heading("3.1 Referral Bonus Amount and Payout", level=2)
    doc.add_paragraph(
        "To encourage employees to recommend high-calibre professionals, Northstar Technologies offers an Employee "
        "Referral Bonus of ₹15,000 for each successfully hired candidate. The bonus is subject to the following terms:")
    bonus_rules = [
        "The referral bonus of ₹15,000 is credited in the monthly payroll cycle following the referred employee's completion of 6 months (successful completion of probation).",
        "Both the referring employee and the referred candidate must be active employees of Northstar Technologies on the date of payout.",
        "Applicable tax deductions (TDS) apply to all referral bonus disbursements.",
    ]
    for r in bonus_rules:
        doc.add_paragraph(r, style="List Bullet")

    doc.add_heading("3.2 Eligibility and Limits", level=2)
    table_elig = doc.add_table(rows=5, cols=2)
    table_elig.style = "Table Grid"
    elig_data = [
        ("Parameter", "Policy Rule"),
        ("Eligible Employees", "All confirmed employees in good standing"),
        ("Ineligible Roles", "HR recruitment team members; Hiring Managers for the specific open vacancy; Executive Leadership (CEO)"),
        ("Quarterly Limit", "Maximum of 5 eligible referrals per employee per calendar quarter"),
        ("Self-Referral", "Strictly prohibited; employees cannot refer themselves for other roles"),
    ]
    for i, row in enumerate(elig_data):
        for j, val in enumerate(row):
            table_elig.rows[i].cells[j].text = val

    doc.add_heading("3.3 Referral Submission Workflow", level=2)
    doc.add_paragraph(
        "To submit a referral, the employee must email the candidate's resume, contact details, and current LinkedIn profile "
        "to careers@northstar.example with the subject line 'Referral: [Candidate Name] - [Requisition ID]'. Submissions "
        "must occur prior to the candidate applying directly or through a third-party agency. Referral claims are valid for "
        "6 months from the date of submission.")

    doc.add_heading("4. Background Verification", level=1)
    doc.add_paragraph(
        "All prospective hires undergo comprehensive pre-employment background verification, including academic credentials, "
        "previous employment history, identity verification, and criminal record screening. Discrepancies or false representations "
        "lead to immediate withdrawal of offer or termination of employment.")
    add_statutory_note(doc)

    doc.add_heading("5. Related Documents", level=1)
    for ref in ["NST-HR-POL-001 — Employee Handbook",
                "NST-HR-POL-006 — Onboarding & Employee Development Policy",
                "NST-HR-POL-003 — Code of Conduct & Workplace Ethics"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("6. Frequently Asked Questions", level=1)
    faqs = [
        ("When is the referral bonus paid?", "The ₹15,000 referral bonus is paid in the payroll run after the referred employee completes their 6-month probation period."),
        ("Can an engineering manager refer candidates for their own team?", "No. Hiring managers cannot claim referral bonuses for vacancies within their direct reporting hierarchy."),
        ("Is there a limit on how many candidates I can refer?", "Yes, you may submit up to 5 referrals per calendar quarter."),
        ("Can probationary employees submit referrals?", "Probationary employees may submit resumes, but the referral bonus eligibility is confirmed only after the referring employee is confirmed."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-HR-POL-005")
    add_demo_footer(doc)
    return save_doc(doc, "NST-HR-POL-005_Recruitment_Referral_v1.0.docx")

# ============================================================================
# DOCUMENT 6: Onboarding & Employee Development Policy (NST-HR-POL-006)
# ============================================================================
def build_onboarding_development():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-HR-POL-006", "Onboarding & Employee Development Policy",
                    "Ishita Rao, Head of Human Resources (EMP-002)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This policy establishes the structured onboarding framework, induction schedule, buddy program, and continuous "
        "learning and professional development opportunities provided to employees at Northstar Technologies. It covers "
        "all newly hired employees across Nagpur, Pune, and Bengaluru.")

    doc.add_heading("2. New Hire Onboarding Framework", level=1)
    doc.add_heading("2.1 Day One Induction Agenda", level=2)
    doc.add_paragraph(
        "Day One focuses on formal joining formalities, orientation, and device configuration:")
    table_d1 = doc.add_table(rows=5, cols=3)
    table_d1.style = "Table Grid"
    d1_items = [
        ("Time Window", "Activity", "Responsible Owner"),
        ("10:00 AM – 11:30 AM", "HR Welcome, document verification, HRMS portal access setup", "HR Team (Rohan Deshpande)"),
        ("11:30 AM – 01:00 PM", "Company Overview, mission, cultural values, policy briefing", "Head of HR (Ishita Rao)"),
        ("01:00 PM – 02:00 PM", "Team Welcome Lunch & introductions", "Department Buddy & Manager"),
        ("02:00 PM – 04:30 PM", "IT device handover, email/Slack provisioning, VPN/MFA setup", "IT Support (Kabir Shah)"),
    ]
    for i, row in enumerate(d1_items):
        for j, val in enumerate(row):
            table_d1.rows[i].cells[j].text = val

    doc.add_heading("2.2 The 30-60-90 Day Milestone Roadmap", level=2)
    milestones = [
        ("First 30 Days (Assimilation):", "Complete mandatory compliance training (Information Security, POSH, Code of Conduct). Set up local development/analytical environment. Complete first starter ticket with assigned Buddy."),
        ("60 Days (Contribution):", "Deliver independent project tasks. First formal progress check-in with Reporting Manager. Mid-probation feedback review."),
        ("90 Days (Autonomy):", "Full operational autonomy. Participation in cross-team code reviews or client discussions. Objective alignment for remaining probation period."),
    ]
    for title, desc in milestones:
        p = doc.add_paragraph()
        run = p.add_run(title + " ")
        run.bold = True
        p.add_run(desc)

    doc.add_heading("3. The OnboardIQ Buddy Program", level=1)
    doc.add_paragraph(
        "Every new hire is assigned an experienced peer 'Buddy' from their respective department for their first 90 days. "
        "The Buddy provides informal guidance, clarifies internal workflows, explains acronyms, and facilitates cross-team "
        "introductions. Buddies are designated by the Department Manager during the pre-joining phase.")

    doc.add_heading("4. Probation Review and Confirmation", level=1)
    doc.add_paragraph(
        "All permanent employees undergo a standard 6-month probation period. Formal reviews take place at:")
    p_reviews = [
        "Month 3: Formal mid-probation checkpoint to assess role alignment and identify skill gaps.",
        "Month 5: Comprehensive confirmation review conducted by Reporting Manager and HR.",
        "Month 6: Issuance of written confirmation letter or, in rare instances, extension of probation (maximum 3 additional months with specific improvement milestones).",
    ]
    for pr in p_reviews:
        doc.add_paragraph(pr, style="List Bullet")
    add_statutory_note(doc)

    doc.add_heading("5. Learning and Professional Development", level=1)
    doc.add_paragraph(
        "Northstar Technologies actively invests in employee skill enhancement. Confirmed employees are entitled to:")
    learn_items = [
        "Access to enterprise online learning platforms (e.g., technical certifications, cloud architecture, AI courses).",
        "Up to 40 hours of dedicated professional learning time per calendar year, scheduled with manager approval.",
        "Certification reimbursement for approved professional credentials (AWS, Azure, GCP, PMP, Scrum) subject to departmental pre-approval and a 12-month service commitment.",
    ]
    for li in learn_items:
        doc.add_paragraph(li, style="List Bullet")

    doc.add_heading("6. Related Documents", level=1)
    for ref in ["NST-HR-POL-001 — Employee Handbook",
                "NST-HR-POL-005 — Recruitment & Employee Referral Policy",
                "NST-IT-GDE-001 — Laptop, Software & Account Setup Guide"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("7. Frequently Asked Questions", level=1)
    faqs = [
        ("Who will be my Buddy when I join?", "Your reporting manager will assign an experienced team colleague as your Buddy before your first day."),
        ("When do I get my laptop and email credentials?", "Your laptop and credentials are provided on Day One during the afternoon IT session with Kabir Shah."),
        ("What happens if my probation is extended?", "In cases where additional time is needed to demonstrate competency, probation may be extended for up to 3 months with a clearly defined action plan."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-HR-POL-006")
    add_demo_footer(doc)
    return save_doc(doc, "NST-HR-POL-006_Onboarding_Development_v1.0.docx")

# ============================================================================
# DOCUMENT 7: Performance Review & Promotion Policy (NST-HR-POL-007)
# ============================================================================
def build_performance_promotion():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-HR-POL-007", "Performance Review & Promotion Policy",
                    "Ishita Rao, Head of Human Resources (EMP-002)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "MANAGERS_AND_HR (Document level audience restricted to Managers and HR)")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This policy governs the performance appraisal cycle, objective setting, competency evaluations, and promotion "
        "processes at Northstar Technologies. It provides guidance to people managers and HR leadership to ensure fair, "
        "transparent, and merit-based talent progression across all departments.")

    doc.add_heading("2. Performance Appraisal Cycle", level=1)
    doc.add_paragraph(
        "Northstar Technologies conducts formal performance reviews on a bi-annual cycle:")
    table_cycle = doc.add_table(rows=3, cols=3)
    table_cycle.style = "Table Grid"
    cycle_data = [
        ("Review Period", "Review Window", "Focus Areas"),
        ("H1 (April – September)", "October 1 – October 31", "Mid-year milestone tracking, feedback, development adjustments"),
        ("H2 (October – March)", "April 1 – April 30", "Annual objective evaluation, rating finalization, increment & promotion awards"),
    ]
    for i, row in enumerate(cycle_data):
        for j, val in enumerate(row):
            table_cycle.rows[i].cells[j].text = val

    doc.add_heading("3. Performance Rating Scale", level=1)
    doc.add_paragraph("Performance is calibrated using a 5-point rating scale:")
    ratings = [
        ("Rating 5 (Exceptional Performance):", "Consistently exceeds all goals; demonstrates outstanding leadership, innovation, and company-wide impact."),
        ("Rating 4 (Exceeds Expectations):", "Regularly surpasses performance expectations; delivers superior technical quality and proactive collaboration."),
        ("Rating 3 (Meets Expectations):", "Consistently achieves defined objectives and core job responsibilities; solid, dependable contributor."),
        ("Rating 2 (Needs Improvement):", "Inconsistently meets standards; developmental gaps identified requiring a structured support plan."),
        ("Rating 1 (Unsatisfactory):", "Consistently fails to achieve key requirements; triggers a mandatory Performance Improvement Plan (PIP)."),
    ]
    for r_title, r_desc in ratings:
        p = doc.add_paragraph()
        run = p.add_run(r_title + " ")
        run.bold = True
        p.add_run(r_desc)

    doc.add_heading("4. Promotion Criteria and Governance", level=1)
    doc.add_heading("4.1 Eligibility Prerequisites", level=2)
    doc.add_paragraph("Employees considered for promotion must satisfy all of the following prerequisites:")
    prereqs = [
        "Tenure: Minimum of 12 continuous months in their current designation at Northstar Technologies.",
        "Performance Track Record: Rating of 4 or 5 in the most recent annual review cycle, with no disciplinary warnings.",
        "Demonstrated Competency: Consistently executing responsibilities characteristic of the next band for at least 3 months.",
        "Organizational Need: Documented business requirement and budget allocation within the department.",
    ]
    for pr in prereqs:
        doc.add_paragraph(pr, style="List Bullet")

    doc.add_heading("4.2 Promotion Approval Matrix", level=2)
    doc.add_paragraph("Promotions require multi-tier authorization as specified in the Approval Authority Matrix:")
    table_prom = doc.add_table(rows=2, cols=2)
    table_prom.style = "Table Grid"
    table_prom.rows[0].cells[0].text = "Action"
    table_prom.rows[0].cells[1].text = "Authorized Approval Chain"
    table_prom.rows[1].cells[0].text = "Employee Promotion & Title Reclassification"
    table_prom.rows[1].cells[1].text = "Reporting Manager → Department Head → Head of HR (Ishita Rao) → CEO (Aarav Mehta)"

    doc.add_heading("5. Performance Improvement Plan (PIP) Framework", level=1)
    doc.add_paragraph(
        "Employees receiving a Rating 1 or exhibiting persistent underperformance are placed on a structured PIP:")
    pip_steps = [
        "Duration: 30 to 60 calendar days, agreed between Reporting Manager and HR.",
        "Documentation: Clear, measurable deliverables, weekly check-in dates, and specific success metrics recorded in HRMS.",
        "Outcome: Successful completion returns employee to good standing; failure to meet agreed targets leads to separation under the Employee Handbook (NST-HR-POL-001 Section 13).",
    ]
    for ps in pip_steps:
        doc.add_paragraph(ps, style="List Bullet")

    doc.add_heading("6. Related Documents", level=1)
    for ref in ["NST-HR-POL-001 — Employee Handbook",
                "NST-HR-POL-002 — Leave, Attendance & Working Hours Policy",
                "NST-HR-POL-006 — Onboarding & Employee Development Policy"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("7. Frequently Asked Questions (Managers)", level=1)
    faqs = [
        ("Can an employee be promoted before completing 12 months in their role?", "No. The 12-month tenure prerequisite in the current role is mandatory across all departments."),
        ("Who makes the final decision on promotions?", "Final promotion authorization requires sign-off from the Department Head, Head of HR (Ishita Rao), and CEO (Aarav Mehta)."),
        ("What is the duration of a Performance Improvement Plan?", "A PIP typically lasts between 30 and 60 calendar days depending on role complexity."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-HR-POL-007")
    add_demo_footer(doc)
    return save_doc(doc, "NST-HR-POL-007_Performance_Promotion_v1.0.docx")

# ============================================================================
# DOCUMENT 8: Information Security & Acceptable Use Policy (NST-IT-POL-001)
# ============================================================================
def build_infosec_acceptable_use():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-IT-POL-001", "Information Security & Acceptable Use Policy",
                    "Neha Kulkarni, IT Manager (EMP-004)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES (Sections marked IT_ONLY are restricted)")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This policy defines mandatory requirements for protecting Northstar Technologies' digital assets, customer data, "
        "and IT infrastructure. It outlines acceptable computer and network usage, password standards, data handling "
        "classifications, and incident response requirements. It applies to all employees, contractors, and third parties "
        "accessing Northstar systems across Nagpur, Pune, and Bengaluru.")

    doc.add_heading("2. Access Control and Authentication Standards", level=1)
    doc.add_paragraph(
        "Access to company resources follows the principle of least privilege. Authentication rules are strictly enforced:")
    table_auth = doc.add_table(rows=6, cols=2)
    table_auth.style = "Table Grid"
    auth_data = [
        ("Parameter", "Requirement"),
        ("Minimum Password Length", "12 characters"),
        ("Complexity", "At least one uppercase letter, one lowercase letter, one number, and one special character"),
        ("Password Expiry", "90 calendar days; cannot reuse last 5 passwords"),
        ("Multi-Factor Authentication (MFA)", "Mandatory on Google Workspace, GitLab, Jira, Confluence, Slack, and VPN"),
        ("Screen Lock Inactivity Timeout", "5 minutes of inactivity triggers automatic screen lock"),
    ]
    for i, row in enumerate(auth_data):
        for j, val in enumerate(row):
            table_auth.rows[i].cells[j].text = val

    doc.add_heading("3. Device and Endpoint Security", level=1)
    doc.add_heading("3.1 Company Hardware", level=2)
    doc.add_paragraph(
        "All work must be conducted on company-provisioned laptops managed by IT. Employees must not disable endpoint "
        "antivirus, firewall, or MDM profiles.")
    
    doc.add_heading("3.2 Removable Media and USB Policy", level=2)
    doc.add_paragraph(
        "Mass storage via USB drives, external hard disks, and memory cards is disabled by default across all company laptops. "
        "In exceptional operational scenarios, temporary USB access requires formal approval from IT Manager Neha Kulkarni "
        "with an active business justification.")

    doc.add_heading("3.3 Bring Your Own Device (BYOD)", level=2)
    doc.add_paragraph(
        "Personal computers, tablets, or unmanaged devices are strictly prohibited from accessing internal code repositories "
        "or customer databases. Mobile device access (email/Slack) is permitted only upon enrollment in the company MDM.")

    doc.add_heading("4. Remote Access and Network Usage", level=1)
    doc.add_paragraph(
        "When working remotely or from public locations, connection through the company WireGuard VPN (vpn.northstar.example) "
        "is mandatory before accessing any internal corporate system. Connecting to open, unencrypted public Wi-Fi networks "
        "without active VPN encapsulation is an explicit policy violation.")

    doc.add_heading("5. Data Classification Framework", level=1)
    doc.add_paragraph("All company and customer data must be classified into one of four tiers:")
    tiers = [
        ("Tier 1: Public", "Marketing materials, publicly released software documentation, website content. No special safeguards."),
        ("Tier 2: Internal", "Internal policies, employee handbook, general company announcements, directory. Standard employee access."),
        ("Tier 3: Confidential", "Source code, customer project deliverables, contracts, financial reports, operational architecture. Role-based access."),
        ("Tier 4: Restricted", "Customer PII, production credentials, private cryptographic keys, HR disciplinary files, fraud investigation records. Strictly segregated access with audit logging."),
    ]
    for t_name, t_desc in tiers:
        p = doc.add_paragraph()
        run = p.add_run(t_name + ": ")
        run.bold = True
        p.add_run(t_desc)
    add_statutory_note(doc)

    doc.add_heading("6. Incident Reporting and Escalation", level=1)
    doc.add_paragraph(
        "Any suspected security incident, malware detection, phishing attempt, lost laptop, or inadvertent data disclosure "
        "must be immediately reported to security@northstar.example. The primary operational escalation path is:")
    doc.add_paragraph(
        "IT Support Specialist (Kabir Shah) → IT Manager (Neha Kulkarni) → CEO (Aarav Mehta).",
        style="List Bullet")

    # RESTRICTED UNIT 2: RU-002
    doc.add_heading("7. Security Incident Response Procedures — Internal Playbook", level=1)
    p_rest = doc.add_paragraph()
    run_rest = p_rest.add_run("ACCESS RESTRICTION: This section is classified IT_ONLY. "
                              "Only members of the Information Technology department (GRP_DEPT_IT) may access this content.")
    run_rest.bold = True
    run_rest.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

    doc.add_heading("7.1 Incident Containment and Network Isolation", level=2)
    doc.add_paragraph(
        "Upon confirmation of a Severity P1 or P2 incident, IT engineers must execute containment within 30 minutes:")
    containment_steps = [
        "Network Isolation: Remotely disconnect the infected endpoint from corporate Wi-Fi/VPN via MDM console without powering off.",
        "Session Revocation: Invalidate active OAuth tokens and terminate Google Workspace, GitLab, and VPN sessions for compromised accounts.",
        "Firewall Rule Enforcement: Block identified malicious external IP addresses and domains at the perimeter gateway.",
    ]
    for cs in containment_steps:
        doc.add_paragraph(cs, style="List Bullet")

    doc.add_heading("7.2 Forensic Evidence Preservation", level=2)
    doc.add_paragraph(
        "Volatile memory (RAM) must be imaged prior to system reboot using approved forensic tooling. Disk drive BitLocker "
        "recovery keys must be secured, and chain-of-custody documentation logged in Jira Service Desk under the CONFIDENTIAL-SEC project.")

    doc.add_heading("7.3 Breach Notification Decision Criteria", level=2)
    doc.add_paragraph(
        "Statutory and customer breach notification triggers are evaluated exclusively by the IT Manager (Neha Kulkarni) and "
        "CEO (Aarav Mehta). Under applicable Indian data protection frameworks, notification protocols must initiate within "
        "prescribed statutory windows following incident confirmation.")
    add_statutory_note(doc)

    doc.add_heading("8. Related Documents", level=1)
    for ref in ["NST-IT-GDE-001 — Laptop, Software & Account Setup Guide",
                "NST-IT-GDE-003 — IT Incident Management & Emergency Procedures",
                "NST-HR-POL-003 — Code of Conduct & Workplace Ethics",
                "NST-DA-GDE-001 — Data Handling, Access & Analytics Delivery Guide"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("9. Frequently Asked Questions", level=1)
    faqs = [
        ("What should I do if I receive a suspicious email?", "Do not click any links or attachments. Forward the email as an attachment to security@northstar.example and notify Kabir Shah on Slack."),
        ("How often must I change my password?", "Passwords expire every 90 days. You will receive an automated prompt 7 days prior to expiry."),
        ("Can I plug in a personal USB drive to copy files?", "No. USB storage devices are blocked by default. Request an IT exception if business-essential."),
        ("What is the screen lock timeout?", "Screens lock automatically after 5 minutes of inactivity."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-IT-POL-001")
    add_demo_footer(doc)
    return save_doc(doc, "NST-IT-POL-001_InfoSec_Acceptable_Use_v1.0.docx")

print("Starting Batch 2 document generation...")
files = []
files.append(build_recruitment_referral())
files.append(build_onboarding_development())
files.append(build_performance_promotion())
files.append(build_infosec_acceptable_use())
print(f"\nBatch 2 complete: {len(files)} documents generated.")

