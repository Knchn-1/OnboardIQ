"""0002 knowledge

Revision ID: 33f8f980ea16
Revises: fb3fafa82644
Create Date: 2026-11-20 17:15:22.200099

"""
from typing import Sequence, Union

from alembic import op
import pgvector.sqlalchemy.vector
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '33f8f980ea16'
down_revision: Union[str, Sequence[str], None] = 'fb3fafa82644'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # Additional indexes on organization tables
    op.create_index(op.f('ix_employees_manager_id'), 'employees', ['manager_id'], unique=False)
    op.create_index(op.f('ix_employees_department_id'), 'employees', ['department_id'], unique=False)
    op.create_index(op.f('ix_role_assignments_employee_id'), 'role_assignments', ['employee_id'], unique=False)

    op.create_table('documents',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('document_code', sa.String(length=50), nullable=False),
    sa.Column('policy_id', sa.String(length=50), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('version', sa.String(length=20), nullable=False),
    sa.Column('lifecycle_state', sa.String(length=20), nullable=False),
    sa.Column('demonstration_label', sa.String(length=200), nullable=False),
    sa.Column('index_flag', sa.String(length=20), nullable=False),
    sa.Column('document_audience', sa.String(length=50), nullable=False),
    sa.Column('file_serving_audience', sa.String(length=50), nullable=False),
    sa.Column('document_allowed_groups', postgresql.ARRAY(sa.Text()), nullable=False),
    sa.Column('file_serving_allowed_groups', postgresql.ARRAY(sa.Text()), nullable=False),
    sa.Column('access_policy_version', sa.String(length=20), nullable=False),
    sa.Column('source_docx_filename', sa.String(length=255), nullable=False),
    sa.Column('source_docx_sha256', sa.String(length=64), nullable=False),
    sa.Column('pdf_filename', sa.String(length=255), nullable=False),
    sa.Column('pdf_sha256', sa.String(length=64), nullable=False),
    sa.Column('total_pages', sa.Integer(), nullable=False),
    sa.Column('owner_employee_id', sa.Integer(), nullable=True),
    sa.Column('provenance', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("access_policy_version ~ '^v[0-9]+\\.[0-9]+$'", name=op.f('ck_documents_valid_access_policy_version')),
    sa.CheckConstraint("cardinality(document_allowed_groups) >= 1 AND document_allowed_groups <@ ARRAY['GRP_ALL_EMPLOYEES','GRP_MANAGERS','GRP_DEPT_HR','GRP_DEPT_IT','GRP_DEPT_ENG','GRP_DEPT_DA','GRP_DEPT_FIN','GRP_DEPT_SCS']::text[]", name=op.f('ck_documents_valid_document_allowed_groups')),
    sa.CheckConstraint("cardinality(file_serving_allowed_groups) >= 1 AND file_serving_allowed_groups <@ ARRAY['GRP_ALL_EMPLOYEES','GRP_MANAGERS','GRP_DEPT_HR','GRP_DEPT_IT','GRP_DEPT_ENG','GRP_DEPT_DA','GRP_DEPT_FIN','GRP_DEPT_SCS']::text[]", name=op.f('ck_documents_valid_file_serving_allowed_groups')),
    sa.CheckConstraint("document_audience IN ('ALL_EMPLOYEES', 'MANAGERS', 'MANAGERS_AND_HR', 'HR_ONLY', 'IT_ONLY', 'FINANCE_ONLY', 'ENGINEERING_ONLY', 'DA_ONLY', 'SALES_ONLY')", name=op.f('ck_documents_valid_document_audience')),
    sa.CheckConstraint("file_serving_audience IN ('ALL_EMPLOYEES', 'MANAGERS', 'MANAGERS_AND_HR', 'HR_ONLY', 'IT_ONLY', 'FINANCE_ONLY', 'ENGINEERING_ONLY', 'DA_ONLY', 'SALES_ONLY')", name=op.f('ck_documents_valid_file_serving_audience')),
    sa.CheckConstraint("index_flag IN ('INDEX', 'ARCHIVE')", name=op.f('ck_documents_valid_index_flag')),
    sa.CheckConstraint("lifecycle_state IN ('CURRENT', 'SUPERSEDED', 'DRAFT')", name=op.f('ck_documents_valid_lifecycle_state')),
    sa.CheckConstraint("pdf_sha256 ~ '^[0-9a-f]{64}$'", name=op.f('ck_documents_valid_pdf_sha256')),
    sa.CheckConstraint("source_docx_sha256 ~ '^[0-9a-f]{64}$'", name=op.f('ck_documents_valid_source_docx_sha256')),
    sa.ForeignKeyConstraint(['owner_employee_id'], ['employees.id'], name=op.f('fk_documents_owner_employee_id_employees')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_documents')),
    sa.UniqueConstraint('document_code', name=op.f('uq_documents_document_code'))
    )
    op.create_table('document_sections',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('section_code', sa.String(length=50), nullable=False),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('section_number', sa.String(length=20), nullable=False),
    sa.Column('section_title', sa.String(length=200), nullable=False),
    sa.Column('heading_path', sa.Text(), nullable=False),
    sa.Column('page_start', sa.Integer(), nullable=False),
    sa.Column('page_end', sa.Integer(), nullable=False),
    sa.Column('classification_audience', sa.String(length=50), nullable=False),
    sa.Column('allowed_groups', postgresql.ARRAY(sa.Text()), nullable=False),
    sa.Column('restricted_unit_id', sa.String(length=20), nullable=True),
    sa.Column('index_flag', sa.String(length=20), nullable=False),
    sa.Column('lifecycle_state', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("cardinality(allowed_groups) >= 1 AND allowed_groups <@ ARRAY['GRP_ALL_EMPLOYEES','GRP_MANAGERS','GRP_DEPT_HR','GRP_DEPT_IT','GRP_DEPT_ENG','GRP_DEPT_DA','GRP_DEPT_FIN','GRP_DEPT_SCS']::text[]", name=op.f('ck_document_sections_valid_allowed_groups')),
    sa.CheckConstraint("classification_audience IN ('ALL_EMPLOYEES', 'MANAGERS', 'MANAGERS_AND_HR', 'HR_ONLY', 'IT_ONLY', 'FINANCE_ONLY', 'ENGINEERING_ONLY', 'DA_ONLY', 'SALES_ONLY')", name=op.f('ck_document_sections_valid_classification_audience')),
    sa.CheckConstraint("index_flag IN ('INDEX', 'ARCHIVE')", name=op.f('ck_document_sections_valid_index_flag')),
    sa.CheckConstraint("lifecycle_state IN ('CURRENT', 'SUPERSEDED', 'DRAFT')", name=op.f('ck_document_sections_valid_lifecycle_state')),
    sa.CheckConstraint("restricted_unit_id IS NULL OR restricted_unit_id IN ('RU-001', 'RU-002', 'RU-003')", name=op.f('ck_document_sections_valid_restricted_unit_id')),
    sa.ForeignKeyConstraint(['document_id'], ['documents.id'], name=op.f('fk_document_sections_document_id_documents'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_document_sections')),
    sa.UniqueConstraint('section_code', name=op.f('uq_document_sections_section_code'))
    )
    op.create_table('document_chunks',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('chunk_code', sa.String(length=50), nullable=False),
    sa.Column('global_chunk_id', sa.Text(), nullable=True),
    sa.Column('document_id', sa.Integer(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.Column('heading_path', sa.Text(), nullable=False),
    sa.Column('page_number', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('word_count', sa.Integer(), nullable=False),
    sa.Column('classification_audience', sa.String(length=50), nullable=False),
    sa.Column('allowed_groups', postgresql.ARRAY(sa.Text()), nullable=False),
    sa.Column('restricted_unit_id', sa.String(length=20), nullable=True),
    sa.Column('access_policy_version', sa.String(length=20), nullable=False),
    sa.Column('lifecycle_state', sa.String(length=20), nullable=False),
    sa.Column('index_flag', sa.String(length=20), nullable=False),
    sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=384), nullable=True),
    sa.Column('embedding_model', sa.Text(), nullable=True),
    sa.Column('content_tsv', postgresql.TSVECTOR(), sa.Computed("to_tsvector('english', coalesce(heading_path, '') || ' ' || content)", persisted=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("access_policy_version ~ '^v[0-9]+\\.[0-9]+$'", name=op.f('ck_document_chunks_valid_access_policy_version')),
    sa.CheckConstraint("cardinality(allowed_groups) >= 1 AND allowed_groups <@ ARRAY['GRP_ALL_EMPLOYEES','GRP_MANAGERS','GRP_DEPT_HR','GRP_DEPT_IT','GRP_DEPT_ENG','GRP_DEPT_DA','GRP_DEPT_FIN','GRP_DEPT_SCS']::text[]", name=op.f('ck_document_chunks_valid_allowed_groups')),
    sa.CheckConstraint("classification_audience IN ('ALL_EMPLOYEES', 'MANAGERS', 'MANAGERS_AND_HR', 'HR_ONLY', 'IT_ONLY', 'FINANCE_ONLY', 'ENGINEERING_ONLY', 'DA_ONLY', 'SALES_ONLY')", name=op.f('ck_document_chunks_valid_classification_audience')),
    sa.CheckConstraint("index_flag IN ('INDEX', 'ARCHIVE')", name=op.f('ck_document_chunks_valid_index_flag')),
    sa.CheckConstraint("lifecycle_state IN ('CURRENT', 'SUPERSEDED', 'DRAFT')", name=op.f('ck_document_chunks_valid_lifecycle_state')),
    sa.CheckConstraint("restricted_unit_id IS NULL OR restricted_unit_id IN ('RU-001', 'RU-002', 'RU-003')", name=op.f('ck_document_chunks_valid_restricted_unit_id')),
    sa.CheckConstraint('length(btrim(content)) > 0', name=op.f('ck_document_chunks_content_not_empty')),
    sa.ForeignKeyConstraint(['document_id'], ['documents.id'], name=op.f('fk_document_chunks_document_id_documents'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['section_id'], ['document_sections.id'], name=op.f('fk_document_chunks_section_id_document_sections'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_document_chunks')),
    sa.UniqueConstraint('chunk_code', name=op.f('uq_document_chunks_chunk_code')),
    sa.UniqueConstraint('global_chunk_id', name=op.f('uq_document_chunks_global_chunk_id'))
    )

    # Indexes on document_chunks
    op.create_index('ix_document_chunks_allowed_groups', 'document_chunks', ['allowed_groups'], postgresql_using='gin')
    op.create_index('ix_document_chunks_content_tsv', 'document_chunks', ['content_tsv'], postgresql_using='gin')
    op.create_index(op.f('ix_document_chunks_document_id'), 'document_chunks', ['document_id'], unique=False)
    op.create_index(op.f('ix_document_chunks_section_id'), 'document_chunks', ['section_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_document_chunks_section_id'), table_name='document_chunks')
    op.drop_index(op.f('ix_document_chunks_document_id'), table_name='document_chunks')
    op.drop_index('ix_document_chunks_content_tsv', table_name='document_chunks', postgresql_using='gin')
    op.drop_index('ix_document_chunks_allowed_groups', table_name='document_chunks', postgresql_using='gin')

    op.drop_table('document_chunks')
    op.drop_table('document_sections')
    op.drop_table('documents')

    op.drop_index(op.f('ix_role_assignments_employee_id'), table_name='role_assignments')
    op.drop_index(op.f('ix_employees_department_id'), table_name='employees')
    op.drop_index(op.f('ix_employees_manager_id'), table_name='employees')
