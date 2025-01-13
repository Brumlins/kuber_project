"""v2
Revision ID: 20241210_v2
Revises: 20241210_ddd
Create Date: 2024-12-10 13:46:27.309103+00:00
"""
from alembic import op
import sqlalchemy as sa
# revision identifiers, used by Alembic.
revision = '20241210_v2'
down_revision = '20241210_ddd'
branch_labels = None
depends_on = None
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('uzivatele',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surename', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###
def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('uzivatele')
    # ### end Alembic commands ###