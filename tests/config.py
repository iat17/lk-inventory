import os


class BaseConfig:
    APP_NAME: str = "lk_inventory"
    ENVIRONMENT: str = "lk_inventory"

    INIT_LOGGING: bool = True
    LOG_LEVEL = 'INFO'

    TEST_DATABASE_URL = os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql+asyncpg://postgres:postgres@postgres:5432/postgres')


config = BaseConfig()
