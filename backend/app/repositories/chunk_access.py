"""
Chunk authorization predicate.

Uses the employee_groups view to determine which chunks an employee may see,
using the && (array overlap) operator against the chunk's allowed_groups.
Fail-closed: unknown or inactive employees see zero rows.
"""
from sqlalchemy import Column, Integer, MetaData, Table, Text, func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document_chunk import DocumentChunk
from app.models.employee import Employee

_eg_meta = MetaData()
employee_groups = Table(
    "employee_groups",
    _eg_meta,
    Column("employee_id", Integer),
    Column("group_code", Text),
)


def authorized_chunk_filter(employee_code: str):
    """Return a list of WHERE-clause conditions for DocumentChunk queries.

    Usage:
        stmt = select(DocumentChunk).where(*authorized_chunk_filter("EMP-001"))
    """
    user_groups_subq = (
        select(employee_groups.c.group_code)
        .select_from(
            employee_groups.join(
                Employee, Employee.id == employee_groups.c.employee_id
            )
        )
        .where(Employee.employee_code == employee_code)
        .correlate(Employee)
        .scalar_subquery()
    )

    return [
        DocumentChunk.access_policy_version == settings.ACCESS_POLICY_VERSION,
        DocumentChunk.lifecycle_state == "CURRENT",
        DocumentChunk.index_flag == "INDEX",
        DocumentChunk.allowed_groups.op("&&")(func.array(user_groups_subq)),
    ]


def fetch_authorized_chunk_codes(
    session: Session, employee_code: str
) -> set[str]:
    """Return the set of chunk_codes an employee is authorized to see."""
    stmt = select(DocumentChunk.chunk_code).where(
        *authorized_chunk_filter(employee_code)
    )
    return set(session.scalars(stmt).all())
