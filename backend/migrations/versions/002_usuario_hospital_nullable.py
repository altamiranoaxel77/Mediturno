"""usuario id_hospital nullable con constraint superadmin

Revision ID: 002_usuario_hospital_nullable
Revises: 21260cc607ff
Create Date: 2025-08-01
"""
from alembic import op
import sqlalchemy as sa

revision = '002_usuario_hospital_nullable'
down_revision = '21260cc607ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Paso 1: hace id_hospital nullable para que el SuperAdmin
            pueda existir sin estar asociado a ningún hospital.

    Paso 2: agrega CHECK CONSTRAINT que garantiza que SOLO
            el rol 1 (SuperAdmin) tenga id_hospital en NULL.
            Todos los demás roles DEBEN tener hospital.
    """
    op.alter_column(
        'usuario',
        'id_hospital',
        existing_type=sa.Integer(),
        nullable=True
    )

    op.create_check_constraint(
        constraint_name='chk_hospital_superadmin',
        table_name='usuario',
        condition='(id_rol = 1) OR (id_hospital IS NOT NULL)'
    )


def downgrade() -> None:
    """Revierte los cambios. Ejecutar con: alembic downgrade -1"""
    op.drop_constraint(
        constraint_name='chk_hospital_superadmin',
        table_name='usuario',
        type_='check'
    )
    op.alter_column(
        'usuario',
        'id_hospital',
        existing_type=sa.Integer(),
        nullable=False
    )