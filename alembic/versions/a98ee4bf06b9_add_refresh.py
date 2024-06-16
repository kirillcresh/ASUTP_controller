"""add refresh

Revision ID: a98ee4bf06b9
Revises: d0d594cb14c2
Create Date: 2024-06-16 11:48:02.495355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a98ee4bf06b9'
down_revision: Union[str, None] = 'd0d594cb14c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('refresh_token', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'refresh_token')
    # ### end Alembic commands ###
