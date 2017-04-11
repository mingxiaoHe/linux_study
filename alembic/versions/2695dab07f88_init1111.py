"""init1111

Revision ID: 2695dab07f88
Revises: 7edd67c0e64a
Create Date: 2017-04-08 16:43:22.885912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2695dab07f88'
down_revision = '7edd67c0e64a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'tags', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tags', type_='unique')
    # ### end Alembic commands ###