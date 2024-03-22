"""empty message

Revision ID: c5f0d6c97ec7
Revises: 4ee4b528d301
Create Date: 2024-03-21 23:27:33.827533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5f0d6c97ec7'
down_revision = '4ee4b528d301'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    # ### end Alembic commands ###