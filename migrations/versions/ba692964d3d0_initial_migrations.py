"""initial migrations

Revision ID: ba692964d3d0
Revises: 
Create Date: 2024-10-21 22:01:40.310010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba692964d3d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('states',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('census_code', sa.Integer(), nullable=True),
    sa.Column('local_name', sa.String(length=100), nullable=True),
    sa.Column('is_state', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('districts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('census_code', sa.Integer(), nullable=True),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('local_name', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['state_id'], ['states.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('blocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('census_code', sa.Integer(), nullable=True),
    sa.Column('district_id', sa.Integer(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('local_name', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['district_id'], ['districts.id'], ),
    sa.ForeignKeyConstraint(['state_id'], ['states.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rainfall_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('observation_date', sa.DateTime(), nullable=True),
    sa.Column('normal', sa.Float(precision=53), nullable=False),
    sa.Column('actual', sa.Float(precision=53), nullable=False),
    sa.Column('district_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['district_id'], ['districts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('villages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=160), nullable=False),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('census_code', sa.Integer(), nullable=True),
    sa.Column('local_name', sa.String(length=100), nullable=True),
    sa.Column('block_id', sa.Integer(), nullable=False),
    sa.Column('district_id', sa.Integer(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['block_id'], ['blocks.id'], ),
    sa.ForeignKeyConstraint(['district_id'], ['districts.id'], ),
    sa.ForeignKeyConstraint(['state_id'], ['states.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('block_id', 'district_id', 'id')
    )
    op.create_table('census_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tga', sa.String(length=160), nullable=False),
    sa.Column('households', sa.Integer(), nullable=False),
    sa.Column('male_population', sa.Integer(), nullable=True),
    sa.Column('female_population', sa.Integer(), nullable=True),
    sa.Column('sc_male_population', sa.Integer(), nullable=True),
    sa.Column('sc_female_population', sa.Integer(), nullable=True),
    sa.Column('st_male_population', sa.Integer(), nullable=True),
    sa.Column('st_female_population', sa.Integer(), nullable=True),
    sa.Column('forest_area', sa.Integer(), nullable=True),
    sa.Column('non_agriculture_area', sa.Integer(), nullable=True),
    sa.Column('uncultivable_area', sa.Integer(), nullable=True),
    sa.Column('grazing_area', sa.Integer(), nullable=True),
    sa.Column('misc_area', sa.Integer(), nullable=True),
    sa.Column('wasteland_area', sa.Integer(), nullable=True),
    sa.Column('fallow_area', sa.Integer(), nullable=True),
    sa.Column('current_fallow_area', sa.Integer(), nullable=True),
    sa.Column('unirrigated_area', sa.Integer(), nullable=True),
    sa.Column('canal_area', sa.Integer(), nullable=True),
    sa.Column('tubewell_area', sa.Integer(), nullable=True),
    sa.Column('tank_area', sa.Integer(), nullable=True),
    sa.Column('waterfall_area', sa.Integer(), nullable=True),
    sa.Column('other_area', sa.Integer(), nullable=True),
    sa.Column('village_id', sa.Integer(), nullable=False),
    sa.Column('block_id', sa.Integer(), nullable=False),
    sa.Column('district_id', sa.Integer(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('local_name', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['block_id'], ['blocks.id'], ),
    sa.ForeignKeyConstraint(['district_id'], ['districts.id'], ),
    sa.ForeignKeyConstraint(['state_id'], ['states.id'], ),
    sa.ForeignKeyConstraint(['village_id'], ['villages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('census_data')
    op.drop_table('villages')
    op.drop_table('rainfall_data')
    op.drop_table('blocks')
    op.drop_table('districts')
    op.drop_table('states')
    # ### end Alembic commands ###
