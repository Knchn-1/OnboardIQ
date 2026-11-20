from typing import TYPE_CHECKING
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Identity,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.document_chunk import DocumentChunk

GROUPS_CHECK = (
    "cardinality(allowed_groups) >= 1 AND allowed_groups <@ ARRAY["
    "'GRP_ALL_EMPLOYEES','GRP_MANAGERS','GRP_DEPT_HR','GRP_DEPT_IT',"
    "'GRP_DEPT_ENG','GRP_DEPT_DA','GRP_DEPT_FIN','GRP_DEPT_SCS']::text[]"
)

AUDIENCE_CHECK = (
    "classification_audience IN ('ALL_EMPLOYEES', 'MANAGERS', 'MANAGERS_AND_HR', 'HR_ONLY', 'IT_ONLY', "
    "'FINANCE_ONLY', 'ENGINEERING_ONLY', 'DA_ONLY', 'SALES_ONLY')"
)

class DocumentSection(Base, TimestampMixin):
    __tablename__ = "document_sections"
    __table_args__ = (
        CheckConstraint("lifecycle_state IN ('CURRENT', 'SUPERSEDED', 'DRAFT')", name="valid_lifecycle_state"),
        CheckConstraint("index_flag IN ('INDEX', 'ARCHIVE')", name="valid_index_flag"),
        CheckConstraint(AUDIENCE_CHECK, name="valid_classification_audience"),
        CheckConstraint(GROUPS_CHECK, name="valid_allowed_groups"),
        CheckConstraint(
            "restricted_unit_id IS NULL OR restricted_unit_id IN ('RU-001', 'RU-002', 'RU-003')",
            name="valid_restricted_unit_id",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    section_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    section_number: Mapped[str] = mapped_column(String(20), nullable=False)
    section_title: Mapped[str] = mapped_column(String(200), nullable=False)
    heading_path: Mapped[str] = mapped_column(Text, nullable=False)
    page_start: Mapped[int] = mapped_column(Integer, nullable=False)
    page_end: Mapped[int] = mapped_column(Integer, nullable=False)
    classification_audience: Mapped[str] = mapped_column(String(50), nullable=False)
    allowed_groups: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    restricted_unit_id: Mapped[str | None] = mapped_column(String(20), nullable=True)
    index_flag: Mapped[str] = mapped_column(String(20), nullable=False)
    lifecycle_state: Mapped[str] = mapped_column(String(20), nullable=False)

    document: Mapped["Document"] = relationship(back_populates="sections")
    chunks: Mapped[list["DocumentChunk"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan",
    )
