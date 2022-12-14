"""empty message

Revision ID: 8077ab15085f
Revises: b71589d645dc
Create Date: 2022-12-09 13:23:58.313389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8077ab15085f'
down_revision = 'b71589d645dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=False))
        batch_op.create_unique_constraint('email', ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('email', type_='unique')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
