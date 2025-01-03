"""block_tables added

Revision ID: 5c6e6d9e8ff8
Revises: 9d63b7f4ffe8
Create Date: 2024-12-04 17:23:47.635926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c6e6d9e8ff8'
down_revision = '9d63b7f4ffe8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('block_territory',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('district_id', sa.Integer(), nullable=False),
    sa.Column('block_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['block_id'], ['blocks.id'], ),
    sa.ForeignKeyConstraint(['district_id'], ['districts.id'], ),
    sa.ForeignKeyConstraint(['state_id'], ['states.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('block_crops',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('crop_id', sa.Integer(), nullable=False),
    sa.Column('area', sa.Float(), nullable=False),
    sa.Column('b_territory_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['b_territory_id'], ['block_territory.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['crop_id'], ['crops.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('block_groundwater',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('extraction', sa.Float(), nullable=False),
    sa.Column('b_territory_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['b_territory_id'], ['block_territory.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('block_industries',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('industry_id', sa.Integer(), nullable=False),
    sa.Column('unit', sa.String(length=20), nullable=False),
    sa.Column('allocation', sa.Float(), nullable=False),
    sa.Column('b_territory_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['b_territory_id'], ['block_territory.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['industry_id'], ['industries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('block_livestocks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('livestock_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('b_territory_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['b_territory_id'], ['block_territory.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['livestock_id'], ['livestocks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('block_lulc',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lulc_id', sa.Integer(), nullable=False),
    sa.Column('area', sa.Float(), nullable=False),
    sa.Column('b_territory_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['b_territory_id'], ['block_territory.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['lulc_id'], ['lulc.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('block_populations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('population_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('b_territory_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['b_territory_id'], ['block_territory.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['population_id'], ['populations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('block_rainfall',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('normal', sa.Float(), nullable=False),
    sa.Column('actual', sa.Float(), nullable=False),
    sa.Column('month_year', sa.String(length=20), nullable=False),
    sa.Column('b_territory_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['b_territory_id'], ['block_territory.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('block_waterbodies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('wb_type_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('area', sa.Float(), nullable=False),
    sa.Column('storage', sa.Float(), nullable=False),
    sa.Column('b_territory_id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['b_territory_id'], ['block_territory.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['wb_type_id'], ['waterbody_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('populations', schema=None) as batch_op:
        batch_op.drop_column('remarks')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('populations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('remarks', sa.VARCHAR(), autoincrement=False, nullable=True))

    op.drop_table('block_waterbodies')
    op.drop_table('block_rainfall')
    op.drop_table('block_populations')
    op.drop_table('block_lulc')
    op.drop_table('block_livestocks')
    op.drop_table('block_industries')
    op.drop_table('block_groundwater')
    op.drop_table('block_crops')
    op.drop_table('block_territory')
    # ### end Alembic commands ###
