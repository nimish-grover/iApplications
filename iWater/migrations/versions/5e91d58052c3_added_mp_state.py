"""added mp state

Revision ID: 5e91d58052c3
Revises: c6c9eeb0fb86
Create Date: 2024-07-13 01:01:44.190268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e91d58052c3'
down_revision = 'c6c9eeb0fb86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('water_bodies_mp',
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
    op.drop_table('water_bodies_ap')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('water_bodies_ap',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('district_code', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('village_code', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('wb_type_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('water_spread_area', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('max_depth', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('storage_capacity', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('longitude', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('latitude', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='water_bodies_ap_pkey')
    )
    op.drop_table('water_bodies_mp')
    # ### end Alembic commands ###