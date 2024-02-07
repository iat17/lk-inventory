from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    user_id: str = Field(description='Логин пользователя')
    phone: str = Field(description='Телефон')
    email: EmailStr = Field(description='Email')
    name: str = Field(description='Имя пользователя')
    last_name: str = Field(description='Фамилия пользователя')
