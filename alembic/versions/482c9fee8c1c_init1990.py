"""init1990

Revision ID: 482c9fee8c1c
Revises: d3f0dfa4e25f
Create Date: 2017-04-10 16:04:31.635811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '482c9fee8c1c'
down_revision = 'd3f0dfa4e25f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('useridToArticleid',
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('articleid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['articleid'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('useridToArticleid')
    # ### end Alembic commands ###