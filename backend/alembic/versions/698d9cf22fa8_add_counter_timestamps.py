"""add counter timestamps

Revision ID: 698d9cf22fa8
Revises: 0a112d2993d0
Create Date: 2026-07-21 17:34:37.076215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '698d9cf22fa8'
down_revision: Union[str, None] = '0a112d2993d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('counters', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('counters', sa.Column('updated_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('counters', 'updated_at')
    op.drop_column('counters', 'created_at')
