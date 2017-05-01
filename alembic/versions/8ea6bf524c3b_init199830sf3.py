"""init199830sf3

Revision ID: 8ea6bf524c3b
Revises: 1a09d08b2ade
Create Date: 2017-05-01 23:21:22.836419

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8ea6bf524c3b'
down_revision = '1a09d08b2ade'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rotates', sa.Column('description', sa.String(length=200), nullable=True))
    op.drop_column('rotates', 'desc')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rotates', sa.Column('desc', mysql.VARCHAR(length=200), nullable=True))
    op.drop_column('rotates', 'description')
    # ### end Alembic commands ###
