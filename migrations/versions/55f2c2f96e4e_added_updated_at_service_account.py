"""added updated_at service account

Revision ID: 55f2c2f96e4e
Revises: 5a98742adf75
Create Date: 2023-02-14 11:21:50.952920

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '55f2c2f96e4e'
down_revision = '5a98742adf75'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_account_link', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.alter_column('service_account_link', 'created_at',
                    existing_type=postgresql.TIMESTAMP(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('service_account_link', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_column('service_account_link', 'updated_at')
    # ### end Alembic commands ###
