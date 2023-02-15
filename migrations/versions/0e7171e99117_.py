"""empty message

Revision ID: 0e7171e99117
Revises: 
Create Date: 2023-02-14 19:26:57.510154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e7171e99117'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('series',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('imdb_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('plot', sa.String(), nullable=False),
    sa.Column('rating_count', sa.Integer(), nullable=False),
    sa.Column('rating_star', sa.Float(), nullable=False),
    sa.Column('genres', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('season',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('series_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['series_id'], ['series.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('episode',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('no', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('image_large', sa.String(), nullable=False),
    sa.Column('plot', sa.String(), nullable=False),
    sa.Column('published_date', sa.String(), nullable=False),
    sa.Column('rating_count', sa.Integer(), nullable=False),
    sa.Column('rating_star', sa.Float(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['season.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('episode')
    op.drop_table('season')
    op.drop_table('user')
    op.drop_table('todo')
    op.drop_table('series')
    # ### end Alembic commands ###
