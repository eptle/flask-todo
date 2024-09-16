"""empty message

Revision ID: 267396c7eb45
Revises: fe6cb08cf873
Create Date: 2024-09-16 01:58:02.545125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '267396c7eb45'
down_revision = 'fe6cb08cf873'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_constraint('user_position_uc', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.create_unique_constraint('user_position_uc', ['board_id', 'position'])

    # ### end Alembic commands ###
