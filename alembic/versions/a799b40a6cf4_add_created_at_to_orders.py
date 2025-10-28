"""add created_at to orders

Revision ID: a799b40a6cf4
Revises: 04383bba90c1
Create Date: 2025-10-28 09:29:26.615620
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a799b40a6cf4'
down_revision = '04383bba90c1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'orders',
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_column('orders', 'created_at')
