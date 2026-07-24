"""add counter locks table

Revision ID: 7f3e9a2b4c1d
Revises: 698d9cf22fa8
Create Date: 2026-07-24 08:18:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f3e9a2b4c1d'
down_revision: Union[str, None] = '698d9cf22fa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'counter_locks',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('locked_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('counter_locks')
