from typing import TYPE_CHECKING
from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    CheckConstraint,
    Computed,
    ForeignKey,
    Identity,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from app.db.base import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.document_section import DocumentSection

GROUPS_CHECK = (
    "cardinality(allowed_groups) >= 1 AND allowed_groups <@ ARRAY["
    "'GRP_ALL_EMPLOYEES','GRP_MANAGERS','GRP_DEPT_HR','GRP_DEPT_IT',"
    "'GRP_DEPT_ENG','GRP_DEPT_DA','GRP_DEPT_FIN','GRP_DEPT_SCS']::text[]"
)

AUDIENCE_CHECK = (
    "classification_audience IN ('ALL_EMPLOYEES', 'MANAGERS', 'MANAGERS_AND_HR', 'HR_ONLY', 'IT_ONLY', "
    "'FINANCE_ONLY', 'ENGINEERING_ONLY', 'DA_ONLY', 'SALES_ONLY')"
)

class DocumentChunk(Base, TimestampMixin):
    __tablename__ = "document_chunks"
    __table_args__ = (
        CheckConstraint("lifecycle_state IN ('CURRENT', 'SUPERSEDED', 'DRAFT')", name="valid_lifecycle_state"),
        CheckConstraint("index_flag IN ('INDEX', 'ARCHIVE')", name="valid_index_flag"),
        CheckConstraint(AUDIENCE_CHECK, name="valid_classification_audience"),
        CheckConstraint(GROUPS_CHECK, name="valid_allowed_groups"),
        CheckConstraint(
            "restricted_unit_id IS NULL OR restricted_unit_id IN ('RU-001', 'RU-002', 'RU-003')",
            name="valid_restricted_unit_id",
        ),
        CheckConstraint("access_policy_version ~ '^v[0-9]+\\.[0-9]+$'", name="valid_access_policy_version"),
        CheckConstraint("length(btrim(content)) > 0", name="content_not_empty"),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    chunk_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    global_chunk_id: Mapped[str | None] = mapped_column(Text, unique=True, nullable=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    section_id: Mapped[int] = mapped_column(
        ForeignKey("document_sections.id", ondelete="CASCADE"),
        nullable=False,
    )
    heading_path: Mapped[str] = mapped_column(Text, nullable=False)
    page_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, nullable=False)
    classification_audience: Mapped[str] = mapped_column(String(50), nullable=False)
    allowed_groups: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    restricted_unit_id: Mapped[str | None] = mapped_column(String(20), nullable=True)
    access_policy_version: Mapped[str] = mapped_column(String(20), nullable=False)
    lifecycle_state: Mapped[str] = mapped_column(String(20), nullable=False)
    index_flag: Mapped[str] = mapped_column(String(20), nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(settings.EMBEDDING_DIM),
        nullable=True,
    )
    embedding_model: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_tsv: Mapped[TSVECTOR | None] = mapped_column(
        TSVECTOR,
        Computed(
            "to_tsvector('english', coalesce(heading_path, '') || ' ' || content)",
            persisted=True,
        ),
        nullable=True,
    )

    document: Mapped["Document"] = relationship(back_populates="chunks")
    section: Mapped["DocumentSection"] = relationship(back_populates="chunks")
