"""add signature and paymant confirmation fields

Revision ID: 17343990ccc0
Revises: None
Create Date: 2013-12-11 14:01:32.099898

"""

# revision identifiers, used by Alembic.
revision = '17343990ccc0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('members', sa.Column('payment_confirmed', sa.Boolean(), nullable=True))
    op.add_column('members', sa.Column('payment_confirmed_date', sa.DateTime(), nullable=True))
    op.add_column('members', sa.Column('signature_confirmed', sa.Boolean(), nullable=True))
    op.add_column('members', sa.Column('signature_confirmed_date', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('members') as batch_op:
        batch_op.drop_column('signature_confirmed_date')
        batch_op.drop_column('signature_confirmed')
        batch_op.drop_column('payment_confirmed_date')
        batch_op.drop_column('payment_confirmed')
