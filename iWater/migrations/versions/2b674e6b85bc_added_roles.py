"""added roles

Revision ID: 2b674e6b85bc
Revises: 5e91d58052c3
Create Date: 2024-08-13 14:20:01.386443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b674e6b85bc'
down_revision = '5e91d58052c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('in_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
        batch_op.create_unique_constraint(None, ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)

    op.drop_table('in_role')
    op.drop_table('roles')
    # ### end Alembic commands ###