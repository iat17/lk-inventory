"""added services and plans

Revision ID: 90fc82532b44
Revises: 05f7f472b6bd
Create Date: 2023-01-11 00:34:38.226449

"""
import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table

from lk_inventory.api.v1.models import Service

# revision identifiers, used by Alembic.
revision = '90fc82532b44'
down_revision = '7cebe5086edb'
branch_labels = None
depends_on = None

service_table = table('service',
                      sa.column('id'),
                      sa.column('created_at'),
                      sa.column('name'),
                      sa.column('description'))

plan_table = table('plan',
                   sa.column('id'),
                   sa.column('created_at'),
                   sa.column('name'),
                   sa.column('price'),
                   sa.column('service_id'))


def upgrade() -> None:
    op.bulk_insert(service_table, [
        {'id': 1,
         'created_at': datetime.datetime.now(),
         'name': 'iptv',
         'description': 'about iptv'},
        {'id': 2,
         'created_at': datetime.datetime.now(),
         'name': 'internet',
         'description': 'about internet'},
        {'id': 3,
         'created_at': datetime.datetime.now(),
         'name': 'sim',
         'description': 'about sim'},
        {'id': 4,
         'created_at': datetime.datetime.now(),
         'name': 'wink',
         'description': 'about wink'}
    ])

    op.bulk_insert(plan_table,
                   [
                       {
                           'id': 1,
                           'created_at': datetime.datetime.now(),
                           'name': 'iptv_plan_1',
                           'price': 100,
                           'service_id': 1
                       },
                       {
                           'id': 2,
                           'created_at': datetime.datetime.now(),
                           'name': 'iptv_plan_2',
                           'price': 299,
                           'service_id': 1
                       },
                       {
                           'id': 3,
                           'created_at': datetime.datetime.now(),
                           'name': 'internet_plan_1',
                           'price': 250,
                           'service_id': 2
                       },
                       {
                           'id': 4,
                           'created_at': datetime.datetime.now(),
                           'name': 'internet_plan_2',
                           'price': 499,
                           'service_id': 2
                       },
                       {
                           'id': 5,
                           'created_at': datetime.datetime.now(),
                           'name': 'sim_plan_1',
                           'price': 150,
                           'service_id': 3
                       },
                       {
                           'id': 6,
                           'created_at': datetime.datetime.now(),
                           'name': 'sim_plan_2',
                           'price': 299,
                           'service_id': 3
                       },
                       {
                           'id': 7,
                           'created_at': datetime.datetime.now(),
                           'name': 'wink_plan_1',
                           'price': 100,
                           'service_id': 4
                       },
                       {
                           'id': 8,
                           'created_at': datetime.datetime.now(),
                           'name': 'wink_plan_2',
                           'price': 299,
                           'service_id': 4
                       },
                   ])


def downgrade() -> None:
    op.execute('TRUNCATE public.service RESTART IDENTITY CASCADE;')
    op.execute('TRUNCATE public.plan RESTART IDENTITY CASCADE;')
