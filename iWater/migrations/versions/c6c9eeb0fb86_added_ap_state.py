"""added ap state

Revision ID: c6c9eeb0fb86
Revises: d649b04ff22a
Create Date: 2024-07-13 00:21:34.451879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6c9eeb0fb86'
down_revision = 'd649b04ff22a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('water_bodies_ap',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('district_code', sa.Integer(), nullable=True),
    sa.Column('village_code', sa.Integer(), nullable=True),
    sa.Column('wb_type_id', sa.Integer(), nullable=True),
    sa.Column('water_spread_area', sa.Float(), nullable=True),
    sa.Column('max_depth', sa.Float(), nullable=True),
    sa.Column('storage_capacity', sa.Float(), nullable=True),
    sa.Column('longitude', sa.String(length=80), nullable=True),
    sa.Column('latitude', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('water_bodies_ap')
    # ### end Alembic commands ###
