# alembic/versions/xxxx_create_transactions_table.py

"""create transactions table

Revision ID: xxxx
Revises: 
Create Date: yyyy-mm-dd hh:mm:ss

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'xxxx'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'transactions',
        sa.Column('transaction_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('transaction_id')
    )


def downgrade():
    op.drop_table('transactions')
