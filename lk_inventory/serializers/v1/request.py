from pydantic import BaseModel, Field

from lk_inventory.serializers.v1.base_serializer import BaseUser


class UserRegistrationRequest(BaseUser):
    password: str = Field(description='Пароль пользователя')


class LinkServiceAccount(BaseModel):
    plan_id: int = Field(description='Идентификатор тарифного плана')
