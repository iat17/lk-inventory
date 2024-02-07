import os


class BaseConfig:
    APP_NAME: str = "lk_inventory"
    ENVIRONMENT: str = "lk_inventory"

    INIT_LOGGING: bool = True
    LOG_LEVEL = 'INFO'

    DATABASE_URL = os.environ.get(
        'DATABASE_URL',
        'postgresql+asyncpg://postgres:postgres@postgres:5432/postgres')


config = BaseConfig()
