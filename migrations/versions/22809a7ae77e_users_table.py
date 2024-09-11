"""users table

Revision ID: 22809a7ae77e
Revises: ea503332dd06
Create Date: 2024-09-11 20:31:19.037977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22809a7ae77e'
down_revision = 'ea503332dd06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=256), nullable=True))
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=100), nullable=False))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
