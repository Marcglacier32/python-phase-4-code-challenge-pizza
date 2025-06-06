"""Add relationships, proxies, validations

Revision ID: 20bc556fd504
Revises: 75d43fd077b4
Create Date: 2025-06-06 12:50:07.062105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20bc556fd504'
down_revision = '75d43fd077b4'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('restaurant_pizzas') as batch_op:
        batch_op.alter_column('restaurant_id', nullable=False)
        batch_op.alter_column('pizza_id', nullable=False)

def downgrade():
    with op.batch_alter_table('restaurant_pizzas') as batch_op:
        batch_op.alter_column('pizza_id', nullable=True)
        batch_op.alter_column('restaurant_id', nullable=True)