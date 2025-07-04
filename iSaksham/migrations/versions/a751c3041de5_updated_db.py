"""updated db

Revision ID: a751c3041de5
Revises: 4847cc11bb51
Create Date: 2025-06-17 16:45:32.703333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a751c3041de5'
down_revision = '4847cc11bb51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('chapters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uuid', sa.String(length=36), nullable=True))
        batch_op.create_index(batch_op.f('ix_chapters_uuid'), ['uuid'], unique=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('registered_on', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('uuid', sa.String(length=36), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_uuid'), ['uuid'], unique=True)
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_index(batch_op.f('ix_user_uuid'))
        batch_op.drop_column('uuid')
        batch_op.drop_column('registered_on')
        batch_op.drop_column('is_admin')
        batch_op.drop_column('is_active')

    with op.batch_alter_table('chapters', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_chapters_uuid'))
        batch_op.drop_column('uuid')

    op.drop_table('activity_logs')
    # ### end Alembic commands ###
