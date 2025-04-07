"""empty message

Revision ID: 63ae3b159cc1
Revises: 0c24541dd085
Create Date: 2025-04-08 01:02:10.269357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63ae3b159cc1'
down_revision: Union[str, None] = '0c24541dd085'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('secret_logs_secret_id_fkey', 'secret_logs', type_='foreignkey')
    op.create_foreign_key(None, 'secret_logs', 'secrets', ['secret_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'secret_logs', type_='foreignkey')
    op.create_foreign_key('secret_logs_secret_id_fkey', 'secret_logs', 'secrets', ['secret_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
