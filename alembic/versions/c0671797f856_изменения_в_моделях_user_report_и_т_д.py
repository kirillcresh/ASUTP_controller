"""Изменения в моделях User, Report, и т.д.

Revision ID: c0671797f856
Revises: 5c434c15b49a
Create Date: 2024-06-17 03:12:16.619760

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c0671797f856"
down_revision: Union[str, None] = "5c434c15b49a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user",
        "is_admin",
        existing_type=sa.BOOLEAN(),
        nullable=True,
        existing_comment="Администратор",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user",
        "is_admin",
        existing_type=sa.BOOLEAN(),
        nullable=False,
        existing_comment="Администратор",
    )
    # ### end Alembic commands ###
