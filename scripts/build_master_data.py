"""
Build the comprehensive Northstar Company Master Data JSON.
This is the single source of truth for all fictional policy values,
role assignments, approval limits, SLAs, and access control.
"""
import json
import os
from datetime import datetime

DEMO_LABEL = "DEMONSTRATION ONLY — NOT APPROVED FOR REAL-WORLD USE"
STATUTORY_NOTE = "Statutory position to be verified by qualified legal/HR counsel before real-world use."
TIMESTAMP = "2026-11-07"

# Load directory data
with open('knowledge_base/09_source_extracts/directory_integrity_report.json', 'r', encoding='utf-8') as f:
    dir_data = json.load(f)

master_data = {
    "_metadata": {
        "title": "Northstar Technologies — Company Master Data",
        "demonstration_label": DEMO_LABEL,
        "version": "1.0",
        "created": TIMESTAMP,
        "integrity_status": dir_data['directory_integrity_status'],
        "statutory_note": STATUTORY_NOTE
    },

    "Company_Profile": {
        "company_name": "Northstar Technologies",
        "industry": "Information Technology, Software Engineering and Data Services",
        "head_office": "Nagpur, Maharashtra, India",
        "other_offices": ["Pune, Maharashtra, India", "Bengaluru, Karnataka, India"],
        "business_model": "Business-to-business software development and technology consulting",
        "core_services": "Custom software development; web and API engineering; data analytics; cloud solutions; AI-enabled applications",
        "working_model": "Office-first with approved hybrid and remote arrangements under the applicable policies",
        "website": "https://northstar.example",
        "general_email": "hello@northstar.example",
        "fiscal_year": "April 1 to March 31",
        "currency": "INR (₹)",
        "provenance": "DIR"
    },

    "Departments": [
        {"code": "HR", "name": "Human Resources", "responsibilities": dir_data['departments'][0]['responsibilities'], "provenance": "DIR"},
        {"code": "IT", "name": "Information Technology", "responsibilities": dir_data['departments'][1]['responsibilities'], "provenance": "DIR"},
        {"code": "ENG", "name": "Engineering", "responsibilities": dir_data['departments'][2]['responsibilities'], "provenance": "DIR"},
        {"code": "DA", "name": "Data & Analytics", "responsibilities": dir_data['departments'][3]['responsibilities'], "provenance": "DIR"},
        {"code": "FIN", "name": "Finance & Administration", "responsibilities": dir_data['departments'][4]['responsibilities'], "provenance": "DIR"},
        {"code": "SCS", "name": "Sales & Customer Success", "responsibilities": dir_data['departments'][5]['responsibilities'], "provenance": "DIR"},
    ],

    "Offices": [
        {"location": "Nagpur", "state": "Maharashtra", "type": "Head Office", "provenance": "DIR"},
        {"location": "Pune", "state": "Maharashtra", "type": "Branch Office", "provenance": "DIR"},
        {"location": "Bengaluru", "state": "Karnataka", "type": "Branch Office", "provenance": "DIR"},
    ],

    "Employee_Directory_Source": dir_data['employees_source'],
    "Employee_Directory_Derived": dir_data['employees_derived'],

    "Role_Assignments": [
        {"role": "CEO", "employee_id": "EMP-001", "name": "Aarav Mehta", "provenance": "DIR", "decision_id": None},
        {"role": "Head of HR / HR Policy Owner", "employee_id": "EMP-002", "name": "Ishita Rao", "provenance": "DIR", "decision_id": None},
        {"role": "HR Business Partner", "employee_id": "EMP-003", "name": "Rohan Deshpande", "provenance": "DIR", "decision_id": None},
        {"role": "IT Manager / IT Policy Owner", "employee_id": "EMP-004", "name": "Neha Kulkarni", "provenance": "DIR", "decision_id": None},
        {"role": "IT Support Specialist", "employee_id": "EMP-005", "name": "Kabir Shah", "provenance": "DIR", "decision_id": None},
        {"role": "Engineering Manager / ENG Policy Owner", "employee_id": "EMP-006", "name": "Ananya Iyer", "provenance": "DIR", "decision_id": None},
        {"role": "Data & Analytics Manager / DA Policy Owner", "employee_id": "EMP-009", "name": "Dev Patel", "provenance": "DIR", "decision_id": None},
        {"role": "Finance Manager / FIN Policy Owner", "employee_id": "EMP-011", "name": "Arjun Bhat", "provenance": "DIR", "decision_id": None},
        {"role": "Customer Success Manager / SCS Policy Owner", "employee_id": "EMP-013", "name": "Rahul Sethi", "provenance": "DIR", "decision_id": None},
        {"role": "Travel & Administration Coordinator", "employee_id": "EMP-012", "name": "Tara Menon", "provenance": "DIR", "decision_id": None},
        {"role": "Chief Technology Officer", "employee_id": None, "name": "UNASSIGNED — role referenced in directory but no person listed", "provenance": "DIR", "decision_id": "DEC-001"},
        {"role": "Chief Operating Officer", "employee_id": None, "name": "UNASSIGNED — role referenced in directory but no person listed", "provenance": "DIR", "decision_id": "DEC-001"},
        {"role": "Chief Financial Officer", "employee_id": None, "name": "UNASSIGNED — role referenced in directory but no person listed", "provenance": "DIR", "decision_id": "DEC-001"},
        {"role": "POSH Internal Committee Chairperson", "employee_id": None, "name": "UNASSIGNED — no suitable employee identified", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-002"},
        {"role": "Information Security Officer", "employee_id": "EMP-004", "name": "Neha Kulkarni (dual-hat as IT Manager)", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-003"},
    ],

    "Policy_Values": {
        "probation_period_months": {"value": 6, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-004"},
        "notice_period_days_probation": {"value": 30, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-004"},
        "notice_period_days_confirmed": {"value": 60, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-004"},
        "retirement_age": {"value": 60, "provenance": "STATUTORY-FLAGGED", "decision_id": "DEC-005", "legal_review_id": "LR-001"},
        "dress_code": {"value": "Business casual on regular days; formal attire for client-facing meetings", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-006"},
        "pay_cycle": {"value": "Monthly, last working day of each calendar month", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-007"},
    },

    "Leave_and_Attendance": {
        "casual_leave_days": {"value": 12, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-008", "statutory_note": STATUTORY_NOTE, "legal_review_id": "LR-002"},
        "sick_leave_days": {"value": 12, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-008", "statutory_note": STATUTORY_NOTE, "legal_review_id": "LR-002"},
        "earned_leave_days": {"value": 15, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-008", "statutory_note": STATUTORY_NOTE, "legal_review_id": "LR-002"},
        "maternity_leave_weeks": {"value": 26, "provenance": "STATUTORY-FLAGGED", "decision_id": "DEC-009", "statutory_note": STATUTORY_NOTE, "legal_review_id": "LR-003"},
        "paternity_leave_days": {"value": 5, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-009", "statutory_note": STATUTORY_NOTE, "legal_review_id": "LR-003"},
        "bereavement_leave_days": {"value": 5, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-010"},
        "comp_off_validity_days": {"value": 30, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-010"},
        "leave_year": {"value": "January 1 to December 31", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-008"},
        "max_leave_carry_forward_days": {"value": 5, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-008"},
        "leave_encashment": {"value": "Up to 5 days of earned leave at basic pay at financial year-end, subject to manager approval", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-008"},
        "half_day_leave": {"value": "Permitted for casual and sick leave", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-008"},
        "leave_approval_chain": {"value": "Employee → Reporting Manager → HR (for > 3 consecutive days)", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-011"},
        "attendance_marking": {"value": "Daily through HRMS self-service portal by 10:30 AM", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-012"},
        "late_arrival_grace_minutes": {"value": 15, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-012"},
        "unauthorised_absence_threshold_days": {"value": 3, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-012"},
    },

    "Working_Hours": {
        "standard_hours_per_day": {"value": 9, "note": "including 1-hour lunch break", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-013"},
        "standard_hours_per_week": {"value": 45, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-013"},
        "core_office_hours": {"value": "10:00 AM to 7:00 PM", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-013"},
        "flexible_start_window": {"value": "9:00 AM to 10:30 AM (manager-approved)", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-013"},
        "overtime_policy": {"value": "Overtime must be pre-approved by reporting manager. Compensation through compensatory off (comp-off) within 30 days. No direct overtime pay unless specifically agreed for project needs.", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-014", "statutory_note": STATUTORY_NOTE, "legal_review_id": "LR-004"},
        "work_week": {"value": "Monday to Friday", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-013"},
    },

    "Remote_Work": {
        "eligibility": {"value": "All confirmed employees who have completed probation. Roles requiring on-site presence (IT infrastructure, facilities) may be excluded.", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-015"},
        "max_remote_days_per_week": {"value": 2, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-015"},
        "approval_authority": {"value": "Reporting Manager with HR notification", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-015"},
        "equipment_provision": {"value": "Company laptop must be used. No stipend for home internet or furniture.", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-015"},
        "connectivity_requirement": {"value": "Stable broadband connection, available on company communication tools during core hours", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-015"},
        "full_remote_arrangement": {"value": "Exceptional cases only, requires Head of Department and HR approval, reviewed quarterly", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-015"},
    },

    "Approval_Authority_Matrix": [
        {"action": "Leave (≤ 3 days)", "approver": "Reporting Manager", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-011"},
        {"action": "Leave (> 3 days)", "approver": "Reporting Manager + HR", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-011"},
        {"action": "Expense claim (≤ ₹5,000)", "approver": "Reporting Manager", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-016"},
        {"action": "Expense claim (₹5,001–₹25,000)", "approver": "Department Head + Finance", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-016"},
        {"action": "Expense claim (> ₹25,000)", "approver": "Department Head + Finance Manager + CEO", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-016"},
        {"action": "Travel request (domestic)", "approver": "Reporting Manager + Finance", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-017"},
        {"action": "Travel request (international)", "approver": "Department Head + Finance Manager + CEO", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-017"},
        {"action": "Software/tool purchase (≤ ₹10,000)", "approver": "IT Manager", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-018"},
        {"action": "Software/tool purchase (> ₹10,000)", "approver": "IT Manager + Finance Manager", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-018"},
        {"action": "New employee hire", "approver": "Department Head + HR + CEO", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-019"},
        {"action": "Remote work arrangement", "approver": "Reporting Manager + HR notification", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-015"},
        {"action": "Promotion", "approver": "Reporting Manager + Department Head + HR + CEO", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-020"},
        {"action": "Policy exception", "approver": "Department Head + HR + CEO", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-021"},
    ],

    "Expense_Limits": {
        "daily_meal_allowance_inr": {"value": 500, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-022"},
        "local_transport_per_trip_max_inr": {"value": 1500, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-022"},
        "mobile_reimbursement_monthly_inr": {"value": 500, "note": "For employees with approved business mobile use", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-022"},
        "claim_submission_deadline_days": {"value": 30, "note": "From date of expense", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-023"},
        "receipt_required_above_inr": {"value": 250, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-023"},
        "reimbursement_processing_days": {"value": 15, "note": "Working days from approved claim submission", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-023"},
    },

    "Travel_Rules": {
        "domestic_air_travel_class": {"value": "Economy", "note": "Business class for journeys > 4 hours with Department Head approval", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-024"},
        "domestic_hotel_limit_inr_per_night": {
            "metro_cities": {"value": 5000, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-024"},
            "non_metro": {"value": 3500, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-024"},
        },
        "daily_diem_inr": {
            "metro_cities": {"value": 1500, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-024"},
            "non_metro": {"value": 1000, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-024"},
        },
        "advance_request_days_before_travel": {"value": 7, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-025"},
        "travel_settlement_deadline_days": {"value": 7, "note": "Working days after return", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-025"},
        "advance_max_percentage": {"value": 80, "note": "% of estimated trip cost", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-025"},
        "taxi_aggregator_allowed": {"value": True, "note": "Company-approved platforms only", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-025"},
    },

    "Referral_Rules": {
        "referral_bonus_inr": {"value": 15000, "note": "Paid after referred employee completes 6 months", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-026"},
        "eligibility": {"value": "All confirmed employees except HR recruitment team and hiring managers for the specific role", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-026"},
        "self_referral_allowed": {"value": False, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-026"},
        "max_referrals_per_quarter": {"value": 5, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-026"},
    },

    "IT_Security_Parameters": {
        "password_min_length": {"value": 12, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-027"},
        "password_expiry_days": {"value": 90, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-027"},
        "mfa_required": {"value": True, "note": "For all company systems, email and VPN", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-027"},
        "screen_lock_timeout_minutes": {"value": 5, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-027"},
        "usb_storage_policy": {"value": "Disabled by default. Exception requires IT Manager approval with business justification.", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-028"},
        "personal_device_policy": {"value": "Personal devices may not access company data without MDM enrollment and IT approval", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-028"},
        "vpn_required_for_remote": {"value": True, "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-029"},
        "data_classification_levels": {"value": ["Public", "Internal", "Confidential", "Restricted"], "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-030"},
        "incident_reporting_channel": {"value": "security@northstar.example", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-031"},
        "acceptable_use_violations_escalation": {"value": "IT Manager → HR → CEO", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-031"},
    },

    "Incident_SLA": {
        "P1_critical": {"response_minutes": 30, "resolution_hours": 4, "example": "Production system down, data breach", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-032"},
        "P2_high": {"response_minutes": 60, "resolution_hours": 8, "example": "Major feature unavailable, security vulnerability", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-032"},
        "P3_medium": {"response_hours": 4, "resolution_hours": 24, "example": "Non-critical system issue, access request", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-032"},
        "P4_low": {"response_hours": 8, "resolution_hours": 48, "example": "Minor bug, information request", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-032"},
        "escalation_path": {"value": "IT Support Specialist → IT Manager → CEO", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-032"},
    },

    "Systems_and_Tools": [
        {"name": "HRMS Portal", "purpose": "Leave, attendance, payslips, employee self-service", "url": "https://hrms.northstar.example", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-033"},
        {"name": "GitLab", "purpose": "Source code repository, CI/CD pipelines, code review", "url": "https://gitlab.northstar.example", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-033"},
        {"name": "Jira", "purpose": "Project management, issue tracking, sprint planning", "url": "https://jira.northstar.example", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-033"},
        {"name": "Confluence", "purpose": "Internal documentation and knowledge base", "url": "https://confluence.northstar.example", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-033"},
        {"name": "Slack", "purpose": "Team messaging, channels, notifications", "url": "https://northstar.slack.example", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-033"},
        {"name": "Google Workspace", "purpose": "Email, calendar, documents, video meetings", "url": "https://workspace.google.example", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-033"},
        {"name": "VPN (WireGuard)", "purpose": "Secure remote access to internal systems", "url": "vpn.northstar.example", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-033"},
        {"name": "Expense Portal", "purpose": "Expense claims, reimbursement tracking", "url": "https://expenses.northstar.example", "provenance": "FICTIONAL-DECISION", "decision_id": "DEC-033"},
    ],

    "Restricted_Units": [
        {
            "unit_id": "RU-001",
            "document": "NST-HR-POL-001 Employee Handbook",
            "section": "Disciplinary Action and Termination Procedures",
            "audience_label": "HR_ONLY",
            "allowed_groups": ["GRP_DEPT_HR"],
            "business_rationale": "Disciplinary procedures, termination steps, and HR investigation workflows contain sensitive operational details that should only be visible to the HR team.",
            "restricted_facts": [
                "Step-by-step disciplinary escalation matrix",
                "Termination checklist and exit interview protocol",
                "Suspension pending investigation procedures",
                "HR case file handling procedures"
            ],
            "authorized_test_persona": {"employee_id": "EMP-002", "name": "Ishita Rao", "group": "GRP_DEPT_HR"},
            "unauthorized_test_persona": {"employee_id": "EMP-007", "name": "Vikram Joshi", "group": "GRP_DEPT_ENG"},
            "provenance": "FICTIONAL-DECISION",
            "decision_id": "DEC-034"
        },
        {
            "unit_id": "RU-002",
            "document": "NST-IT-POL-001 Information Security & Acceptable Use Policy",
            "section": "Security Incident Response Procedures — Internal Playbook",
            "audience_label": "IT_ONLY",
            "allowed_groups": ["GRP_DEPT_IT"],
            "business_rationale": "Internal incident response playbook details (containment steps, forensic procedures, communication templates) must not be disclosed to non-IT staff to prevent adversarial knowledge.",
            "restricted_facts": [
                "Incident containment and isolation procedures",
                "Forensic evidence collection steps",
                "Internal security communication escalation matrix",
                "Breach notification decision criteria and timelines"
            ],
            "authorized_test_persona": {"employee_id": "EMP-004", "name": "Neha Kulkarni", "group": "GRP_DEPT_IT"},
            "unauthorized_test_persona": {"employee_id": "EMP-010", "name": "Sana Khan", "group": "GRP_DEPT_DA"},
            "provenance": "FICTIONAL-DECISION",
            "decision_id": "DEC-035"
        },
        {
            "unit_id": "RU-003",
            "document": "NST-FIN-POL-001 Expense Reimbursement Policy",
            "section": "Finance Audit Controls and Fraud Detection Procedures",
            "audience_label": "FINANCE_ONLY",
            "allowed_groups": ["GRP_DEPT_FIN"],
            "business_rationale": "Internal fraud detection criteria, audit sampling methods, and escalation thresholds for suspicious claims must remain confidential to the Finance team to maintain control effectiveness.",
            "restricted_facts": [
                "Fraud detection red-flag criteria for expense claims",
                "Random audit sampling percentage and selection method",
                "Finance-internal escalation path for suspected fraud",
                "Threshold amounts triggering automatic audit review"
            ],
            "authorized_test_persona": {"employee_id": "EMP-011", "name": "Arjun Bhat", "group": "GRP_DEPT_FIN"},
            "unauthorized_test_persona": {"employee_id": "EMP-013", "name": "Rahul Sethi", "group": "GRP_DEPT_SCS"},
            "provenance": "FICTIONAL-DECISION",
            "decision_id": "DEC-036"
        }
    ],

    "Access_Control_Matrix": {
        "ALL_EMPLOYEES": {"groups": ["GRP_ALL_EMPLOYEES"], "semantics": "any-of"},
        "MANAGERS": {"groups": ["GRP_MANAGERS"], "semantics": "any-of"},
        "HR_ONLY": {"groups": ["GRP_DEPT_HR"], "semantics": "any-of"},
        "IT_ONLY": {"groups": ["GRP_DEPT_IT"], "semantics": "any-of"},
        "FINANCE_ONLY": {"groups": ["GRP_DEPT_FIN"], "semantics": "any-of"},
        "SALES_ONLY": {"groups": ["GRP_DEPT_SCS"], "semantics": "any-of"},
        "ENGINEERING_ONLY": {"groups": ["GRP_DEPT_ENG"], "semantics": "any-of", "note": "ENG dept only; DA is separate"},
        "DA_ONLY": {"groups": ["GRP_DEPT_DA"], "semantics": "any-of"},
        "MANAGERS_AND_HR": {"groups": ["GRP_MANAGERS", "GRP_DEPT_HR"], "semantics": "any-of"},
    },

    "Corporate_Codes": {
        "note": "Executive Leadership is NOT a 7th department. It is a classification tag for EMP-001 (CEO) who sits above the 6 departments.",
        "executive_tag": "EXEC",
        "decision_id": "DEC-037",
        "provenance": "FICTIONAL-DECISION"
    },

    "Legal_Review_Register": [
        {"id": "LR-001", "topic": "Retirement Age", "statutory_area": "Employment / retirement", "jurisdictions": ["Maharashtra", "Karnataka"], "fictional_value": "60 years", "note": STATUTORY_NOTE, "status": "PENDING_REVIEW", "reviewer": "Qualified HR/Legal counsel"},
        {"id": "LR-002", "topic": "Leave Entitlements (CL/SL/EL)", "statutory_area": "State Shops & Establishments Acts", "jurisdictions": ["Maharashtra", "Karnataka"], "fictional_value": "CL: 12, SL: 12, EL: 15 per year", "note": STATUTORY_NOTE + " Maharashtra and Karnataka may have different statutory minimums.", "status": "PENDING_REVIEW", "reviewer": "Qualified HR/Legal counsel"},
        {"id": "LR-003", "topic": "Maternity and Paternity Leave", "statutory_area": "Maternity Benefit Act, 1961 / company policy", "jurisdictions": ["Central"], "fictional_value": "Maternity: 26 weeks; Paternity: 5 days (company benefit, not statutory)", "note": STATUTORY_NOTE, "status": "PENDING_REVIEW", "reviewer": "Qualified HR/Legal counsel"},
        {"id": "LR-004", "topic": "Overtime Compensation", "statutory_area": "Factories Act / Shops & Establishments Acts", "jurisdictions": ["Maharashtra", "Karnataka"], "fictional_value": "Comp-off only, no direct overtime pay by default", "note": STATUTORY_NOTE + " Statutory overtime rates may apply under specific Acts.", "status": "PENDING_REVIEW", "reviewer": "Qualified HR/Legal counsel"},
        {"id": "LR-005", "topic": "POSH (Prevention of Sexual Harassment)", "statutory_area": "Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013", "jurisdictions": ["Central"], "fictional_value": "Internal Committee to be constituted", "note": STATUTORY_NOTE, "status": "PENDING_REVIEW", "reviewer": "Qualified HR/Legal counsel"},
        {"id": "LR-006", "topic": "Gratuity", "statutory_area": "Payment of Gratuity Act, 1972", "jurisdictions": ["Central"], "fictional_value": "Not detailed in current policies — to be addressed", "note": STATUTORY_NOTE, "status": "PENDING_REVIEW", "reviewer": "Qualified HR/Legal counsel"},
        {"id": "LR-007", "topic": "Data Protection and Privacy", "statutory_area": "Digital Personal Data Protection Act, 2023 (India)", "jurisdictions": ["Central"], "fictional_value": "Data classification levels defined; specific compliance obligations TBD", "note": STATUTORY_NOTE, "status": "PENDING_REVIEW", "reviewer": "Qualified Legal counsel"},
        {"id": "LR-008", "topic": "Working Hours and Weekly Rest", "statutory_area": "Shops & Establishments Acts (state-specific)", "jurisdictions": ["Maharashtra", "Karnataka"], "fictional_value": "9 hours/day, 45 hours/week, Monday-Friday", "note": STATUTORY_NOTE + " Maharashtra and Karnataka shops acts may differ on maximum hours and rest day requirements.", "status": "PENDING_REVIEW", "reviewer": "Qualified HR/Legal counsel"},
    ],

    "Decision_Log": [
        {"id": "DEC-001", "topic": "Missing C-suite roles", "question": "CTO, COO, CFO titles referenced as reporting managers but no employees listed", "source_evidence": "Directory Table 2 — EMP-004, 006, 009, 011, 013 report to unlisted titles", "options_considered": ["Invent C-suite employees", "Leave unassigned, flag hierarchy"], "chosen": "Leave unassigned, flag hierarchy as UNRESOLVED_STRUCTURE", "rationale": "Spec prohibits inventing employees not in Directory", "provenance": "DIR", "affected_docs": "All documents referencing org hierarchy", "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-002", "topic": "POSH IC Chairperson", "question": "Who chairs the Internal Committee?", "source_evidence": "No POSH-related info in Directory", "options_considered": ["Assign to HR Head", "Leave unassigned"], "chosen": "Leave unassigned with functional mailbox posh.committee@northstar.example", "rationale": "Sensitive statutory role; cannot be assigned without proper context", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-003"], "legal_review": True, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-003", "topic": "Information Security Officer", "question": "Who is responsible for information security?", "source_evidence": "IT Manager (EMP-004) manages IT including endpoint security per Directory", "options_considered": ["Assign to IT Manager", "Create separate role"], "chosen": "Assign dual-hat to IT Manager (EMP-004, Neha Kulkarni)", "rationale": "Small company; IT Manager responsibilities include endpoint security per Directory", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-IT-POL-001", "NST-IT-GDE-003"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-004", "topic": "Probation and Notice Periods", "question": "What are the probation and notice periods?", "source_evidence": "No source data", "options_considered": ["3/6 month probation", "30/60/90 day notice"], "chosen": "6-month probation, 30-day notice (probation), 60-day notice (confirmed)", "rationale": "Common in Indian IT industry", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-005", "topic": "Retirement Age", "question": "What is the company retirement age?", "source_evidence": "No source data", "options_considered": ["58", "60"], "chosen": "60 years", "rationale": "Common in Indian private sector", "provenance": "STATUTORY-FLAGGED", "affected_docs": ["NST-HR-POL-001"], "legal_review": True, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-006", "topic": "Dress Code", "question": "What is the dress code?", "source_evidence": "No source data", "options_considered": ["Formal only", "Business casual", "No policy"], "chosen": "Business casual, formal for client meetings", "rationale": "Standard for Indian IT services companies", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-001", "NST-HR-POL-003"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-007", "topic": "Pay Cycle", "question": "When is salary paid?", "source_evidence": "No source data", "options_considered": ["Last working day", "1st of next month"], "chosen": "Last working day of each calendar month", "rationale": "Standard practice", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-008", "topic": "Leave Entitlements", "question": "How many leave days per type?", "source_evidence": "No source data; state acts vary", "options_considered": ["CL:7/SL:7/EL:12", "CL:12/SL:12/EL:15"], "chosen": "CL:12, SL:12, EL:15 per year, carry-forward 5 days, leave year Jan-Dec", "rationale": "Generous but common in Indian IT; flagged for statutory review", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-002"], "legal_review": True, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-009", "topic": "Maternity/Paternity Leave", "question": "What parental leave is offered?", "source_evidence": "Maternity Benefit Act mandates 26 weeks", "options_considered": ["Statutory minimum only", "Add paternity"], "chosen": "26 weeks maternity, 5 days paternity (company benefit)", "rationale": "Maternity as per Act; paternity is company benefit", "provenance": "STATUTORY-FLAGGED", "affected_docs": ["NST-HR-POL-002"], "legal_review": True, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-010", "topic": "Bereavement and Comp-off", "question": "Bereavement leave days? Comp-off validity?", "source_evidence": "No source data", "options_considered": ["3 days", "5 days"], "chosen": "5 days bereavement, 30-day comp-off validity", "rationale": "Reasonable for Indian IT", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-002"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-011", "topic": "Leave Approval Chain", "question": "Who approves leave?", "source_evidence": "No source data", "options_considered": ["Manager only", "Manager + HR for long leave"], "chosen": "Manager for ≤3 days; Manager + HR for >3 consecutive days", "rationale": "Balanced control", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-002"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-012", "topic": "Attendance Rules", "question": "Attendance marking and grace period?", "source_evidence": "No source data", "options_considered": ["No grace", "15-min grace"], "chosen": "Daily HRMS marking by 10:30 AM, 15-min grace, 3-day unauthorized absence threshold", "rationale": "Industry standard", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-002"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-013", "topic": "Working Hours", "question": "Standard working hours?", "source_evidence": "No source data", "options_considered": ["8h/40h", "9h/45h"], "chosen": "9h/day (incl. 1h lunch), 45h/week, Mon-Fri, core 10AM-7PM, flex 9-10:30AM", "rationale": "Common in Indian IT", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-002"], "legal_review": True, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-014", "topic": "Overtime Compensation", "question": "How is overtime compensated?", "source_evidence": "No source data; statutory provisions vary", "options_considered": ["Overtime pay", "Comp-off only", "Hybrid"], "chosen": "Comp-off within 30 days; no direct overtime pay by default", "rationale": "Common IT practice; flagged for statutory review", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-002"], "legal_review": True, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-015", "topic": "Remote Work Policy", "question": "Remote work rules?", "source_evidence": "Directory: 'Office-first with approved hybrid and remote'", "options_considered": ["1 day/week", "2 days/week", "3 days/week"], "chosen": "Max 2 days/week remote for confirmed employees, manager-approved, full remote exceptional", "rationale": "Aligns with Directory 'office-first' model", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-004"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-016", "topic": "Expense Approval Thresholds", "question": "Expense claim approval levels?", "source_evidence": "No source data", "options_considered": ["Flat approval", "Tiered"], "chosen": "≤₹5K: Manager; ₹5K-₹25K: Dept Head + Finance; >₹25K: Dept Head + Finance + CEO", "rationale": "Standard tiered control for SME", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-FIN-POL-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-017", "topic": "Travel Approval", "question": "Travel request approval?", "source_evidence": "No source data", "options_considered": ["Manager only", "Manager + Finance"], "chosen": "Domestic: Manager + Finance; International: Dept Head + Finance + CEO", "rationale": "Appropriate controls", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-FIN-POL-002"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-018", "topic": "Software Purchase Approval", "question": "Who approves software purchases?", "source_evidence": "No source data", "options_considered": ["IT only", "IT + Finance"], "chosen": "≤₹10K: IT Manager; >₹10K: IT Manager + Finance Manager", "rationale": "Dual control for significant purchases", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-IT-GDE-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-019", "topic": "Hiring Approval", "question": "Who approves new hires?", "source_evidence": "No source data", "options_considered": ["Manager + HR", "Manager + HR + CEO"], "chosen": "Department Head + HR + CEO", "rationale": "Small company; CEO visibility on all hires", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-005"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-020", "topic": "Promotion Approval", "question": "Who approves promotions?", "source_evidence": "No source data", "options_considered": ["Manager + HR", "Full chain"], "chosen": "Manager + Dept Head + HR + CEO", "rationale": "Ensures fairness and visibility", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-007"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-021", "topic": "Policy Exception Process", "question": "How are policy exceptions handled?", "source_evidence": "No source data", "options_considered": ["Manager", "Dept Head + HR + CEO"], "chosen": "Department Head + HR + CEO", "rationale": "Strict control for exceptions", "provenance": "FICTIONAL-DECISION", "affected_docs": ["All policies"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-022", "topic": "Meal and Transport Allowances", "question": "Daily meal and transport limits?", "source_evidence": "No source data", "options_considered": ["₹300/₹500 meal", "₹500/₹1000/₹1500 transport"], "chosen": "₹500 daily meal, ₹1,500 local transport per trip, ₹500/month mobile", "rationale": "Reasonable for Indian cities", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-FIN-POL-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-023", "topic": "Expense Claim Deadlines", "question": "Claim submission and processing timelines?", "source_evidence": "No source data", "options_considered": ["15/30 days submission", "7/15 days processing"], "chosen": "30-day submission deadline, receipt >₹250, 15 working days processing", "rationale": "Balanced for finance team capacity", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-FIN-POL-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-024", "topic": "Travel Class and Hotel Limits", "question": "Travel class and per-night hotel rates?", "source_evidence": "No source data", "options_considered": ["Economy only", "Tiered by distance"], "chosen": "Economy (business >4h with approval), Hotel: ₹5K metro/₹3.5K non-metro, Diem: ₹1.5K/₹1K", "rationale": "Reasonable for Indian IT SME", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-FIN-POL-002"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-025", "topic": "Travel Advance and Settlement", "question": "Travel advance and settlement rules?", "source_evidence": "No source data", "options_considered": ["No advance", "80% advance"], "chosen": "80% advance max, 7-day advance request lead, 7 working days settlement deadline", "rationale": "Standard practice", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-FIN-POL-002"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-026", "topic": "Employee Referral Bonus", "question": "Referral bonus amount and rules?", "source_evidence": "No source data", "options_considered": ["₹10K", "₹15K", "₹25K"], "chosen": "₹15,000 after 6-month completion, max 5 per quarter, HR/hiring managers excluded", "rationale": "Moderate for mid-size IT company", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-005"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-027", "topic": "Password Policy", "question": "Password length, expiry, MFA?", "source_evidence": "No source data", "options_considered": ["8-char/180-day", "12-char/90-day"], "chosen": "12-char minimum, 90-day expiry, MFA required for all systems", "rationale": "Industry best practice", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-IT-POL-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-028", "topic": "USB and BYOD Policy", "question": "USB and personal device rules?", "source_evidence": "No source data", "options_considered": ["Allow with logging", "Disabled by default"], "chosen": "USB disabled by default (IT exception), BYOD requires MDM enrollment", "rationale": "Security-first approach", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-IT-POL-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-029", "topic": "VPN Requirement", "question": "VPN for remote work?", "source_evidence": "No source data", "options_considered": ["Optional", "Required"], "chosen": "Required for all remote access", "rationale": "Security best practice", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-IT-POL-001", "NST-HR-POL-004"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-030", "topic": "Data Classification", "question": "Data classification levels?", "source_evidence": "No source data", "options_considered": ["3-level", "4-level"], "chosen": "Public, Internal, Confidential, Restricted", "rationale": "Industry standard 4-level model", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-IT-POL-001", "NST-DA-GDE-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-031", "topic": "Security Incident Reporting", "question": "Incident reporting channel?", "source_evidence": "No source data", "options_considered": ["Email", "Dedicated tool"], "chosen": "security@northstar.example, escalation IT Manager → HR → CEO", "rationale": "Simple for small company", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-IT-POL-001", "NST-IT-GDE-003"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-032", "topic": "Incident SLA", "question": "Response and resolution SLAs?", "source_evidence": "No source data", "options_considered": ["Single SLA", "Priority-based"], "chosen": "P1: 30min/4h, P2: 1h/8h, P3: 4h/24h, P4: 8h/48h", "rationale": "Standard ITIL-aligned SLAs", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-IT-GDE-003"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-033", "topic": "Internal Systems and Tools", "question": "Which tools does the company use?", "source_evidence": "No source data", "options_considered": ["Minimal toolset", "Full modern stack"], "chosen": "HRMS, GitLab, Jira, Confluence, Slack, Google Workspace, VPN, Expense Portal", "rationale": "Realistic stack for Indian IT SME", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-IT-GDE-001", "NST-ENG-GDE-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-034", "topic": "Restricted Unit: Disciplinary Procedures", "question": "Should disciplinary action details be HR-only?", "source_evidence": "Standard HR practice", "options_considered": ["All employees", "HR only", "Managers + HR"], "chosen": "HR_ONLY", "rationale": "Sensitive operational procedures", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-HR-POL-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-035", "topic": "Restricted Unit: Security Incident Playbook", "question": "Should incident response playbook be IT-only?", "source_evidence": "Security best practice", "options_considered": ["All employees", "IT only"], "chosen": "IT_ONLY", "rationale": "Adversarial knowledge risk", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-IT-POL-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-036", "topic": "Restricted Unit: Finance Audit Controls", "question": "Should fraud detection criteria be Finance-only?", "source_evidence": "Internal control practice", "options_considered": ["All employees", "Finance only"], "chosen": "FINANCE_ONLY", "rationale": "Protect control effectiveness", "provenance": "FICTIONAL-DECISION", "affected_docs": ["NST-FIN-POL-001"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
        {"id": "DEC-037", "topic": "Executive Leadership classification", "question": "Is Executive Leadership a 7th department?", "source_evidence": "Directory: EMP-001 dept = 'Executive Leadership'; spec says exactly 6 depts", "options_considered": ["Make 7th dept", "Classification tag"], "chosen": "Classification tag only; not a department. EMP-001 is in GRP_ALL_EMPLOYEES but no department group.", "rationale": "Spec mandates exactly 6 departments", "provenance": "FICTIONAL-DECISION", "affected_docs": ["All documents"], "legal_review": False, "date": TIMESTAMP, "status": "FINAL"},
    ],

    "Superseded_Values": [],

    "Document_Number_Map": [
        {"policy_id": "NST-HR-POL-001", "title": "Employee Handbook", "owner_emp": "EMP-002", "owner_name": "Ishita Rao", "audience": "ALL_EMPLOYEES", "restricted_sections": ["Disciplinary Action and Termination Procedures (HR_ONLY)"]},
        {"policy_id": "NST-HR-POL-002", "title": "Leave, Attendance & Working Hours Policy", "owner_emp": "EMP-002", "owner_name": "Ishita Rao", "audience": "ALL_EMPLOYEES", "restricted_sections": []},
        {"policy_id": "NST-HR-POL-003", "title": "Code of Conduct & Workplace Ethics", "owner_emp": "EMP-002", "owner_name": "Ishita Rao", "audience": "ALL_EMPLOYEES", "restricted_sections": []},
        {"policy_id": "NST-HR-POL-004", "title": "Remote Work & Work From Home Policy", "owner_emp": "EMP-002", "owner_name": "Ishita Rao", "audience": "ALL_EMPLOYEES", "restricted_sections": []},
        {"policy_id": "NST-HR-POL-005", "title": "Recruitment & Employee Referral Policy", "owner_emp": "EMP-002", "owner_name": "Ishita Rao", "audience": "ALL_EMPLOYEES", "restricted_sections": []},
        {"policy_id": "NST-HR-POL-006", "title": "Onboarding & Employee Development Policy", "owner_emp": "EMP-002", "owner_name": "Ishita Rao", "audience": "ALL_EMPLOYEES", "restricted_sections": []},
        {"policy_id": "NST-HR-POL-007", "title": "Performance Review & Promotion Policy", "owner_emp": "EMP-002", "owner_name": "Ishita Rao", "audience": "MANAGERS_AND_HR", "restricted_sections": []},
        {"policy_id": "NST-IT-POL-001", "title": "Information Security & Acceptable Use Policy", "owner_emp": "EMP-004", "owner_name": "Neha Kulkarni", "audience": "ALL_EMPLOYEES", "restricted_sections": ["Security Incident Response Procedures — Internal Playbook (IT_ONLY)"]},
        {"policy_id": "NST-IT-GDE-001", "title": "Laptop, Software & Account Setup Guide", "owner_emp": "EMP-004", "owner_name": "Neha Kulkarni", "audience": "ALL_EMPLOYEES", "restricted_sections": []},
        {"policy_id": "NST-ENG-GDE-001", "title": "Engineering Development Workflow, Git & Code Review Guide", "owner_emp": "EMP-006", "owner_name": "Ananya Iyer", "audience": "ALL_EMPLOYEES", "restricted_sections": []},
        {"policy_id": "NST-DA-GDE-001", "title": "Data Handling, Access & Analytics Delivery Guide", "owner_emp": "EMP-009", "owner_name": "Dev Patel", "audience": "ALL_EMPLOYEES", "restricted_sections": []},
        {"policy_id": "NST-FIN-POL-001", "title": "Expense Reimbursement Policy", "owner_emp": "EMP-011", "owner_name": "Arjun Bhat", "audience": "ALL_EMPLOYEES", "restricted_sections": ["Finance Audit Controls and Fraud Detection Procedures (FINANCE_ONLY)"]},
        {"policy_id": "NST-FIN-POL-002", "title": "Business Travel & Travel Expense Policy", "owner_emp": "EMP-011", "owner_name": "Arjun Bhat", "audience": "ALL_EMPLOYEES", "restricted_sections": []},
        {"policy_id": "NST-IT-GDE-003", "title": "IT Incident Management & Emergency Procedures", "owner_emp": "EMP-004", "owner_name": "Neha Kulkarni", "audience": "ALL_EMPLOYEES", "restricted_sections": []},
        {"policy_id": "CORP-001", "title": "Company Overview & Employee Directory", "owner_emp": "EMP-002", "owner_name": "Ishita Rao", "audience": "ALL_EMPLOYEES", "restricted_sections": [], "note": "Pre-existing document from source directory, preserved as-is"},
    ],
}

# Save
os.makedirs('knowledge_base/01_master_data', exist_ok=True)
with open('knowledge_base/01_master_data/northstar_master_data.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=2, ensure_ascii=False)

print("Master Data created successfully.")
print(f"Decision Log entries: {len(master_data['Decision_Log'])}")
print(f"Legal Review entries: {len(master_data['Legal_Review_Register'])}")
print(f"Document Number Map entries: {len(master_data['Document_Number_Map'])}")
print(f"Restricted Units: {len(master_data['Restricted_Units'])}")
print(f"Policy values defined: {sum(1 for _ in master_data['Policy_Values'])}")
print(f"Approval matrix entries: {len(master_data['Approval_Authority_Matrix'])}")

