"""empty message

Revision ID: 1823c0001e87
Revises: b0467ef780c8
Create Date: 2018-04-05 21:15:12.940943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1823c0001e87'
down_revision = 'b0467ef780c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('category', sa.String(length=36), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'category')
    # ### end Alembic commands ###
