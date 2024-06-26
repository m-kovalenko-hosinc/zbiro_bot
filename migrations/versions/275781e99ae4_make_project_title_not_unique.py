"""make project title not unique

Revision ID: 275781e99ae4
Revises: 4939904be8c4
Create Date: 2024-03-28 20:02:41.062720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '275781e99ae4'
down_revision: Union[str, None] = '4939904be8c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('projects_title_key', 'projects', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('projects_title_key', 'projects', ['title'])
    # ### end Alembic commands ###
