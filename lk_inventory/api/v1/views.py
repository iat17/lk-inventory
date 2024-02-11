from typing import Optional

from fastapi import Depends
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from lk_inventory.api.v1.controllers import create_user, create_account, \
    get_accounts, get_account, get_services, link_service_to_account
from lk_inventory.api.v1.dependencies import auth
from lk_inventory.app.api_slash_router import APISlashRouter
from lk_inventory.app.db import get_session
from lk_inventory.serializers.v1.request import UserRegistrationRequest, LinkServiceAccount
from lk_inventory.serializers.v1.response import User, Account, PagingAccount, PagingService

base_routes = APISlashRouter()


@base_routes.post('/users', status_code=HTTP_201_CREATED, response_model=User)
async def create_user_view(user: UserRegistrationRequest, session: AsyncSession = Depends(get_session)):
    return await create_user(user, session)


@base_routes.post('/users/{user_id}/accounts', status_code=HTTP_201_CREATED,
                  description='Создание аккаунта', response_model=Account)
async def create_account_view(user_id: int, session: AsyncSession = Depends(get_session),
                              authorization: bool = Depends(auth)):
    return await create_account(user_id, session=session)


@base_routes.get('/accounts', response_model=PagingAccount)
async def get_accounts_view(limit: int = 10, offset: int = 0, authorization: bool = Depends(auth),
                            session: AsyncSession = Depends(get_session)):
    return await get_accounts(limit, offset, session)


@base_routes.get('/accounts/{account_id}', response_model=Account, response_model_exclude={'services'})
async def get_account_view(account_id: int, session: AsyncSession = Depends(get_session),
                           authorization: bool = Depends(auth)):
    return await get_account(account_id, session)


@base_routes.get('/accounts/{account_id}/services', response_model=PagingService)
async def get_services_by_account_view(account_id: int = Field(gt=0),
                                       limit: Optional[int] = 10,
                                       offset: Optional[int] = 0,
                                       filter_service: Optional[str] = None,
                                       sort_order: Optional[str] = None,
                                       session: AsyncSession = Depends(get_session),
                                       authorization: bool = Depends(auth)):
    return await get_services(account_id, limit, offset, filter_service, sort_order, session)


@base_routes.post('/accounts/{account_id}/service/{service_id}')
async def link_service_to_account_view(link: LinkServiceAccount,
                                       account_id: int = Field(gt=0),
                                       service_id: int = Field(gt=0),
                                       session: AsyncSession = Depends(get_session),
                                       authorization: bool = Depends(auth)):
    return await link_service_to_account(link, account_id, service_id, session)
