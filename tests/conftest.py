import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from lk_inventory.api.v1.dependencies import auth
from lk_inventory.api.v1.models import Base, Service, User, Account, Plan, ServiceAccountLink
from lk_inventory.app.db import get_session
from lk_inventory.app.fastapi import create_app
from tests.config import config


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop_policy().new_event_loop()


@pytest.fixture()
def fake_app(db_session):
    def get_db_session():
        yield db_session

    app = create_app()
    app.dependency_overrides[get_session] = get_db_session
    yield app


@pytest_asyncio.fixture()
async def client(fake_app, db_engine):
    async with AsyncClient(app=fake_app, base_url='http://test') as async_client:
        yield async_client


@pytest_asyncio.fixture()
async def db_engine():
    engine = create_async_engine(
        config.TEST_DATABASE_URL
    )

    async with engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db_session(db_engine):
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
def override_auth_check_dependency(fake_app):
    fake_app.dependency_overrides[auth] = override_dependency


async def override_dependency():
    return True


@pytest_asyncio.fixture
async def create_fake_users(db_session):
    users = [User(user_id=f'user_{i}',
                  password=b'123',
                  phone='+71234567890',
                  email=f'test_mail_{i}',
                  name=f'name_{i}',
                  last_name=f'last_name_{i}') for i in range(1, 10)]
    db_session.add_all(users)
    await db_session.commit()


@pytest_asyncio.fixture
async def create_fake_accounts(db_session):
    accounts = [Account(balance=i) for i in range(1, 10)]
    db_session.add_all(accounts)
    await db_session.commit()


@pytest_asyncio.fixture
async def create_fake_services(db_session):
    services = [Service(name=f'test_name_{i}', description=f'test_description_{i}') for i in range(1, 10)]
    db_session.add_all(services)
    await db_session.commit()


@pytest_asyncio.fixture
async def create_fake_plans(db_session, create_fake_services):
    plans = [Plan(name=f'test_name_{i}', price=i, service_id=i) for i in range(1, 10)]
    db_session.add_all(plans)
    await db_session.commit()


@pytest_asyncio.fixture
async def create_fake_service_account_links(db_session,
                                            create_fake_accounts,
                                            create_fake_plans,
                                            create_fake_services):
    links = [ServiceAccountLink(service_id=i,
                                account_id=i,
                                plan_id=i) for i in range(1, 10)]
    db_session.add_all(links)
    await db_session.commit()
