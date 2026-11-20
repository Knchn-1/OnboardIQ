"""
Phase 1: Directory Integrity Analysis
Parse employee directory, detect anomalies, build integrity report.
"""
import json
import os

# Load extracted data
with open('knowledge_base/09_source_extracts/directory_tables.json', 'r', encoding='utf-8') as f:
    tables = json.load(f)

# Table 0: Company Profile (9 rows x 2 cols)
company_profile = {}
for row in tables[0]['rows']:
    company_profile[row[0]] = row[1]

# Table 1: Departments (7 rows x 2 cols, row 0 = header)
departments = []
for row in tables[1]['rows'][1:]:
    departments.append({'name': row[0], 'responsibilities': row[1]})

# Table 2: Employee Directory (14 rows x 6 cols, row 0 = header)
employees = []
header = tables[2]['rows'][0]
for row in tables[2]['rows'][1:]:
    emp = {}
    for i, col in enumerate(header):
        emp[col] = row[i]
    # Split Email / Location
    email_loc = emp.get('Email / Location', '')
    parts = email_loc.split('\n')
    emp['email'] = parts[0].strip() if len(parts) >= 1 else ''
    emp['location'] = parts[1].strip() if len(parts) >= 2 else ''
    employees.append(emp)

# Table 3: Contact routing (8 rows x 3 cols)
contacts = []
for row in tables[3]['rows'][1:]:
    contacts.append({'reason': row[0], 'team': row[1], 'contact': row[2]})

# ======================================
# DIRECTORY ANOMALY DETECTION
# ======================================
anomalies = []
anomaly_id = 0

def add_anomaly(category, severity, emp_ids, description, evidence, proposed_resolution):
    global anomaly_id
    anomaly_id += 1
    anomalies.append({
        'anomaly_id': f'ANOM-{anomaly_id:03d}',
        'category': category,
        'severity': severity,
        'affected_employees': emp_ids,
        'description': description,
        'evidence': evidence,
        'proposed_resolution': proposed_resolution,
        'status': 'PROPOSED, awaiting human approval'
    })

# 1. Check for duplicate Employee IDs
emp_ids = [e['Employee ID'] for e in employees]
seen_ids = set()
for eid in emp_ids:
    if eid in seen_ids:
        add_anomaly('DUPLICATE_ID', 'CRITICAL', [eid],
                     f'Duplicate Employee ID: {eid}',
                     f'ID {eid} appears multiple times in directory table.',
                     'De-duplicate or assign unique IDs.')
    seen_ids.add(eid)

# 2. Check for duplicate emails
emails = [e['email'] for e in employees]
seen_emails = set()
for i, email in enumerate(emails):
    if email in seen_emails:
        add_anomaly('DUPLICATE_EMAIL', 'HIGH', [employees[i]['Employee ID']],
                     f'Duplicate email: {email}',
                     f'Email {email} appears for multiple employees.',
                     'Assign unique email addresses.')
    seen_emails.add(email)

# 3. Department mapping - check against the 6 canonical departments
canonical_depts = {
    'Human Resources': 'HR',
    'Information Technology': 'IT',
    'Engineering': 'ENG',
    'Data & Analytics': 'DA',
    'Finance & Administration': 'FIN',
    'Sales & Customer Success': 'SCS'
}
non_canonical = set()
for e in employees:
    dept = e['Department']
    if dept not in canonical_depts and dept != 'Executive Leadership':
        non_canonical.add(dept)

# EMP-001 has "Executive Leadership" which is NOT one of the 6 departments
add_anomaly('DEPARTMENT_MISMATCH', 'MEDIUM', ['EMP-001'],
            'EMP-001 (Aarav Mehta, CEO) has department "Executive Leadership" which is not one of the 6 canonical departments (HR, IT, ENG, DA, FIN, SCS).',
            'Directory Table 2, row for EMP-001: Department = "Executive Leadership".',
            'Record as anomaly. The CEO role is above the 6 departments. Do not force into a department. Use "Executive Leadership" as a classification tag, not a 7th department. Log this in Decision Log.')

# 4. Reporting chain validation
emp_by_title = {}
for e in employees:
    emp_by_title[e['Job title']] = e

# Check each employee's "Reports to" resolves to someone
reports_to_titles = set()
for e in employees:
    rt = e['Reports to']
    reports_to_titles.add(rt)

missing_managers = []
for e in employees:
    rt = e['Reports to']
    if rt == 'Board of Directors':
        continue  # CEO reports to board - ok
    # Check if any employee has this title
    found = False
    for other in employees:
        if other['Job title'] == rt:
            found = True
            break
    if not found:
        missing_managers.append((e['Employee ID'], e['Name'], rt))

# EMP-004 reports to "Chief Operating Officer" - no COO in directory
# EMP-006 reports to "Chief Technology Officer" - no CTO in directory
# EMP-009 reports to "Chief Technology Officer" - no CTO in directory
# EMP-011 reports to "Chief Financial Officer" - no CFO in directory
# EMP-013 reports to "Chief Operating Officer" - no COO in directory
if missing_managers:
    for emp_id, name, manager_title in missing_managers:
        add_anomaly('MISSING_MANAGER', 'HIGH', [emp_id],
                     f'{emp_id} ({name}) reports to "{manager_title}" but no employee with that title exists in the directory.',
                     f'Directory Table 2: {emp_id} Reports to = "{manager_title}". No row has Job title = "{manager_title}".',
                     f'Record as unresolved. The "{manager_title}" role exists but the person is not listed in the directory. Flag hierarchy as UNRESOLVED_STRUCTURE.')

# 5. Check for self-reporting
for e in employees:
    if e['Reports to'] == e['Job title']:
        add_anomaly('SELF_REPORTING', 'HIGH', [e['Employee ID']],
                     f'{e["Employee ID"]} reports to their own title.',
                     f'Reports to = Job title = "{e["Job title"]}".',
                     'Correct reporting line.')

# 6. Check location consistency
valid_locations = {'Nagpur', 'Pune', 'Bengaluru'}
for e in employees:
    if e['location'] and e['location'] not in valid_locations:
        add_anomaly('INVALID_LOCATION', 'LOW', [e['Employee ID']],
                     f'Location "{e["location"]}" not in expected set.',
                     f'Expected: {valid_locations}',
                     'Verify location.')

# 7. Build hierarchy / detect cycles
def build_hierarchy():
    """Attempt to build reporting hierarchy."""
    # Map title -> employee
    title_to_emp = {}
    for e in employees:
        title_to_emp[e['Job title']] = e
    
    hierarchy = {}
    for e in employees:
        hierarchy[e['Employee ID']] = {
            'name': e['Name'],
            'title': e['Job title'],
            'department': e['Department'],
            'reports_to_title': e['Reports to'],
            'reports_to_emp_id': None,
            'direct_reports': [],
            'location': e['location'],
            'email': e['email']
        }
        # Find manager
        if e['Reports to'] != 'Board of Directors':
            for other in employees:
                if other['Job title'] == e['Reports to']:
                    hierarchy[e['Employee ID']]['reports_to_emp_id'] = other['Employee ID']
                    break
    
    # Build direct reports
    for eid, data in hierarchy.items():
        mgr_id = data['reports_to_emp_id']
        if mgr_id and mgr_id in hierarchy:
            hierarchy[mgr_id]['direct_reports'].append(eid)
    
    return hierarchy

hierarchy = build_hierarchy()

# 8. Check for multiple roots
roots = [eid for eid, data in hierarchy.items() if data['reports_to_emp_id'] is None]
orphans = []
for eid in roots:
    if hierarchy[eid]['reports_to_title'] != 'Board of Directors':
        orphans.append(eid)

if len(orphans) > 0:
    add_anomaly('ORPHANED_EMPLOYEES', 'HIGH', orphans,
                 f'{len(orphans)} employees have no resolvable manager in the directory (their manager title does not match any listed employee).',
                 f'Orphaned: {", ".join(orphans)} — their Reports to titles point to unlisted CTO/COO/CFO roles.',
                 'The directory omits C-suite roles (CTO, COO, CFO). Hierarchy is incomplete. Mark as UNRESOLVED_STRUCTURE.')

# ======================================
# INTEGRITY STATUS DETERMINATION
# ======================================
has_critical = any(a['severity'] == 'CRITICAL' for a in anomalies)
has_high = any(a['severity'] == 'HIGH' for a in anomalies)
has_missing_managers = len(missing_managers) > 0

if has_critical:
    integrity_status = 'FLAGGED'
elif has_missing_managers:
    integrity_status = 'UNRESOLVED_STRUCTURE'
else:
    integrity_status = 'CLEAN'

# ======================================
# BUILD DERIVED EMPLOYEE DATA
# ======================================
def dept_code(dept_name):
    return canonical_depts.get(dept_name, 'EXEC' if dept_name == 'Executive Leadership' else 'UNKNOWN')

employees_source = []
employees_derived = []
for e in employees:
    # Source: verbatim
    employees_source.append({
        'Employee ID': e['Employee ID'],
        'Name': e['Name'],
        'Job title': e['Job title'],
        'Department': e['Department'],
        'Reports to': e['Reports to'],
        'Email / Location': e.get('Email / Location', f"{e['email']}\n{e['location']}"),
        '_provenance': 'DIR'
    })
    # Derived: normalized
    h = hierarchy.get(e['Employee ID'], {})
    employees_derived.append({
        'employee_id': e['Employee ID'],
        'full_name': e['Name'],
        'first_name': e['Name'].split()[0],
        'last_name': ' '.join(e['Name'].split()[1:]),
        'job_title': e['Job title'],
        'department_full': e['Department'],
        'department_code': dept_code(e['Department']),
        'reports_to_title': e['Reports to'],
        'reports_to_emp_id': h.get('reports_to_emp_id'),
        'email': e['email'],
        'location': e['location'],
        'is_manager': len(h.get('direct_reports', [])) > 0,
        'direct_report_ids': h.get('direct_reports', []),
        'direct_report_count': len(h.get('direct_reports', [])),
        '_provenance': 'DIR (derived)'
    })

# ======================================
# GROUP MEMBERSHIP RESOLUTION
# ======================================
groups = {
    'GRP_ALL_EMPLOYEES': [e['employee_id'] for e in employees_derived],
    'GRP_MANAGERS': [e['employee_id'] for e in employees_derived if e['is_manager']],
    'GRP_DEPT_HR': [e['employee_id'] for e in employees_derived if e['department_code'] == 'HR'],
    'GRP_DEPT_IT': [e['employee_id'] for e in employees_derived if e['department_code'] == 'IT'],
    'GRP_DEPT_ENG': [e['employee_id'] for e in employees_derived if e['department_code'] == 'ENG'],
    'GRP_DEPT_DA': [e['employee_id'] for e in employees_derived if e['department_code'] == 'DA'],
    'GRP_DEPT_FIN': [e['employee_id'] for e in employees_derived if e['department_code'] == 'FIN'],
    'GRP_DEPT_SCS': [e['employee_id'] for e in employees_derived if e['department_code'] == 'SCS'],
}

# Note: EMP-001 is EXEC - not in any dept group. Handle in decision log.
# Note: Managers group requires unambiguous hierarchy. Missing managers mean some are uncertain.
manager_note = 'Manager status is derived from having direct reports within the listed directory only. Employees reporting to unlisted CTO/COO/CFO are not counted as direct reports of those roles.'

# ======================================
# SAVE ALL OUTPUTS
# ======================================
output = {
    'directory_integrity_status': integrity_status,
    'employee_count': len(employees),
    'department_count_in_table': len(departments),
    'canonical_department_count': 6,
    'anomaly_count': len(anomalies),
    'anomalies': anomalies,
    'company_profile': company_profile,
    'departments': departments,
    'employees_source': employees_source,
    'employees_derived': employees_derived,
    'hierarchy': {k: {kk: vv for kk, vv in v.items()} for k, v in hierarchy.items()},
    'groups': groups,
    'group_membership_notes': manager_note,
    'contact_routing': contacts,
    'missing_manager_titles': list(set(m[2] for m in missing_managers)),
    'roots': roots
}

os.makedirs('knowledge_base/09_source_extracts', exist_ok=True)
with open('knowledge_base/09_source_extracts/directory_integrity_report.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

# Print summary
print(f"Integrity Status: {integrity_status}")
print(f"Employees: {len(employees)}")
print(f"Anomalies: {len(anomalies)}")
for a in anomalies:
    print(f"  [{a['severity']}] {a['anomaly_id']}: {a['description'][:100]}")
print(f"\nGroups:")
for g, members in groups.items():
    print(f"  {g}: {members}")
print(f"\nMissing manager titles: {list(set(m[2] for m in missing_managers))}")
print(f"\nRoots (no resolvable manager): {roots}")

