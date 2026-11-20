"""
Phase 5: Generate Batch 4 Northstar Technologies policy/guide DOCX documents.
Documents 13 to 15:
  - NST-FIN-POL-002: Business Travel & Travel Expense Policy
  - NST-IT-GDE-003: IT Incident Management & Emergency Procedures
  - CORP-001: Company Overview & Employee Directory
"""
import json
import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUTPUT_DIR = "output/02_documents_docx"
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open("output/01_master_data/northstar_master_data.json", "r", encoding="utf-8") as f:
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
# DOCUMENT 13: Business Travel & Travel Expense Policy (NST-FIN-POL-002)
# ============================================================================
def build_travel_policy():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-FIN-POL-002", "Business Travel & Travel Expense Policy",
                    "Arjun Bhat, Finance Manager (EMP-011)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This policy governs all official business travel undertaken by employees of Northstar Technologies. It establishes "
        "entitlements for transportation, lodging limits, daily allowances, travel advances, and claim settlement timelines. "
        "It applies to domestic and international travel originating from Nagpur, Pune, and Bengaluru.")

    doc.add_heading("2. Travel Coordination and Pre-Approval", level=1)
    doc.add_paragraph(
        "All business travel must be coordinated through the dedicated corporate Travel Desk managed by Tara Menon, "
        "Travel & Administration Coordinator (EMP-012) at tara.menon@northstar.example. Travel authorization must be "
        "secured prior to booking tickets or hotels:")
    table_app = doc.add_table(rows=3, cols=2)
    table_app.style = "Table Grid"
    app_data = [
        ("Travel Classification", "Mandatory Approval Path"),
        ("Domestic Business Travel", "Reporting Manager + Finance Team (Arjun Bhat, EMP-011)"),
        ("International Business Travel", "Department Head + Finance Manager (Arjun Bhat) + CEO (Aarav Mehta, EMP-001)"),
    ]
    for i, row in enumerate(app_data):
        for j, val in enumerate(row):
            table_app.rows[i].cells[j].text = val

    doc.add_heading("3. Transportation & Air Travel Guidelines", level=1)
    doc.add_paragraph(
        "Transportation arrangements must balance cost prudence with traveler safety:")
    trans_rules = [
        "Air Travel Class: All domestic flights are booked in Economy Class. Business Class is strictly restricted to continuous flight durations exceeding 4 hours, subject to written Department Head pre-approval.",
        "Rail Travel: AC 2-Tier or AC 3-Tier is authorized for inter-city travel where train journeys are practical.",
        "Local Transport at Destination: Pre-paid airport taxis or authorized ride-hailing aggregators (Uber, Ola) are approved up to ₹1,500 per one-way transfer. Rental car hire requires Department Head pre-approval.",
    ]
    for tr in trans_rules:
        doc.add_paragraph(tr, style="List Bullet")

    doc.add_heading("4. Accommodation and Daily Per Diem Allowances", level=1)
    doc.add_paragraph(
        "Lodging and incidental allowances are tiered based on destination city cost-of-living:")
    table_hotel = doc.add_table(rows=3, cols=3)
    table_hotel.style = "Table Grid"
    hotel_data = [
        ("City Tier Classification", "Hotel Room Limit (per night, excl. tax)", "Daily Per Diem Allowance"),
        ("Metro Cities (Mumbai, Delhi NCR, Bengaluru, Hyderabad, Chennai, Kolkata)", "₹5,000", "₹1,500 per day"),
        ("Non-Metro Cities (Nagpur, Pune, Ahmedabad, Kochi, Jaipur, and other cities)", "₹3,500", "₹1,000 per day"),
    ]
    for i, row in enumerate(hotel_data):
        for j, val in enumerate(row):
            table_hotel.rows[i].cells[j].text = val
    doc.add_paragraph()
    doc.add_paragraph(
        "The daily per diem allowance covers meals, local transit incidentals, and tips. Itemized food bills are not "
        "required when claiming within the standard per diem limits; however, proof of travel/boarding pass is mandatory.")

    doc.add_heading("5. Travel Advances and Expense Settlement", level=1)
    doc.add_heading("5.1 Travel Advance Requests", level=2)
    doc.add_paragraph(
        "Employees may request a travel cash advance for official trips. Advance requests must be submitted to Tara Menon "
        "at least 7 calendar days prior to the departure date. The maximum allowable advance is 80% of the projected total trip "
        "expenditure (excluding airfare booked directly by the Travel Desk).")

    doc.add_heading("5.2 Post-Travel Claim Settlement Deadline", level=2)
    doc.add_paragraph(
        "Upon completion of travel, employees must submit their finalized travel expense settlement report via the Expense Portal "
        "within 7 working days of returning to their home base. Boarding passes, original hotel tax invoices, and local transit receipts "
        "must be attached. Unspent travel advance balances must be refunded via bank transfer to Northstar Technologies within the "
        "same 7 working day window. Failure to settle advances within 15 working days results in automatic payroll deduction.")

    doc.add_heading("6. Related Documents", level=1)
    for ref in ["NST-FIN-POL-001 — Expense Reimbursement Policy",
                "NST-HR-POL-001 — Employee Handbook",
                "NST-HR-POL-003 — Code of Conduct & Workplace Ethics"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("7. Frequently Asked Questions", level=1)
    faqs = [
        ("Who coordinates hotel and flight bookings?", "Tara Menon, Travel & Administration Coordinator (EMP-012) handles all official bookings once your travel requisition is approved."),
        ("What is the hotel ceiling in Bengaluru or Mumbai?", "Metro cities have a hotel room ceiling of ₹5,000 per night excluding taxes."),
        ("How soon must I settle my travel advance after returning?", "You must submit your expense settlement and refund any surplus advance within 7 working days of your return."),
        ("Can I fly Business Class for domestic client visits?", "Domestic flights are Economy Class only. Business Class requires a flight duration over 4 hours and explicit Department Head sign-off."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-FIN-POL-002")
    add_demo_footer(doc)
    return save_doc(doc, "NST-FIN-POL-002_Business_Travel_Policy_v1.0.docx")

# ============================================================================
# DOCUMENT 14: IT Incident Management & Emergency Procedures (NST-IT-GDE-003)
# ============================================================================
def build_incident_management_guide():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "NST-IT-GDE-003", "IT Incident Management & Emergency Procedures",
                    "Neha Kulkarni, IT Manager (EMP-004)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES")

    doc.add_heading("1. Purpose and Scope", level=1)
    doc.add_paragraph(
        "This guide defines operational protocols for identifying, categorizing, reporting, escalating, and resolving "
        "IT infrastructure disruptions, software outages, and cybersecurity incidents at Northstar Technologies. It covers "
        "all corporate and client-hosted environments supporting offices in Nagpur, Pune, and Bengaluru.")

    doc.add_heading("2. Incident Severity Classification & Service Level Agreements (SLAs)", level=1)
    doc.add_paragraph(
        "All reported incidents are assigned a priority rating dictating mandatory response and resolution targets:")
    table_sla = doc.add_table(rows=5, cols=4)
    table_sla.style = "Table Grid"
    sla_data = [
        ("Severity Level", "Operational Definition & Example", "Response SLA", "Resolution SLA"),
        ("P1 — Critical", "Total outage of production service, customer-facing platform down, confirmed data breach", "30 minutes", "4 hours"),
        ("P2 — High", "Core system degraded, significant performance disruption, major security vulnerability identified", "60 minutes", "8 hours"),
        ("P3 — Medium", "Non-critical functionality impaired, individual developer system down, access provisioning delay", "4 hours", "24 hours"),
        ("P4 — Low", "Minor defect with workaround, cosmetic UI bug, general informational technical query", "8 hours", "48 hours"),
    ]
    for i, row in enumerate(sla_data):
        for j, val in enumerate(row):
            table_sla.rows[i].cells[j].text = val

    doc.add_heading("3. Incident Escalation & Response Workflow", level=1)
    doc.add_paragraph(
        "Incident resolution follows a structured three-tiered escalation path:")
    esc_steps = [
        "Tier 1 (Triage & Initial Remediation): Kabir Shah, IT Support Specialist (EMP-005) conducts initial diagnostics, opens incident ticket in Jira Service Desk, and applies standard playbooks.",
        "Tier 2 (Managerial Escalation & War Room): If unresolved within 50% of the SLA window or for any P1/P2 incident, escalation proceeds to Neha Kulkarni, IT Manager (EMP-004), who convenes an emergency virtual war room on Slack #it-war-room.",
        "Tier 3 (Executive Notification): For critical P1 incidents threatening customer SLAs or data security, Neha Kulkarni briefs CEO Aarav Mehta (EMP-001) within 60 minutes of confirmation.",
    ]
    for es in esc_steps:
        doc.add_paragraph(es, style="List Bullet")

    doc.add_heading("4. Emergency Contact Channels", level=1)
    doc.add_paragraph(
        "Employees and system monitoring alerts must direct urgent incident notifications to:")
    contacts = [
        "Email Reporting: security@northstar.example (monitored 24/7 with automated PagerDuty alerting).",
        "Urgent Helpdesk: it.support@northstar.example / Kabir Shah (EMP-005).",
        "Dedicated Slack Channel: #it-emergency and #it-helpdesk.",
        "IT Management: Neha Kulkarni (EMP-004) at neha.kulkarni@northstar.example.",
    ]
    for c in contacts:
        doc.add_paragraph(c, style="List Bullet")

    doc.add_heading("5. Post-Incident Review (PIR) and Root Cause Analysis (RCA)", level=1)
    doc.add_paragraph(
        "Following the resolution of any P1 or P2 incident, the engineering and IT teams must conduct a blameless Post-Incident "
        "Review within 3 business days. An RCA document identifying underlying architectural flaws, timeline of events, and "
        "preventative action items must be published to Confluence and shared with engineering leadership.")

    doc.add_heading("6. Related Documents", level=1)
    for ref in ["NST-IT-POL-001 — Information Security & Acceptable Use Policy",
                "NST-IT-GDE-001 — Laptop, Software & Account Setup Guide",
                "NST-ENG-GDE-001 — Engineering Development Workflow Guide"]:
        doc.add_paragraph(ref, style="List Bullet")

    doc.add_heading("7. Frequently Asked Questions", level=1)
    faqs = [
        ("What is the response time for a critical P1 outage?", "P1 incidents require an initial response within 30 minutes and resolution within 4 hours."),
        ("Where do I report an active IT system outage?", "Post immediately in Slack #it-emergency and email security@northstar.example."),
        ("Who leads the emergency war room during a major incident?", "IT Manager Neha Kulkarni (EMP-004) convenes and leads the incident war room."),
    ]
    for q, a in faqs:
        p_q = doc.add_paragraph()
        run_q = p_q.add_run("Q: " + q)
        run_q.bold = True
        doc.add_paragraph("A: " + a)

    add_revision_history(doc, "NST-IT-GDE-003")
    add_demo_footer(doc)
    return save_doc(doc, "NST-IT-GDE-003_IT_Incident_Management_v1.0.docx")

# ============================================================================
# DOCUMENT 15: Company Overview & Employee Directory (CORP-001)
# ============================================================================
def build_company_directory_doc():
    doc = Document()
    add_demo_banner(doc)
    add_title_block(doc, "CORP-001", "Company Overview & Employee Directory",
                    "Human Resources & Administration (Ishita Rao, EMP-002)",
                    "Aarav Mehta, CEO (EMP-001)",
                    "ALL_EMPLOYEES")

    doc.add_heading("1. About the Company", level=1)
    doc.add_paragraph(
        "Northstar Technologies is a fictional India-based technology services and product engineering company created "
        "for the OnboardIQ demonstration environment. The company designs and builds software platforms, data solutions, "
        "and cloud-based applications for business customers. All company details, employee names, roles, email addresses, "
        "and contact channels in this document are sample demonstration data and do not describe a real organization or real people.")

    doc.add_heading("2. Company Profile", level=1)
    table_prof = doc.add_table(rows=9, cols=2)
    table_prof.style = "Table Grid"
    prof_data = [
        ("Company Name", "Northstar Technologies"),
        ("Industry", "Information Technology, Software Engineering and Data Services"),
        ("Head Office", "Nagpur, Maharashtra, India (fictional address/location)"),
        ("Other Work Locations", "Pune and Bengaluru, India (fictional locations)"),
        ("Business Model", "Business-to-business software development and technology consulting"),
        ("Core Services", "Custom software development; web and API engineering; data analytics; cloud solutions; AI-enabled applications"),
        ("Working Model", "Office-first with approved hybrid and remote arrangements under the applicable policies"),
        ("Official Website", "https://northstar.example (reserved example domain; not a live website)"),
        ("General Contact", "hello@northstar.example (fictional email address; not monitored)"),
    ]
    for i, row in enumerate(prof_data):
        for j, val in enumerate(row):
            table_prof.rows[i].cells[j].text = val

    doc.add_heading("3. Vision, Mission and Values", level=1)
    doc.add_heading("3.1 Vision", level=2)
    doc.add_paragraph("To make useful technology accessible, reliable and impactful for organizations and the people they serve.")
    doc.add_heading("3.2 Mission", level=2)
    doc.add_paragraph("To understand customer and employee needs, build dependable digital solutions, use data responsibly, and continuously improve through collaboration and learning.")
    doc.add_heading("3.3 Core Values", level=2)
    vals = [
        ("Integrity:", "Communicate honestly and act responsibly."),
        ("Respect:", "Create a safe, inclusive and professional workplace."),
        ("Customer Focus:", "Understand requirements and deliver practical value."),
        ("Ownership:", "Take responsibility for quality, commitments and outcomes."),
        ("Learning:", "Share knowledge and improve skills continuously."),
        ("Security and Privacy:", "Protect company, customer and employee information."),
    ]
    for v_title, v_desc in vals:
        p = doc.add_paragraph()
        run = p.add_run(v_title + " ")
        run.bold = True
        p.add_run(v_desc)

    doc.add_heading("4. Organization Structure and Departments", level=1)
    doc.add_paragraph("Northstar Technologies is organized into exactly six departments:")
    table_dept = doc.add_table(rows=7, cols=2)
    table_dept.style = "Table Grid"
    dept_data = [
        ("Department", "Primary Responsibilities"),
        ("Human Resources (HR)", "Recruitment, onboarding, employee records, leave administration, employee relations, learning and performance processes."),
        ("Information Technology (IT)", "Employee devices and accounts, access provisioning, IT support, infrastructure, endpoint security and incident coordination."),
        ("Engineering (ENG)", "Software design and development, code review, testing, release processes, technical documentation and application maintenance."),
        ("Data & Analytics (DA)", "Data engineering, data quality, reporting, analytics, machine learning and responsible use of data."),
        ("Finance & Administration (FIN)", "Budgets, invoices, expense verification, reimbursements, payroll coordination, travel administration and office facilities."),
        ("Sales & Customer Success (SCS)", "Customer discovery, proposals, account coordination, customer communication and service feedback."),
    ]
    for i, row in enumerate(dept_data):
        for j, val in enumerate(row):
            table_dept.rows[i].cells[j].text = val

    doc.add_heading("5. Employee Directory", level=1)
    doc.add_paragraph(
        "The directory below contains the authoritative roster of employees for Northstar Technologies. All records "
        "preserve the verbatim source data character-for-character:")
    table_emp = doc.add_table(rows=14, cols=6)
    table_emp.style = "Table Grid"
    emp_headers = ["Employee ID", "Name", "Job Title", "Department", "Reports To", "Email / Location"]
    for j, h in enumerate(emp_headers):
        table_emp.rows[0].cells[j].text = h
    
    # Verbatim employees from source table 2
    raw_employees = [
        ("EMP-001", "Aarav Mehta", "Chief Executive Officer", "Executive Leadership", "Board of Directors", "aarav.mehta@northstar.example\nNagpur"),
        ("EMP-002", "Ishita Rao", "Head of Human Resources", "Human Resources", "Chief Executive Officer", "ishita.rao@northstar.example\nNagpur"),
        ("EMP-003", "Rohan Deshpande", "HR Business Partner", "Human Resources", "Head of Human Resources", "rohan.deshpande@northstar.example\nPune"),
        ("EMP-004", "Neha Kulkarni", "IT Manager", "Information Technology", "Chief Operating Officer", "neha.kulkarni@northstar.example\nNagpur"),
        ("EMP-005", "Kabir Shah", "IT Support Specialist", "Information Technology", "IT Manager", "kabir.shah@northstar.example\nNagpur"),
        ("EMP-006", "Ananya Iyer", "Engineering Manager", "Engineering", "Chief Technology Officer", "ananya.iyer@northstar.example\nBengaluru"),
        ("EMP-007", "Vikram Joshi", "Senior Software Engineer", "Engineering", "Engineering Manager", "vikram.joshi@northstar.example\nPune"),
        ("EMP-008", "Mira Nair", "Software Engineer", "Engineering", "Engineering Manager", "mira.nair@northstar.example\nNagpur"),
        ("EMP-009", "Dev Patel", "Data & Analytics Manager", "Data & Analytics", "Chief Technology Officer", "dev.patel@northstar.example\nBengaluru"),
        ("EMP-010", "Sana Khan", "Data Analyst", "Data & Analytics", "Data & Analytics Manager", "sana.khan@northstar.example\nNagpur"),
        ("EMP-011", "Arjun Bhat", "Finance Manager", "Finance & Administration", "Chief Financial Officer", "arjun.bhat@northstar.example\nPune"),
        ("EMP-012", "Tara Menon", "Travel & Administration Coordinator", "Finance & Administration", "Finance Manager", "tara.menon@northstar.example\nNagpur"),
        ("EMP-013", "Rahul Sethi", "Customer Success Manager", "Sales & Customer Success", "Chief Operating Officer", "rahul.sethi@northstar.example\nBengaluru"),
    ]
    for i, row in enumerate(raw_employees, start=1):
        for j, val in enumerate(row):
            table_emp.rows[i].cells[j].text = val

    doc.add_heading("6. Who to Contact (Routing Guidance)", level=1)
    table_route = doc.add_table(rows=8, cols=3)
    table_route.style = "Table Grid"
    route_data = [
        ("Reason for Contact", "Team", "Sample Contact"),
        ("Recruitment, joining documents, employee records", "Human Resources", "ishita.rao@northstar.example"),
        ("Leave, attendance, workplace concerns", "Human Resources", "rohan.deshpande@northstar.example"),
        ("Laptop, email account, access or IT issue", "Information Technology", "kabir.shah@northstar.example"),
        ("Software development, code review or release workflow", "Engineering", "ananya.iyer@northstar.example"),
        ("Data platform, analytics or reporting questions", "Data & Analytics", "dev.patel@northstar.example"),
        ("Expense reimbursement, invoices or travel claims", "Finance & Administration", "arjun.bhat@northstar.example"),
        ("Customer account or service query", "Sales & Customer Success", "rahul.sethi@northstar.example"),
    ]
    for i, row in enumerate(route_data):
        for j, val in enumerate(row):
            table_route.rows[i].cells[j].text = val

    doc.add_heading("7. General Contact and Escalation Guidance", level=1)
    guidelines = [
        "For routine operational questions, contact the designated department contact or your direct reporting manager.",
        "For IT access or equipment trouble, reach Kabir Shah (EMP-005); escalate unresolved tickets to IT Manager Neha Kulkarni (EMP-004).",
        "For employee relations, workplace concerns, or onboarding inquiries, contact HR Business Partner Rohan Deshpande (EMP-003).",
        "For expense, travel advance, or invoice inquiries, contact Arjun Bhat (EMP-011) or Tara Menon (EMP-012).",
        "For suspected information security incidents, immediately notify security@northstar.example.",
    ]
    for g in guidelines:
        doc.add_paragraph(g, style="List Bullet")

    doc.add_heading("8. Document Governance & Directory Anomaly Notes", level=1)
    doc.add_paragraph(
        "Owner: Human Resources & Administration. Review frequency: Bi-annually or upon organizational restructuring. "
        "Notice of Structural Anomaly: In accordance with Project QA standards, the reporting hierarchy currently lists "
        "reports to unlisted executive roles (CTO, COO, CFO). This structure is logged under Anomaly Report ANOM-002 through "
        "ANOM-007 and flagged as UNRESOLVED_STRUCTURE awaiting corporate human administrator confirmation.")

    add_revision_history(doc, "CORP-001")
    add_demo_footer(doc)
    return save_doc(doc, "CORP-001_Company_Overview_Directory_v1.0.docx")

print("Starting Batch 4 document generation...")
files = []
files.append(build_travel_policy())
files.append(build_incident_management_guide())
files.append(build_company_directory_doc())
print(f"\nBatch 4 complete: {len(files)} documents generated.")

