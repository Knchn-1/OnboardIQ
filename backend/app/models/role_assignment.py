from typing import TYPE_CHECKING
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Identity,
    Index,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.department import Department
    from app.models.employee import Employee

class RoleAssignment(Base, TimestampMixin):
    __tablename__ = "role_assignments"
    __table_args__ = (
        CheckConstraint(
            "status IN ('ASSIGNED', 'UNASSIGNED')",
            name="valid_status",
        ),
        CheckConstraint(
            "((status = 'ASSIGNED') = (employee_id IS NOT NULL))",
            name="status_employee_match",
        ),
        Index(
            "uq_role_assignments_department_lead",
            "department_id",
            unique=True,
            postgresql_where=text("is_department_lead = true"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    role_title: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    employee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id"), nullable=True)
    department_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id"), nullable=True)
    is_department_lead: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("false"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    provenance: Mapped[str] = mapped_column(Text, nullable=False)
    decision_id: Mapped[str | None] = mapped_column(String(50), nullable=True)

    employee: Mapped["Employee | None"] = relationship(back_populates="role_assignments")
    department: Mapped["Department | None"] = relationship(back_populates="role_assignments")
