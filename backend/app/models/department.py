from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, Identity, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.employee import Employee
    from app.models.role_assignment import RoleAssignment

class Department(Base, TimestampMixin):
    __tablename__ = "departments"
    __table_args__ = (
        CheckConstraint(
            "code IN ('HR', 'IT', 'ENG', 'DA', 'FIN', 'SCS')",
            name="valid_code",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    responsibilities: Mapped[str] = mapped_column(Text, nullable=False)

    employees: Mapped[list["Employee"]] = relationship(back_populates="department")
    role_assignments: Mapped[list["RoleAssignment"]] = relationship(back_populates="department")
