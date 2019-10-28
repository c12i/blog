"""Remove unique constrain from Subscribers model

Revision ID: a23bb387d443
Revises: 5adddf56cabc
Create Date: 2019-10-28 10:59:36.748401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a23bb387d443'
down_revision = '5adddf56cabc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_subscribers_email', table_name='subscribers')
    op.create_index(op.f('ix_subscribers_email'), 'subscribers', ['email'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_subscribers_email'), table_name='subscribers')
    op.create_index('ix_subscribers_email', 'subscribers', ['email'], unique=True)
    # ### end Alembic commands ###