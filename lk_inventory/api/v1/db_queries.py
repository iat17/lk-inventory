from datetime import datetime
from typing import Optional

import bcrypt
from sqlalchemy import func, desc, asc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Load

from lk_inventory.api.v1.models import User, Account, ServiceAccountLink, Service
from lk_inventory.serializers.v1.request import UserRegistrationRequest


async def get_user_query(login: str, session: AsyncSession):
    user = await session.execute(select(User).where(User.user_id == login))
    return user.scalar()


async def create_user_query(session: AsyncSession, user: UserRegistrationRequest):
    password = bcrypt.hashpw(user.password.encode('utf8'), bcrypt.gensalt())
    user = User(**user.dict())
    user.password = password
    session.add(user)
    return user


async def get_user_by_email(session: AsyncSession, email: str):
    query = await session.execute(select(User).where(User.email == email))
    return query.first()


async def link_account_to_user_query(session: AsyncSession, user_id: int):
    account = Account(user_id=user_id)
    session.add(account)
    await session.flush()
    await session.refresh(account)
    return account


async def get_accounts_query(limit, offset, session: AsyncSession):
    query = select(Account, func.count(Account.id).over().label("totalCount")).order_by(Account.created_at.desc())
    query = await session.execute(query.limit(limit).offset(offset))
    objects = query.unique().all()
    return [row[0] for row in objects], objects[0][1]


async def get_account_query(account_id: int, session: AsyncSession):
    query = select(Account).where(Account.id == account_id).options(
        Load(Account).load_only(Account.id, Account.created_at, Account.balance, Account.user_id))
    account = await session.execute(query)
    return account.scalar()


async def get_services_by_account_query(account_id: int, limit: int,
                                        offset: int, filter_by_service: Optional[str],
                                        sort_order: Optional[str], session: AsyncSession):
    query = select(
        ServiceAccountLink, func.count(ServiceAccountLink.id).over().label("totalCount")).where(
        ServiceAccountLink.account_id == account_id)
    if filter_by_service or sort_order:
        query = query.join(Service)
        query = query.join(Service).where(Service.name.ilike(filter_by_service))
    if sort_order:
        sort = asc if sort_order == 'asc' else desc
        query = query.order_by(sort(Service.name))
    service_account = await session.execute(query.limit(limit).offset(offset))
    services = service_account.unique().all()
    return [row[0] for row in services], services[0][1] if services else 0


async def link_service_to_account_query(account_id: int, service_id: int, plan_id: int, session: AsyncSession):
    query = insert(ServiceAccountLink).values(
        account_id=account_id, service_id=service_id, plan_id=plan_id).on_conflict_do_update(
        constraint='_service_uc', set_=dict(account_id=account_id,
                                            service_id=service_id,
                                            plan_id=plan_id,
                                            updated_at=datetime.utcnow()))
    return await session.execute(query)
