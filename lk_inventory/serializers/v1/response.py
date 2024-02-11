from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from lk_inventory.serializers.v1.base_serializer import BaseUser


class User(BaseUser):
    id: int = Field(gt=0, description='Идентификатор пользователя')
    created_at: datetime = Field(description='Дата создания записи в БД')
    updated_at: datetime = Field(description='Дата редактирования')

    class Config:
        orm_mode = True


class Plan(BaseModel):
    id: int = Field(gt=0, description='Идентификатор тарифного плана')
    name: str = Field(description='Название тарифного плана')
    price: str = Field(description='Цена')
    service_id: int = Field(gt=0, description='Идентификатор услуги')

    class Config:
        orm_mode = True


class Service(BaseModel):
    id: int = Field(gt=0, description='Идентификатор услуги')
    name: str = Field(description='Название услуги')
    description: str = Field(description='Описание услуги')
    plans: List[Plan] = Field(description='Тарифные планы по услуге')

    class Config:
        orm_mode = True


class ServiceAccountLink(BaseModel):
    updated_at: datetime = Field(description='Дата редактирования')
    service_id: int = Field(description='Идентификатор услуги')
    plan_id: int = Field(description='Идентификатор тарифного плана')
    service_details: Service = Field(description='Информация о сервисе')

    class Config:
        orm_mode = True


class Account(BaseModel):
    id: int = Field(gt=0, description='Идентификатор аккаунта')
    user_id: Optional[int] = Field(gt=0, description='Идентификатор пользователя')
    balance: int = Field(description='Баланс')
    services: List[ServiceAccountLink] = Field(description='Подключенные услуги')

    class Config:
        orm_mode = True


class Paging(BaseModel):
    limit: int = Field(default=0, description='Выводимое количество записей')
    offset: int = Field(default=0, description='Количество пропускаемых записей')
    totalCount: int = Field(default=0, description='Полное количество всех записей в выборке')


class PagingAccount(Paging):
    entries: List[Account] = Field(default=[], description='Массив объектов аккаунта')


class PagingService(Paging):
    entries: List[ServiceAccountLink] = Field(default=[], description='Массив объектов услуг')
