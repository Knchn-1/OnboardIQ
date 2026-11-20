import json
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.office import Office
from app.models.department import Department
from app.models.employee import Employee
from app.models.role_assignment import RoleAssignment

POLICY_OWNER_TO_DEPT_CODE = {
    "Head of HR / HR Policy Owner": "HR",
    "IT Manager / IT Policy Owner": "IT",
    "Engineering Manager / ENG Policy Owner": "ENG",
    "Data & Analytics Manager / DA Policy Owner": "DA",
    "Finance Manager / FIN Policy Owner": "FIN",
    "Customer Success Manager / SCS Policy Owner": "SCS",
}

def seed_organization(session: Session | None = None) -> None:
    """Seed offices, departments, employees, and role_assignments idempotently in one transaction."""
    close_session = False
    if session is None:
        session = SessionLocal()
        close_session = True

    master_data_file = settings.KNOWLEDGE_BASE_DIR / "01_master_data" / "northstar_master_data.json"
    if not master_data_file.exists():
        raise FileNotFoundError(f"Master data file not found: {master_data_file}")

    with open(master_data_file, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    try:
        # 1. Offices
        office_name_to_id: dict[str, int] = {}
        for off_data in master_data["Offices"]:
            name = off_data["location"]
            state = off_data["state"]
            office_type = off_data["type"]

            office = session.execute(
                select(Office).where(Office.name == name)
            ).scalar_one_or_none()

            if office is None:
                office = Office(name=name, state=state, office_type=office_type)
                session.add(office)
                session.flush()
            else:
                office.state = state
                office.office_type = office_type
                session.flush()

            office_name_to_id[name] = office.id

        # 2. Departments (exactly the 6 from "Departments")
        dept_code_to_id: dict[str, int] = {}
        for dept_data in master_data["Departments"]:
            code = dept_data["code"]
            name = dept_data["name"]
            responsibilities = dept_data["responsibilities"]

            dept = session.execute(
                select(Department).where(Department.code == code)
            ).scalar_one_or_none()

            if dept is None:
                dept = Department(code=code, name=name, responsibilities=responsibilities)
                session.add(dept)
                session.flush()
            else:
                dept.name = name
                dept.responsibilities = responsibilities
                session.flush()

            dept_code_to_id[code] = dept.id

        # 3. Employees sorted by employee_code
        emp_code_to_id: dict[str, int] = {}
        sorted_employees = sorted(
            master_data["Employee_Directory_Derived"],
            key=lambda e: e["employee_id"],
        )

        for emp_data in sorted_employees:
            emp_code = emp_data["employee_id"]
            dept_code = emp_data["department_code"]
            location = emp_data["location"]

            if location not in office_name_to_id:
                raise ValueError(f"Location '{location}' for employee {emp_code} does not match any office.")

            office_id = office_name_to_id[location]

            # EXEC is NOT a department
            if dept_code == "EXEC":
                department_id = None
            else:
                if dept_code not in dept_code_to_id:
                    raise ValueError(f"Unknown department code '{dept_code}' for employee {emp_code}")
                department_id = dept_code_to_id[dept_code]

            reports_to_emp_id = emp_data.get("reports_to_emp_id")
            manager_id = None
            if reports_to_emp_id:
                assert reports_to_emp_id in emp_code_to_id, (
                    f"Manager {reports_to_emp_id} does not exist yet for {emp_code}"
                )
                manager_id = emp_code_to_id[reports_to_emp_id]

            employee = session.execute(
                select(Employee).where(Employee.employee_code == emp_code)
            ).scalar_one_or_none()

            if employee is None:
                employee = Employee(
                    employee_code=emp_code,
                    full_name=emp_data["full_name"],
                    first_name=emp_data["first_name"],
                    last_name=emp_data["last_name"],
                    job_title=emp_data["job_title"],
                    email=emp_data["email"],
                    office_id=office_id,
                    department_id=department_id,
                    directory_department=emp_data["department_full"],
                    reports_to_title=emp_data.get("reports_to_title"),
                    manager_id=manager_id,
                    is_active=True,
                    provenance=emp_data.get("_provenance", "DIR"),
                )
                session.add(employee)
                session.flush()
            else:
                employee.full_name = emp_data["full_name"]
                employee.first_name = emp_data["first_name"]
                employee.last_name = emp_data["last_name"]
                employee.job_title = emp_data["job_title"]
                employee.email = emp_data["email"]
                employee.office_id = office_id
                employee.department_id = department_id
                employee.directory_department = emp_data["department_full"]
                employee.reports_to_title = emp_data.get("reports_to_title")
                employee.manager_id = manager_id
                employee.is_active = True
                employee.provenance = emp_data.get("_provenance", "DIR")
                session.flush()

            emp_code_to_id[emp_code] = employee.id

        # 4. Role Assignments (all 15 rows)
        for role_data in master_data["Role_Assignments"]:
            role_title = role_data["role"]
            assigned_emp_code = role_data.get("employee_id")

            if assigned_emp_code is None:
                status = "UNASSIGNED"
                employee_id = None
            else:
                status = "ASSIGNED"
                if assigned_emp_code not in emp_code_to_id:
                    raise ValueError(f"Assigned employee {assigned_emp_code} not found for role '{role_title}'")
                employee_id = emp_code_to_id[assigned_emp_code]

            if "Policy Owner" in role_title:
                if role_title not in POLICY_OWNER_TO_DEPT_CODE:
                    raise ValueError(f"Unexpected policy owner role title: '{role_title}'")
                dept_code = POLICY_OWNER_TO_DEPT_CODE[role_title]
                department_id = dept_code_to_id[dept_code]
                is_department_lead = True
            else:
                is_department_lead = False
                department_id = None

            role_assignment = session.execute(
                select(RoleAssignment).where(RoleAssignment.role_title == role_title)
            ).scalar_one_or_none()

            if role_assignment is None:
                role_assignment = RoleAssignment(
                    role_title=role_title,
                    employee_id=employee_id,
                    department_id=department_id,
                    is_department_lead=is_department_lead,
                    status=status,
                    provenance=role_data["provenance"],
                    decision_id=role_data.get("decision_id"),
                )
                session.add(role_assignment)
                session.flush()
            else:
                role_assignment.employee_id = employee_id
                role_assignment.department_id = department_id
                role_assignment.is_department_lead = is_department_lead
                role_assignment.status = status
                role_assignment.provenance = role_data["provenance"]
                role_assignment.decision_id = role_data.get("decision_id")
                session.flush()

        session.commit()
        print("Organization seed completed successfully!")
        print(f"Seeded: {len(office_name_to_id)} offices, {len(dept_code_to_id)} departments, "
              f"{len(emp_code_to_id)} employees, {len(master_data['Role_Assignments'])} role assignments.")
    except Exception:
        session.rollback()
        raise
    finally:
        if close_session:
            session.close()

if __name__ == "__main__":
    seed_organization()
