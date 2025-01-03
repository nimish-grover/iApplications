"""add_state_to_users

Revision ID: 740eb282fcaa
Revises: 89c0d451a06e
Create Date: 2024-12-07 14:16:11.726114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '740eb282fcaa'
down_revision = '89c0d451a06e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('state_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'states', ['state_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('state_id')

    # ### end Alembic commands ###
