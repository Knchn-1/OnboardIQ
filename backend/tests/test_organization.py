import json
import sys
from pathlib import Path
import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.seed_org import seed_organization
from app.models.department import Department
from app.models.employee import Employee
from app.models.office import Office
from app.models.role_assignment import RoleAssignment

REPO_ROOT = Path(__file__).resolve().parents[2]
MASTER_DATA_PATH = REPO_ROOT / "knowledge_base" / "01_master_data" / "northstar_master_data.json"

# Import ReferenceAuthorizer via sys.path
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from reference_authorizer import ReferenceAuthorizer


def load_master_data() -> dict:
    with open(MASTER_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_a_departments_and_employees_counts(db_session: Session):
    """Exactly 6 departments with the exact codes; exactly 13 employees EMP-001..EMP-013."""
    departments = db_session.execute(select(Department)).scalars().all()
    assert len(departments) == 6
    dept_codes = {d.code for d in departments}
    expected_codes = {"HR", "IT", "ENG", "DA", "FIN", "SCS"}
    assert dept_codes == expected_codes

    employees = db_session.execute(
        select(Employee).order_by(Employee.employee_code)
    ).scalars().all()
    assert len(employees) == 13
    emp_codes = [e.employee_code for e in employees]
    expected_emp_codes = [f"EMP-{i:03d}" for i in range(1, 14)]
    assert emp_codes == expected_emp_codes


def test_b_emp_001_executive(db_session: Session):
    """EMP-001: department_id IS NULL, directory_department = 'Executive Leadership',
    reports_to_title = 'Board of Directors', manager_id IS NULL."""
    emp = db_session.execute(
        select(Employee).where(Employee.employee_code == "EMP-001")
    ).scalar_one()

    assert emp.department_id is None
    assert emp.directory_department == "Executive Leadership"
    assert emp.reports_to_title == "Board of Directors"
    assert emp.manager_id is None


def test_c_employee_reporting_chain_and_managers(db_session: Session):
    """For all 13 employees: reports_to_title equals master data value and the manager's
    employee_code equals reports_to_emp_id (or both NULL). Exactly 6 employees have manager_id NULL."""
    md = load_master_data()
    md_employees = {e["employee_id"]: e for e in md["Employee_Directory_Derived"]}

    employees = db_session.execute(select(Employee)).scalars().all()
    emp_by_id = {e.id: e for e in employees}

    null_manager_count = 0
    for emp in employees:
        md_emp = md_employees[emp.employee_code]
        assert emp.reports_to_title == md_emp.get("reports_to_title")

        expected_manager_code = md_emp.get("reports_to_emp_id")
        if expected_manager_code is None:
            assert emp.manager_id is None
            null_manager_count += 1
        else:
            assert emp.manager_id is not None
            actual_manager = emp_by_id[emp.manager_id]
            assert actual_manager.employee_code == expected_manager_code

    assert null_manager_count == 6


def test_d_role_assignments(db_session: Session):
    """role_assignments: 15 rows; 4 UNASSIGNED; EMP-004 holds 2 roles; exactly 6 department leads, one per department."""
    roles = db_session.execute(select(RoleAssignment)).scalars().all()
    assert len(roles) == 15

    unassigned_roles = [r for r in roles if r.status == "UNASSIGNED"]
    assert len(unassigned_roles) == 4
    for r in unassigned_roles:
        assert r.employee_id is None

    emp_004 = db_session.execute(
        select(Employee).where(Employee.employee_code == "EMP-004")
    ).scalar_one()
    emp_004_roles = [r for r in roles if r.employee_id == emp_004.id]
    assert len(emp_004_roles) == 2

    dept_leads = [r for r in roles if r.is_department_lead]
    assert len(dept_leads) == 6
    lead_dept_ids = {r.department_id for r in dept_leads}
    assert len(lead_dept_ids) == 6
    assert None not in lead_dept_ids


def test_e_employee_groups_view_and_authorizer_parity(db_session: Session):
    """employee_groups equals ReferenceAuthorizer.resolve_principal_groups for all 13 employees.
    An inactive employee yields no groups."""
    authorizer = ReferenceAuthorizer(str(MASTER_DATA_PATH))
    employees = db_session.execute(select(Employee)).scalars().all()

    for emp in employees:
        ref_groups = authorizer.resolve_principal_groups(emp.employee_code)
        view_result = db_session.execute(
            text("SELECT group_code FROM employee_groups WHERE employee_id = :id"),
            {"id": emp.id},
        ).fetchall()
        view_groups = {row[0] for row in view_result}
        assert view_groups == ref_groups, f"Mismatch for {emp.employee_code}: {view_groups} != {ref_groups}"

    # Test that an inactive employee yields no groups
    test_emp = db_session.execute(
        select(Employee).where(Employee.employee_code == "EMP-005")
    ).scalar_one()
    test_emp.is_active = False
    db_session.flush()

    inactive_groups = db_session.execute(
        text("SELECT group_code FROM employee_groups WHERE employee_id = :id"),
        {"id": test_emp.id},
    ).fetchall()
    assert len(inactive_groups) == 0

    # Restore active state
    test_emp.is_active = True
    db_session.flush()


def test_f_seeding_idempotency(db_session: Session):
    """Seeding twice leaves the row counts unchanged."""
    seed_organization(db_session)

    offices_count = db_session.scalar(text("SELECT count(*) FROM offices"))
    departments_count = db_session.scalar(text("SELECT count(*) FROM departments"))
    employees_count = db_session.scalar(text("SELECT count(*) FROM employees"))
    roles_count = db_session.scalar(text("SELECT count(*) FROM role_assignments"))

    assert offices_count == 3
    assert departments_count == 6
    assert employees_count == 13
    assert roles_count == 15


def test_g_constraints_enforcement(db_session: Session):
    """Constraints reject: duplicate employee_code, self-manager, an ASSIGNED role
    with NULL employee_id, and a 7th department code."""
    # 1. Duplicate employee_code
    with pytest.raises(IntegrityError):
        dup_emp = Employee(
            employee_code="EMP-001",
            full_name="Duplicate Employee",
            first_name="Duplicate",
            last_name="Employee",
            job_title="Duplicate",
            email="dup.emp@northstar.example",
            directory_department="Executive Leadership",
            provenance="TEST",
        )
        db_session.add(dup_emp)
        db_session.flush()
    db_session.rollback()

    # 2. Self-manager
    emp_002 = db_session.execute(
        select(Employee).where(Employee.employee_code == "EMP-002")
    ).scalar_one()
    with pytest.raises(IntegrityError):
        emp_002.manager_id = emp_002.id
        db_session.flush()
    db_session.rollback()

    # 3. ASSIGNED role with NULL employee_id
    with pytest.raises(IntegrityError):
        bad_role = RoleAssignment(
            role_title="Ghost Officer",
            employee_id=None,
            status="ASSIGNED",
            provenance="TEST",
        )
        db_session.add(bad_role)
        db_session.flush()
    db_session.rollback()

    # 4. 7th department code
    with pytest.raises(IntegrityError):
        bad_dept = Department(
            code="LEGAL",
            name="Legal Affairs",
            responsibilities="Legal compliance and contracts",
        )
        db_session.add(bad_dept)
        db_session.flush()
    db_session.rollback()
