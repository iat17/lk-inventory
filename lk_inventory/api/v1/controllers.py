from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from lk_inventory.api.v1.db_queries import get_accounts_query, get_services_by_account_query, get_user_by_email, \
    create_user_query, link_account_to_user_query, get_account_query, link_service_to_account_query
from lk_inventory.api.v1.models import Account
from lk_inventory.serializers.v1.request import UserRegistrationRequest, LinkServiceAccount


def get_paging_objects(objects: list, count: int, limit: int, offset: int):
    result = dict(totalCount=count, limit=limit, offset=offset, entries=objects)
    return result


def get_first_services(accounts: List[Account]):
    for account in accounts:
        account.services = account.services[:3]
    return accounts


async def get_paging_accounts(limit: int, offset: int, session: AsyncSession):
    accounts, count = await get_accounts_query(limit, offset, session)
    accounts = get_first_services(accounts)
    return get_paging_objects(accounts, count, limit, offset)


async def get_paging_services(account_id: int, limit: int,
                              offset: int, filter_service: Optional[str],
                              sort_order: Optional[str], session: AsyncSession):
    services, count = await get_services_by_account_query(account_id, limit,
                                                          offset, filter_service,
                                                          sort_order, session)
    return get_paging_objects(services, count, limit, offset)


async def create_user(user: UserRegistrationRequest, session: AsyncSession):
    async with session.begin():
        db_user = await get_user_by_email(session, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return await create_user_query(session, user=user)


async def create_account(id_: int, session: AsyncSession):
    async with session.begin():
        return await link_account_to_user_query(session, id_)


async def get_accounts(limit: int, offset: int, session: AsyncSession):
    return await get_paging_accounts(limit, offset, session)


async def get_account(account_id: int, session: AsyncSession):
    return await get_account_query(account_id, session)


async def get_services(account_id: int, limit: int,
                       offset: int, filter_service: Optional[str],
                       sort_order: Optional[str], session: AsyncSession):
    return await get_paging_services(account_id, limit,
                                     offset, filter_service,
                                     sort_order, session)


async def link_service_to_account(link: LinkServiceAccount,
                                  account_id: int,
                                  service_id: int,
                                  session: AsyncSession):
    async with session.begin():
        await link_service_to_account_query(account_id, service_id, link.plan_id, session)
    return {'status': 'success'}
