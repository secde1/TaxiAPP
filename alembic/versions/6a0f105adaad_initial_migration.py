"""initial migration

Revision ID: 6a0f105adaad
Revises: 3ccd73620946
Create Date: 2024-10-11 14:31:49.454340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a0f105adaad'
down_revision: Union[str, None] = '3ccd73620946'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=False))
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('users', 'last_name')
    # ### end Alembic commands ###
