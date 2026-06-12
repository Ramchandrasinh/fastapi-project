"""create votes votes table

Revision ID: 32af5ae3cfe2
Revises: f85c1da7bf3f
Create Date: 2026-06-11 22:00:06.803293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32af5ae3cfe2'
down_revision: Union[str, Sequence[str], None] = 'f85c1da7bf3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('votes',
                sa.Column('user_id', sa.Integer(), nullable=False),
                sa.Column('post_id', sa.Integer(), nullable=False),
                sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                sa.PrimaryKeyConstraint('user_id', 'post_id'))
    pass


def downgrade() -> None:
    op.drop_table("votes")
    pass
