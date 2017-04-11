"""init113

Revision ID: 7edd67c0e64a
Revises: 44f59d42d681
Create Date: 2017-04-08 14:42:41.413727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7edd67c0e64a'
down_revision = '44f59d42d681'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('name', table_name='tags')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('name', 'tags', ['name'], unique=True)
    # ### end Alembic commands ###
