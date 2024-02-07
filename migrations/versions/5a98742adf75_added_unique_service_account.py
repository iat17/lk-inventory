"""added unique service account

Revision ID: 5a98742adf75
Revises: a2694d3c54e3
Create Date: 2023-02-14 09:52:56.194334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a98742adf75'
down_revision = 'a2694d3c54e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_service_uc', 'service_account_link', ['service_id', 'account_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_service_uc', 'service_account_link', type_='unique')
    # ### end Alembic commands ###