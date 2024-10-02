"""empty message

Revision ID: c10e33efbdd2
Revises: b85aa3ef7d56
Create Date: 2024-09-21 08:48:28.038667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c10e33efbdd2'
down_revision = 'b85aa3ef7d56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_key')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_key',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('key', sa.VARCHAR(length=64), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    # ### end Alembic commands ###
