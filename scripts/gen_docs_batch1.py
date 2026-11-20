"""
Phase 5: Generate all Northstar Technologies policy DOCX documents.
Reads from Master Data JSON. Writes to output/02_documents_docx/.
"""
import json
import os
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

OUTPUT_DIR = "output/02_documents_docx"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open("output/01_master_data/northstar_master_data.json", "r", encoding="utf-8") as f:
    MD = json.load(f)

DEMO_LABEL = MD["_metadata"]["demonstration_label"]
STAT_NOTE = MD["_metadata"]["statutory_note"]
VERSION = "1.0"
EFF_DATE = "01 November 2026"
REVIEW_DATE = "01 May 2027"

# Helper functions
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
# DOCUMENT 1: Employee Handbook (NST-HR-POL-001)
# ============================================================================
def build_employee_handbook():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-HR-POL-001", "Employee Handbook",
                    "Ishita Rao, Head of Human Resources (EMP-002)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES (Sections marked HR_ONLY are restricted)")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This Employee Handbook provides a comprehensive overview of the employment policies, workplace expectations, "
        "and employee benefits at Northstar Technologies. It applies to all employees across all office locations — "
        "Nagpur, Pune and Bengaluru — unless a specific policy states otherwise. This handbook is a reference guide "
        "and does not constitute an employment contract.")

    doc.add_heading("2. About Northstar Technologies", level=1)
    doc.add_paragraph(
        "Northstar Technologies is an India-based technology services company specialising in custom software development, "
        "web and API engineering, data analytics, cloud solutions and AI-enabled applications. The company operates from "
        "its head office in Nagpur, Maharashtra, with branch offices in Pune, Maharashtra, and Bengaluru, Karnataka.")
    doc.add_paragraph(
        "The company follows an office-first working model with approved hybrid and remote arrangements under the "
        "applicable Remote Work & Work From Home Policy (NST-HR-POL-004).")

    doc.add_heading("3. Employment Classifications", level=1)
    doc.add_paragraph("Northstar Technologies classifies employees as follows:")
    items = [
        ("Probationary Employee", "A new employee serving the initial 6-month probation period. During probation, either party may terminate the employment relationship with 30 calendar days' written notice."),
        ("Confirmed Employee", "An employee who has successfully completed the probation period and received written confirmation. Confirmed employees must provide 60 calendar days' written notice for resignation."),
        ("Intern/Trainee", "A temporary position for learning and development purposes, governed by a separate internship agreement."),
    ]
    for title, desc in items:
        p = doc.add_paragraph()
        run = p.add_run(title + ": ")
        run.bold = True
        p.add_run(desc)
    add_statutory_note(doc)

    doc.add_heading("4. Compensation and Benefits", level=1)
    doc.add_heading("4.1 Pay Cycle", level=2)
    doc.add_paragraph(
        "Salaries are credited on the last working day of each calendar month to the employee's registered bank account. "
        "Payslips are available on the HRMS Portal (https://hrms.northstar.example).")
    doc.add_heading("4.2 Provident Fund and Statutory Deductions", level=2)
    doc.add_paragraph(
        "Statutory deductions including Provident Fund (PF), Professional Tax and income tax (TDS) are applied "
        "as per applicable laws. Employees may view deduction details on the HRMS Portal.")
    add_statutory_note(doc)

    doc.add_heading("5. Working Hours and Attendance", level=1)
    doc.add_paragraph(
        "Standard working hours are 9 hours per day (including a 1-hour lunch break), totalling 45 hours per week, "
        "Monday through Friday. Core office hours are 10:00 AM to 7:00 PM with a flexible start window of 9:00 AM "
        "to 10:30 AM subject to manager approval. Employees must mark attendance daily through the HRMS Portal by "
        "10:30 AM. A grace period of 15 minutes is allowed for late arrivals.")
    doc.add_paragraph(
        "Detailed rules are in the Leave, Attendance & Working Hours Policy (NST-HR-POL-002).")

    doc.add_heading("6. Leave Entitlements — Summary", level=1)
    table = doc.add_table(rows=7, cols=3)
    table.style = "Table Grid"
    leave_data = [
        ("Leave Type", "Days per Year", "Notes"),
        ("Casual Leave", "12", "Cannot be carried forward"),
        ("Sick Leave", "12", "Medical certificate required for > 2 consecutive days"),
        ("Earned Leave", "15", "Up to 5 days may be carried forward; encashable"),
        ("Maternity Leave", "26 weeks", "As per the Maternity Benefit Act, 1961"),
        ("Paternity Leave", "5 days", "Company benefit; within 30 days of childbirth"),
        ("Bereavement Leave", "5 days", "Immediate family members"),
    ]
    for i, row_data in enumerate(leave_data):
        for j, cell_val in enumerate(row_data):
            table.rows[i].cells[j].text = cell_val
    doc.add_paragraph("Full leave rules are in NST-HR-POL-002.")
    add_statutory_note(doc)

    doc.add_heading("7. Code of Conduct — Summary", level=1)
    doc.add_paragraph(
        "All employees are expected to uphold the company's core values of integrity, respect, customer focus, "
        "ownership, learning, and security and privacy. Detailed expectations, anti-harassment commitments, "
        "conflict-of-interest guidelines and the Prevention of Sexual Harassment (POSH) framework are covered "
        "in the Code of Conduct & Workplace Ethics (NST-HR-POL-003).")

    doc.add_heading("8. Information Security — Summary", level=1)
    doc.add_paragraph(
        "All employees must comply with the Information Security & Acceptable Use Policy (NST-IT-POL-001). "
        "Key requirements include: passwords of at least 12 characters changed every 90 days, multi-factor "
        "authentication on all company systems, mandatory VPN for remote access, and immediate reporting of "
        "suspected security incidents to security@northstar.example.")

    doc.add_heading("9. Performance and Development", level=1)
    doc.add_paragraph(
        "Northstar Technologies conducts formal performance reviews bi-annually. Employees set objectives in "
        "discussion with their reporting manager at the start of each review cycle. The performance framework, "
        "promotion eligibility criteria and the review process are detailed in the Performance Review & Promotion "
        "Policy (NST-HR-POL-007).")

    doc.add_heading("10. Dress Code", level=1)
    doc.add_paragraph(
        "The standard dress code is business casual on regular working days. Formal attire is expected during "
        "client-facing meetings, presentations and official company events. Employees should use good judgement "
        "and dress appropriately for their scheduled activities.")

    doc.add_heading("11. Grievance and Complaint Procedures", level=1)
    doc.add_paragraph(
        "Employees who have workplace concerns may raise them with their reporting manager or directly with the "
        "HR team. For sensitive matters including harassment complaints, employees should use the confidential "
        "reporting channel at hr.grievance@northstar.example. Complaints are acknowledged within 2 working days "
        "and investigated in line with the company's internal procedures.")
    doc.add_paragraph(
        "For matters related to sexual harassment, the company follows the framework under the Sexual Harassment "
        "of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013. The Internal Committee can be "
        "reached at posh.committee@northstar.example.")
    add_statutory_note(doc)

    doc.add_heading("12. Separation and Exit", level=1)
    doc.add_paragraph(
        "Employees wishing to resign must submit a written resignation to their reporting manager and HR. "
        "The applicable notice period is 30 calendar days during probation and 60 calendar days after confirmation. "
        "The company may waive or buy out part of the notice period at its discretion. An exit interview will be "
        "conducted by HR. All company assets including laptop, ID card, and access credentials must be returned "
        "on or before the last working day.")

    doc.add_heading("13. Disciplinary Action and Termination Procedures", level=1)
    p = doc.add_paragraph()
    run = p.add_run("ACCESS RESTRICTION: This section is classified HR_ONLY. "
                     "Only members of the Human Resources department may access this content.")
    run.bold = True
    run.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

    doc.add_heading("13.1 Disciplinary Escalation Framework", level=2)
    doc.add_paragraph(
        "Northstar Technologies follows a progressive disciplinary approach. The escalation steps are:")
    table2 = doc.add_table(rows=5, cols=3)
    table2.style = "Table Grid"
    disc_data = [
        ("Step", "Action", "Authority"),
        ("Step 1", "Verbal counselling with documented record", "Reporting Manager + HR"),
        ("Step 2", "Written warning with improvement plan (30-day timeline)", "HR Business Partner"),
        ("Step 3", "Final written warning and performance improvement plan (60 days)", "Head of HR"),
        ("Step 4", "Termination of employment with documented rationale", "Head of HR + CEO"),
    ]
    for i, row_data in enumerate(disc_data):
        for j, val in enumerate(row_data):
            table2.rows[i].cells[j].text = val

    doc.add_heading("13.2 Suspension Pending Investigation", level=2)
    doc.add_paragraph(
        "In cases of serious misconduct or security concerns, an employee may be placed on administrative "
        "suspension with pay pending investigation. Suspension decisions require approval from the Head of HR "
        "(EMP-002, Ishita Rao). The investigation must be completed within 15 working days. The employee "
        "must be informed in writing of the suspension, its duration, and the investigation process.")

    doc.add_heading("13.3 Termination Checklist", level=2)
    doc.add_paragraph("The following steps must be completed for any termination:")
    checklist = [
        "Document the complete disciplinary history and investigation findings.",
        "Obtain written approval from Head of HR and CEO.",
        "Prepare the termination letter with effective date and final settlement details.",
        "Schedule a termination meeting with the employee, HR representative and reporting manager.",
        "Revoke all system access, email and VPN credentials immediately upon notification.",
        "Collect company assets (laptop, ID card, access cards).",
        "Process full and final settlement within 30 working days.",
        "Conduct an exit interview if the employee consents.",
        "Archive the employee's HR case file with restricted access for 7 years.",
    ]
    for item in checklist:
        doc.add_paragraph(item, style="List Bullet")

    doc.add_heading("14. Related Documents", level=1)
    refs = [
        "NST-HR-POL-002 — Leave, Attendance & Working Hours Policy",
        "NST-HR-POL-003 — Code of Conduct & Workplace Ethics",
        "NST-HR-POL-004 — Remote Work & Work From Home Policy",
        "NST-HR-POL-005 — Recruitment & Employee Referral Policy",
        "NST-HR-POL-006 — Onboarding & Employee Development Policy",
        "NST-HR-POL-007 — Performance Review & Promotion Policy",
        "NST-IT-POL-001 — Information Security & Acceptable Use Policy",
        "NST-IT-GDE-001 — Laptop, Software & Account Setup Guide",
        "NST-FIN-POL-001 — Expense Reimbursement Policy",
    ]
    for r in refs:
        doc.add_paragraph(r, style="List Bullet")

    doc.add_heading("15. Frequently Asked Questions", level=1)
    faqs = [
        ("How long is the probation period?", "The standard probation period is 6 months from your date of joining. You will receive written confirmation upon successful completion."),
        ("What is the notice period if I want to resign?", "During probation, the notice period is 30 calendar days. After confirmation, it is 60 calendar days. Notice periods may be waived or bought out at the company's discretion."),
        ("Where can I view my payslips?", "Payslips are available on the HRMS Portal at https://hrms.northstar.example after each pay cycle."),
        ("What should I do if I have a workplace complaint?", "Raise the matter with your reporting manager or contact HR directly. For confidential concerns, email hr.grievance@northstar.example."),
        ("How many casual leave days do I get per year?", "You are entitled to 12 casual leave days per calendar year. These cannot be carried forward."),
        ("What is the dress code?", "Business casual on regular days. Formal attire for client-facing meetings."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-HR-POL-001")
    add_demo_footer(doc)
    return save_doc(doc, "NST-HR-POL-001_Employee_Handbook_v1.0.docx")

# ============================================================================
# DOCUMENT 2: Leave, Attendance & Working Hours Policy (NST-HR-POL-002)
# ============================================================================
def build_leave_policy():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-HR-POL-002", "Leave, Attendance & Working Hours Policy",
                    "Ishita Rao, Head of Human Resources (EMP-002)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This policy establishes the rules governing leave entitlements, attendance recording and working hours "
        "for all employees of Northstar Technologies across Nagpur, Pune and Bengaluru offices. It ensures "
        "consistent application of time-off benefits while maintaining operational continuity.")

    doc.add_heading("2. Definitions", level=1)
    defs = [
        ("Leave Year", "1 January to 31 December of each calendar year."),
        ("Casual Leave (CL)", "Short-duration leave for personal needs that cannot be planned in advance."),
        ("Sick Leave (SL)", "Leave taken on account of illness or medical treatment."),
        ("Earned Leave (EL)", "Leave accrued based on service, intended for planned rest and recuperation."),
        ("Compensatory Off (Comp-Off)", "Time off granted in lieu of work performed on a non-working day or beyond standard hours with prior manager approval."),
        ("Loss of Pay (LOP)", "Absence without available leave balance, resulting in proportionate salary deduction."),
        ("HRMS Portal", "The company's Human Resource Management System at https://hrms.northstar.example."),
    ]
    for term, defn in defs:
        p = doc.add_paragraph()
        run = p.add_run(term + ": ")
        run.bold = True
        p.add_run(defn)

    doc.add_heading("3. Leave Entitlements", level=1)
    doc.add_heading("3.1 Annual Leave Allocation", level=2)
    table = doc.add_table(rows=8, cols=4)
    table.style = "Table Grid"
    leave_rows = [
        ("Leave Type", "Days per Year", "Carry Forward", "Encashment"),
        ("Casual Leave", "12", "Not permitted", "Not permitted"),
        ("Sick Leave", "12", "Not permitted", "Not permitted"),
        ("Earned Leave", "15", "Up to 5 days to next year", "Up to 5 days at basic pay (year-end, manager-approved)"),
        ("Maternity Leave", "26 weeks", "N/A", "N/A"),
        ("Paternity Leave", "5 days", "N/A", "N/A"),
        ("Bereavement Leave", "5 days", "N/A", "N/A"),
        ("Comp-Off", "As accrued", "Must be used within 30 days of accrual", "Not permitted"),
    ]
    for i, row_data in enumerate(leave_rows):
        for j, val in enumerate(row_data):
            table.rows[i].cells[j].text = val
    add_statutory_note(doc)

    doc.add_heading("3.2 Leave Rules", level=2)
    rules = [
        "Casual leave may be taken in half-day units. A maximum of 3 consecutive casual leave days is permitted per instance.",
        "Sick leave for more than 2 consecutive working days requires a medical certificate uploaded to the HRMS Portal.",
        "Earned leave must be applied for at least 3 working days in advance and requires reporting manager approval.",
        "Maternity leave of 26 weeks is available to eligible women employees as per the Maternity Benefit Act, 1961. The leave may be taken up to 8 weeks before the expected delivery date.",
        "Paternity leave of 5 working days is a company benefit available within 30 calendar days of the child's birth. This is not a statutory entitlement.",
        "Bereavement leave of 5 working days is available upon the death of an immediate family member (spouse, parent, child, sibling, parent-in-law).",
        "Compensatory off must be pre-approved by the reporting manager before the extra work is performed. Comp-off expires 30 days after accrual.",
    ]
    for r in rules:
        doc.add_paragraph(r, style="List Bullet")

    doc.add_heading("3.3 Leave Approval Workflow", level=2)
    doc.add_paragraph("All leave requests are submitted through the HRMS Portal and follow this approval chain:")
    table2 = doc.add_table(rows=4, cols=3)
    table2.style = "Table Grid"
    approval = [
        ("Scenario", "Approver", "Timeline"),
        ("Leave of 1–3 days", "Reporting Manager", "Within 1 working day"),
        ("Leave exceeding 3 consecutive days", "Reporting Manager + HR", "Within 2 working days"),
        ("Leave during critical project deadlines", "Reporting Manager + Department Head", "Case-by-case"),
    ]
    for i, row_data in enumerate(approval):
        for j, val in enumerate(row_data):
            table2.rows[i].cells[j].text = val

    doc.add_heading("4. Attendance Policy", level=1)
    doc.add_heading("4.1 Attendance Recording", level=2)
    doc.add_paragraph(
        "Employees must mark their attendance daily through the HRMS Portal by 10:30 AM. Attendance regularisation "
        "requests for missed entries must be submitted within 3 working days with manager approval.")

    doc.add_heading("4.2 Late Arrival", level=2)
    doc.add_paragraph(
        "A grace period of 15 minutes beyond the scheduled start time is permitted. Repeated late arrivals "
        "(more than 3 instances in a calendar month) will be flagged to the reporting manager and HR for counselling.")

    doc.add_heading("4.3 Unauthorised Absence", level=2)
    doc.add_paragraph(
        "Absence without approved leave or notification for 3 or more consecutive working days is treated as "
        "unauthorised absence. This triggers a written notice from HR and may result in disciplinary action under "
        "the Employee Handbook (NST-HR-POL-001). Days of unauthorised absence are marked as Loss of Pay.")

    doc.add_heading("5. Working Hours", level=1)
    table3 = doc.add_table(rows=6, cols=2)
    table3.style = "Table Grid"
    wh = [
        ("Parameter", "Value"),
        ("Standard work day", "9 hours (including 1-hour lunch break)"),
        ("Standard work week", "45 hours, Monday to Friday"),
        ("Core office hours", "10:00 AM to 7:00 PM"),
        ("Flexible start window", "9:00 AM to 10:30 AM (with manager approval)"),
        ("Lunch break", "1 hour, typically 1:00 PM to 2:00 PM"),
    ]
    for i, row_data in enumerate(wh):
        for j, val in enumerate(row_data):
            table3.rows[i].cells[j].text = val
    add_statutory_note(doc)

    doc.add_heading("5.1 Overtime", level=2)
    doc.add_paragraph(
        "Work beyond standard hours must be pre-approved by the reporting manager. Overtime is compensated "
        "through compensatory off (comp-off) to be availed within 30 calendar days. Direct overtime payment is "
        "not provided by default unless specifically agreed for project-specific requirements. Managers must ensure "
        "overtime does not become a regular pattern and must address workload distribution proactively.")
    add_statutory_note(doc)

    doc.add_heading("6. Roles and Responsibilities", level=1)
    roles_table = doc.add_table(rows=4, cols=2)
    roles_table.style = "Table Grid"
    roles_data = [
        ("Role", "Responsibility"),
        ("Employee", "Apply for leave in advance where possible, mark attendance daily, comply with working hour norms."),
        ("Reporting Manager", "Approve or reject leave requests within specified timelines, monitor attendance patterns, approve overtime."),
        ("HR (Ishita Rao / Rohan Deshpande)", "Administer leave balances, investigate attendance issues, maintain records, ensure policy compliance."),
    ]
    for i, row_data in enumerate(roles_data):
        for j, val in enumerate(row_data):
            roles_table.rows[i].cells[j].text = val

    doc.add_heading("7. Exceptions and Escalation", level=1)
    doc.add_paragraph(
        "Exceptions to this policy (for instance, extended leave beyond entitlement or modified working hours) "
        "require written approval from the Department Head and HR. Unresolved disputes may be escalated to the "
        "CEO (EMP-001, Aarav Mehta). All exceptions are recorded in the HRMS Portal.")

    doc.add_heading("8. Related Documents", level=1)
    for ref in ["NST-HR-POL-001 — Employee Handbook",
                "NST-HR-POL-004 — Remote Work & Work From Home Policy",
                "NST-HR-POL-007 — Performance Review & Promotion Policy"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("9. Frequently Asked Questions", level=1)
    faqs = [
        ("Can I carry forward my casual leave?", "No. Casual leave cannot be carried forward to the next year and lapses on 31 December."),
        ("How do I apply for sick leave if I am unable to come to the office?", "Inform your reporting manager by phone, email or Slack as soon as possible. Submit the formal leave request on the HRMS Portal within 1 working day of your return. For sick leave exceeding 2 consecutive days, upload a medical certificate."),
        ("What happens if I exhaust all my leave balance?", "Any additional absence will be marked as Loss of Pay (LOP). You may apply for leave without pay through the HRMS Portal, which requires reporting manager and HR approval."),
        ("How is earned leave encashment calculated?", "Up to 5 days of unused earned leave may be encashed at your basic pay rate at the end of the financial year, subject to reporting manager approval."),
        ("What if I need to work on a public holiday?", "Work on a public holiday requires prior approval from your reporting manager. You will be entitled to a compensatory off to be taken within 30 days."),
        ("Is the 15-minute grace period cumulative?", "No. The grace period applies per day. However, if you are consistently late (more than 3 times in a month), the pattern will be flagged."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-HR-POL-002")
    add_demo_footer(doc)
    return save_doc(doc, "NST-HR-POL-002_Leave_Attendance_Working_Hours_v1.0.docx")

# ============================================================================
# DOCUMENT 3: Code of Conduct & Workplace Ethics (NST-HR-POL-003)
# ============================================================================
def build_code_of_conduct():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-HR-POL-003", "Code of Conduct & Workplace Ethics",
                    "Ishita Rao, Head of Human Resources (EMP-002)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This policy sets out the professional conduct, ethical standards and workplace behaviour expectations "
        "for all employees of Northstar Technologies. It applies at all company locations (Nagpur, Pune and "
        "Bengaluru) and during company-related activities including business travel, client engagements and "
        "online communications on company platforms.")

    doc.add_heading("2. Core Values", level=1)
    values = [
        ("Integrity", "Communicate honestly and act responsibly in all professional interactions."),
        ("Respect", "Create a safe, inclusive and professional workplace free from harassment, discrimination and bullying."),
        ("Customer Focus", "Understand requirements and deliver practical value to customers."),
        ("Ownership", "Take responsibility for quality, commitments and outcomes."),
        ("Learning", "Share knowledge and improve skills continuously."),
        ("Security and Privacy", "Protect company, customer and employee information."),
    ]
    for title, desc in values:
        p = doc.add_paragraph()
        run = p.add_run(title + ": ")
        run.bold = True
        p.add_run(desc)

    doc.add_heading("3. Professional Conduct Standards", level=1)
    standards = [
        "Treat all colleagues, clients and visitors with courtesy and professionalism.",
        "Arrive on time for meetings and commitments. Communicate proactively if delays are unavoidable.",
        "Use company resources and equipment responsibly and only for authorised purposes.",
        "Maintain confidentiality of proprietary information, client data and employee personal data.",
        "Follow the dress code: business casual on regular days, formal attire for client-facing engagements.",
        "Avoid the use of offensive, discriminatory or inappropriate language in any company communication channel.",
        "Report any suspected illegal activity, policy violation or ethical concern to your manager or HR.",
    ]
    for s in standards:
        doc.add_paragraph(s, style="List Bullet")

    doc.add_heading("4. Anti-Harassment and Non-Discrimination", level=1)
    doc.add_paragraph(
        "Northstar Technologies is committed to providing a workplace free from harassment, bullying and "
        "discrimination on any ground including but not limited to gender, religion, caste, ethnicity, age, "
        "disability, sexual orientation or marital status.")
    doc.add_paragraph(
        "Harassment includes unwelcome verbal, physical or visual conduct that creates a hostile, intimidating "
        "or offensive work environment. Employees who experience or witness harassment should report it to "
        "HR at hr.grievance@northstar.example or through the POSH Committee at posh.committee@northstar.example.")

    doc.add_heading("4.1 Prevention of Sexual Harassment (POSH)", level=2)
    doc.add_paragraph(
        "The company follows the framework established under the Sexual Harassment of Women at Workplace "
        "(Prevention, Prohibition and Redressal) Act, 2013. An Internal Committee has been designated with the "
        "contact address posh.committee@northstar.example. Complaints are treated confidentially and investigated "
        "within the timelines prescribed under the Act.")
    p_note = doc.add_paragraph()
    run_note = p_note.add_run(
        "Note: The Internal Committee Chairperson role is currently unassigned in this demonstration version. "
        "In a real deployment, a senior woman employee must be appointed as required by the Act.")
    run_note.italic = True
    add_statutory_note(doc)

    doc.add_heading("5. Conflict of Interest", level=1)
    doc.add_paragraph(
        "Employees must disclose any situation where their personal, financial or family interests may conflict "
        "with the interests of the company or its clients. Examples include:")
    conflicts = [
        "Holding a financial interest in a competitor, vendor or client company.",
        "Engaging in outside employment or consulting that competes with or interferes with duties at Northstar.",
        "Accepting gifts, hospitality or favours from vendors, clients or business partners beyond a nominal value of ₹1,500.",
        "Hiring or supervising a close relative without prior HR disclosure and approval.",
    ]
    for c in conflicts:
        doc.add_paragraph(c, style="List Bullet")
    doc.add_paragraph(
        "Disclosures should be submitted to the Head of HR (Ishita Rao, EMP-002) in writing. "
        "Undisclosed conflicts may result in disciplinary action.")

    doc.add_heading("6. Confidentiality and Intellectual Property", level=1)
    doc.add_paragraph(
        "All employees are bound by confidentiality obligations from their date of joining. This includes:")
    ip_items = [
        "Proprietary source code, algorithms and technical designs.",
        "Client data, project specifications and business agreements.",
        "Financial information, pricing and business plans.",
        "Employee personal data and HR records.",
        "Internal communications and strategic discussions.",
    ]
    for item in ip_items:
        doc.add_paragraph(item, style="List Bullet")
    doc.add_paragraph(
        "Intellectual property created during employment belongs to Northstar Technologies as specified in the "
        "employment agreement. Confidentiality obligations survive the end of employment.")

    doc.add_heading("7. Use of Company Resources", level=1)
    doc.add_paragraph(
        "Company-provided equipment, systems and communication tools are primarily for business purposes. "
        "Limited personal use is permitted provided it does not interfere with work, violate any policy "
        "or consume significant resources. Detailed rules are in the Information Security & Acceptable Use "
        "Policy (NST-IT-POL-001).")

    doc.add_heading("8. Reporting Violations", level=1)
    doc.add_paragraph(
        "Employees who become aware of a policy violation, ethical concern or suspected illegal activity "
        "should report it to:")
    channels = [
        "Their reporting manager (for routine matters).",
        "HR at hr.grievance@northstar.example (for confidential or sensitive matters).",
        "The POSH Committee at posh.committee@northstar.example (for harassment complaints).",
        "IT Security at security@northstar.example (for security or data protection concerns).",
    ]
    for ch in channels:
        doc.add_paragraph(ch, style="List Bullet")
    doc.add_paragraph(
        "The company prohibits retaliation against any employee who reports a concern in good faith.")

    doc.add_heading("9. Consequences of Violation", level=1)
    doc.add_paragraph(
        "Violations of this Code of Conduct may result in disciplinary action as outlined in the Employee "
        "Handbook (NST-HR-POL-001), ranging from verbal counselling to termination of employment depending "
        "on the severity of the violation.")

    doc.add_heading("10. Related Documents", level=1)
    for ref in ["NST-HR-POL-001 — Employee Handbook",
                "NST-IT-POL-001 — Information Security & Acceptable Use Policy",
                "NST-HR-POL-007 — Performance Review & Promotion Policy"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("11. Frequently Asked Questions", level=1)
    faqs = [
        ("Can I accept a gift from a client?", "Gifts of nominal value (up to ₹1,500) such as company-branded items or festival sweets may be accepted. Anything above this value must be disclosed to HR and may need to be returned."),
        ("What should I do if I witness harassment?", "Report it to HR at hr.grievance@northstar.example or to the POSH Committee at posh.committee@northstar.example. You may also speak to your manager if you are comfortable doing so. All reports are treated confidentially."),
        ("Am I allowed to take freelance work outside office hours?", "Outside work that competes with or interferes with your duties at Northstar is not permitted. Other freelance work must be disclosed to HR for a conflict-of-interest review before you engage in it."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-HR-POL-003")
    add_demo_footer(doc)
    return save_doc(doc, "NST-HR-POL-003_Code_of_Conduct_v1.0.docx")

# ============================================================================
# DOCUMENT 4: Remote Work & Work From Home Policy (NST-HR-POL-004)
# ============================================================================
def build_remote_work():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-HR-POL-004", "Remote Work & Work From Home Policy",
                    "Ishita Rao, Head of Human Resources (EMP-002)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This policy defines the terms and conditions for remote work and work-from-home (WFH) arrangements "
        "at Northstar Technologies. The company follows an office-first working model, and remote work is "
        "available as a structured benefit subject to eligibility, approval and compliance requirements.")

    doc.add_heading("2. Eligibility", level=1)
    doc.add_paragraph("The following criteria must be met to be eligible for regular remote work:")
    elig = [
        "The employee must be a confirmed employee who has completed the 6-month probation period.",
        "The employee's role must not require mandatory on-site presence (for example, IT infrastructure or facilities roles may be excluded).",
        "The employee must have a satisfactory performance record with no active performance improvement plan.",
        "The employee must have a reliable broadband internet connection and a suitable home work environment.",
    ]
    for e in elig:
        doc.add_paragraph(e, style="List Bullet")

    doc.add_heading("3. Remote Work Arrangements", level=1)
    table = doc.add_table(rows=4, cols=3)
    table.style = "Table Grid"
    arrangements = [
        ("Arrangement", "Details", "Approval Required"),
        ("Regular Hybrid", "Up to 2 remote days per week on pre-agreed days", "Reporting Manager with HR notification"),
        ("Occasional WFH", "Ad-hoc remote day for specific circumstances (delivery, appointment)", "Reporting Manager (same-day Slack/email notification)"),
        ("Full Remote", "Exceptional cases only — medical, family or extraordinary circumstances", "Department Head + HR, reviewed quarterly"),
    ]
    for i, row_data in enumerate(arrangements):
        for j, val in enumerate(row_data):
            table.rows[i].cells[j].text = val

    doc.add_heading("4. Employee Responsibilities During Remote Work", level=1)
    responsibilities = [
        "Use the company-provided laptop for all work activities. Personal devices must not access company data without MDM enrollment and IT approval.",
        "Connect through the company VPN (vpn.northstar.example) when accessing internal systems or tools.",
        "Be available on Slack and Google Meet during core office hours (10:00 AM to 7:00 PM).",
        "Mark attendance on the HRMS Portal by 10:30 AM.",
        "Maintain a professional environment during video meetings.",
        "Secure the company laptop — use a screen lock, do not work from public Wi-Fi without VPN, and do not leave the device unattended.",
        "Respond to messages and meeting invitations within the same timelines as in the office.",
    ]
    for r in responsibilities:
        doc.add_paragraph(r, style="List Bullet")

    doc.add_heading("5. Equipment and Connectivity", level=1)
    doc.add_paragraph(
        "The company provides a laptop to all employees. No separate stipend is provided for home internet, "
        "furniture or other home office expenses. Employees experiencing connectivity issues during remote work "
        "must inform their manager immediately and, if necessary, attend the office.")

    doc.add_heading("6. Revocation", level=1)
    doc.add_paragraph(
        "Remote work arrangements may be revoked with 5 working days' notice if the employee fails to comply "
        "with this policy, if performance deteriorates, or if business requirements change. The reporting manager "
        "must document the rationale and notify HR.")

    doc.add_heading("7. Related Documents", level=1)
    for ref in ["NST-HR-POL-001 — Employee Handbook",
                "NST-HR-POL-002 — Leave, Attendance & Working Hours Policy",
                "NST-IT-POL-001 — Information Security & Acceptable Use Policy"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("8. Frequently Asked Questions", level=1)
    faqs = [
        ("Can I work remotely during my probation period?", "No. Regular remote work is available only to confirmed employees who have completed the 6-month probation period. Occasional WFH may be granted in exceptional circumstances with manager approval."),
        ("Can I work from a different city for an extended period?", "Extended remote work from a different city requires a Full Remote arrangement, which needs Department Head and HR approval and is reviewed quarterly."),
        ("Do I get a stipend for my home internet?", "No. The company does not provide a separate stipend for home internet or home office setup at this time."),
        ("How many days per week can I work from home?", "Up to 2 days per week under the Regular Hybrid arrangement, on pre-agreed days with your reporting manager."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-HR-POL-004")
    add_demo_footer(doc)
    return save_doc(doc, "NST-HR-POL-004_Remote_Work_WFH_v1.0.docx")

print("Starting document generation...")
files = []
files.append(build_employee_handbook())
files.append(build_leave_policy())
files.append(build_code_of_conduct())
files.append(build_remote_work())
print(f"\nBatch 1 complete: {len(files)} documents generated.")

