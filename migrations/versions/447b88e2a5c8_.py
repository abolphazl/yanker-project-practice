"""empty message

Revision ID: 447b88e2a5c8
Revises: 0e7171e99117
Create Date: 2023-02-14 19:28:26.003201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '447b88e2a5c8'
down_revision = '0e7171e99117'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('episode', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('episode', schema=None) as batch_op:
        batch_op.drop_column('file_id')

    # ### end Alembic commands ###