from typing import TYPE_CHECKING
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Identity,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.office import Office
    from app.models.department import Department
    from app.models.role_assignment import RoleAssignment

class Employee(Base, TimestampMixin):
    __tablename__ = "employees"
    __table_args__ = (
        CheckConstraint(
            "employee_code ~ '^EMP-[0-9]{3}$'",
            name="valid_employee_code",
        ),
        CheckConstraint(
            "manager_id IS NULL OR manager_id <> id",
            name="manager_not_self",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    employee_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    job_title: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    office_id: Mapped[int | None] = mapped_column(ForeignKey("offices.id"), nullable=True)
    department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id"), nullable=True)
    directory_department: Mapped[str] = mapped_column(Text, nullable=False)
    reports_to_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="RESTRICT"),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False,
    )
    provenance: Mapped[str] = mapped_column(Text, nullable=False)

    office: Mapped["Office | None"] = relationship(back_populates="employees")
    department: Mapped["Department | None"] = relationship(back_populates="employees")
    manager: Mapped["Employee | None"] = relationship(
        "Employee",
        remote_side="Employee.id",
        back_populates="direct_reports",
    )
    direct_reports: Mapped[list["Employee"]] = relationship(
        "Employee",
        back_populates="manager",
    )
    role_assignments: Mapped[list["RoleAssignment"]] = relationship(back_populates="employee")
