"""added crops

Revision ID: d649b04ff22a
Revises: 5361e1b81d1b
Create Date: 2024-06-09 10:05:48.229079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd649b04ff22a'
down_revision = '5361e1b81d1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crop_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('district_code', sa.Integer(), nullable=False),
    sa.Column('village_code', sa.Integer(), nullable=False),
    sa.Column('crop_id', sa.Integer(), nullable=False),
    sa.Column('crop_type_id', sa.Integer(), nullable=False),
    sa.Column('crop_area', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('crops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('water_required_per_hectare', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('crops_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('villages_mp')
    op.alter_column('water_bodies', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               nullable=False,
               autoincrement=True)
    op.alter_column('water_bodies', 'district_code',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('water_bodies', 'village_code',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('water_bodies', 'wb_type_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('water_bodies', 'max_depth',
               existing_type=sa.BIGINT(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('water_bodies', 'longitude',
               existing_type=sa.TEXT(),
               type_=sa.String(length=80),
               existing_nullable=True)
    op.alter_column('water_bodies', 'latitude',
               existing_type=sa.TEXT(),
               type_=sa.String(length=80),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('water_bodies', 'latitude',
               existing_type=sa.String(length=80),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('water_bodies', 'longitude',
               existing_type=sa.String(length=80),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('water_bodies', 'max_depth',
               existing_type=sa.Float(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('water_bodies', 'wb_type_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('water_bodies', 'village_code',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('water_bodies', 'district_code',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_nullable=True)
    op.alter_column('water_bodies', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               nullable=True,
               autoincrement=True)
    op.create_table('villages_mp',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=160), autoincrement=False, nullable=False),
    sa.Column('code', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('census_code', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('block_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('district_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['block_id'], ['blocks.id'], name='villages_mp_block_id_fkey'),
    sa.ForeignKeyConstraint(['district_id'], ['districts.id'], name='villages_mp_district_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='villages_mp_pkey'),
    sa.UniqueConstraint('block_id', 'district_id', 'code', name='villages_mp_block_id_district_id_code_key')
    )
    op.drop_table('crops_type')
    op.drop_table('crops')
    op.drop_table('crop_area')
    # ### end Alembic commands ###