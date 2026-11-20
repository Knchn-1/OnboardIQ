"""0001 organization

Revision ID: fb3fafa82644
Revises: 
Create Date: 2026-11-20 17:02:22.262280

"""
from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb3fafa82644'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('departments',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('responsibilities', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("code IN ('HR', 'IT', 'ENG', 'DA', 'FIN', 'SCS')", name=op.f('ck_departments_valid_code')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_departments')),
    sa.UniqueConstraint('code', name=op.f('uq_departments_code')),
    sa.UniqueConstraint('name', name=op.f('uq_departments_name'))
    )
    op.create_table('offices',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=False),
    sa.Column('office_type', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_offices')),
    sa.UniqueConstraint('name', name=op.f('uq_offices_name'))
    )
    op.create_table('employees',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('employee_code', sa.String(length=20), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('job_title', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('office_id', sa.Integer(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.Column('directory_department', sa.Text(), nullable=False),
    sa.Column('reports_to_title', sa.Text(), nullable=True),
    sa.Column('manager_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('provenance', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("employee_code ~ '^EMP-[0-9]{3}$'", name=op.f('ck_employees_valid_employee_code')),
    sa.CheckConstraint('manager_id IS NULL OR manager_id <> id', name=op.f('ck_employees_manager_not_self')),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], name=op.f('fk_employees_department_id_departments')),
    sa.ForeignKeyConstraint(['manager_id'], ['employees.id'], name=op.f('fk_employees_manager_id_employees'), ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['office_id'], ['offices.id'], name=op.f('fk_employees_office_id_offices')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_employees')),
    sa.UniqueConstraint('email', name=op.f('uq_employees_email')),
    sa.UniqueConstraint('employee_code', name=op.f('uq_employees_employee_code'))
    )
    op.create_table('role_assignments',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('role_title', sa.String(length=150), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.Column('is_department_lead', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('provenance', sa.Text(), nullable=False),
    sa.Column('decision_id', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("((status = 'ASSIGNED') = (employee_id IS NOT NULL))", name=op.f('ck_role_assignments_status_employee_match')),
    sa.CheckConstraint("status IN ('ASSIGNED', 'UNASSIGNED')", name=op.f('ck_role_assignments_valid_status')),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], name=op.f('fk_role_assignments_department_id_departments')),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], name=op.f('fk_role_assignments_employee_id_employees')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_role_assignments')),
    sa.UniqueConstraint('role_title', name=op.f('uq_role_assignments_role_title'))
    )
    op.create_index('uq_role_assignments_department_lead', 'role_assignments', ['department_id'], unique=True, postgresql_where=sa.text('is_department_lead = true'))

    op.execute("""
    CREATE VIEW employee_groups AS
    SELECT e.id AS employee_id, 'GRP_ALL_EMPLOYEES'::text AS group_code
      FROM employees e WHERE e.is_active
    UNION ALL
    SELECT e.id, 'GRP_DEPT_' || d.code
      FROM employees e JOIN departments d ON d.id = e.department_id
      WHERE e.is_active
    UNION ALL
    SELECT DISTINCT m.id, 'GRP_MANAGERS'
      FROM employees m JOIN employees r ON r.manager_id = m.id
      WHERE m.is_active AND r.is_active;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP VIEW IF EXISTS employee_groups;")
    op.drop_index('uq_role_assignments_department_lead', table_name='role_assignments', postgresql_where=sa.text('is_department_lead = true'))
    op.drop_table('role_assignments')
    op.drop_table('employees')
    op.drop_table('offices')
    op.drop_table('departments')
