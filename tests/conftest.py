import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from lk_inventory.api.v1.dependencies import auth
from lk_inventory.api.v1.models import Base
from lk_inventory.app.config import config
from lk_inventory.app.fastapi import create_app


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop_policy().new_event_loop()


@pytest.fixture()
def fake_app():
    return create_app()


@pytest_asyncio.fixture()
async def client(fake_app):
    async with AsyncClient(app=fake_app, base_url='http://test') as async_client:
        yield async_client


@pytest_asyncio.fixture()
async def db_engine():
    engine = create_engine(
        config.DATABASE_URL
    )

    async with engine.begin() as session:
        session.run_sync(Base.metadata.drop_all())
        session.run_sync(Base.metadata.create_all())

    yield engine

    async with engine.begin() as session:
        session.run_sync(Base.metadata.drop_all())


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


# @pytest_asyncio.fixture()
# async def create_fake_services():
#
