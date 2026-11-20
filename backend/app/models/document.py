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
    from app.models.employee import Employee
    from app.models.document_section import DocumentSection
    from app.models.document_chunk import DocumentChunk

GROUPS_CHECK = (
    "cardinality({col}) >= 1 AND {col} <@ ARRAY["
    "'GRP_ALL_EMPLOYEES','GRP_MANAGERS','GRP_DEPT_HR','GRP_DEPT_IT',"
    "'GRP_DEPT_ENG','GRP_DEPT_DA','GRP_DEPT_FIN','GRP_DEPT_SCS']::text[]"
)

AUDIENCE_CHECK = (
    "{col} IN ('ALL_EMPLOYEES', 'MANAGERS', 'MANAGERS_AND_HR', 'HR_ONLY', 'IT_ONLY', "
    "'FINANCE_ONLY', 'ENGINEERING_ONLY', 'DA_ONLY', 'SALES_ONLY')"
)

class Document(Base, TimestampMixin):
    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint("lifecycle_state IN ('CURRENT', 'SUPERSEDED', 'DRAFT')", name="valid_lifecycle_state"),
        CheckConstraint("index_flag IN ('INDEX', 'ARCHIVE')", name="valid_index_flag"),
        CheckConstraint(AUDIENCE_CHECK.format(col="document_audience"), name="valid_document_audience"),
        CheckConstraint(AUDIENCE_CHECK.format(col="file_serving_audience"), name="valid_file_serving_audience"),
        CheckConstraint(GROUPS_CHECK.format(col="document_allowed_groups"), name="valid_document_allowed_groups"),
        CheckConstraint(GROUPS_CHECK.format(col="file_serving_allowed_groups"), name="valid_file_serving_allowed_groups"),
        CheckConstraint("access_policy_version ~ '^v[0-9]+\\.[0-9]+$'", name="valid_access_policy_version"),
        CheckConstraint("source_docx_sha256 ~ '^[0-9a-f]{64}$'", name="valid_source_docx_sha256"),
        CheckConstraint("pdf_sha256 ~ '^[0-9a-f]{64}$'", name="valid_pdf_sha256"),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    document_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    policy_id: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[str] = mapped_column(String(20), nullable=False)
    lifecycle_state: Mapped[str] = mapped_column(String(20), nullable=False)
    demonstration_label: Mapped[str] = mapped_column(String(200), nullable=False)
    index_flag: Mapped[str] = mapped_column(String(20), nullable=False)
    document_audience: Mapped[str] = mapped_column(String(50), nullable=False)
    file_serving_audience: Mapped[str] = mapped_column(String(50), nullable=False)
    document_allowed_groups: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    file_serving_allowed_groups: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    access_policy_version: Mapped[str] = mapped_column(String(20), nullable=False)
    source_docx_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    source_docx_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    pdf_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    pdf_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    total_pages: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_employee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id"), nullable=True)
    provenance: Mapped[str] = mapped_column(Text, nullable=False)

    owner: Mapped["Employee | None"] = relationship()
    sections: Mapped[list["DocumentSection"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
    )
    chunks: Mapped[list["DocumentChunk"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
    )
