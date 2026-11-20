from typing import TYPE_CHECKING
from sqlalchemy import Identity, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.employee import Employee

class Office(Base, TimestampMixin):
    __tablename__ = "offices"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    office_type: Mapped[str] = mapped_column(String(50), nullable=False)

    employees: Mapped[list["Employee"]] = relationship(back_populates="office")
