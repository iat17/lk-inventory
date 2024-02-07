import os

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'postgresql+asyncpg://postgres:postgres@postgres:5432/postgres')
