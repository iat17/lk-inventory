from fastapi import FastAPI

from lk_inventory.api.v1.routes import v1_routes
from lk_inventory.app.config import config
from lk_inventory.app.logging import init_logging
from lk_inventory.app.api_slash_router import APISlashRouter

healthcheck_route = APISlashRouter()


@healthcheck_route.get('/v1/health')
def health_check():
    return {'status': 'ok'}


def create_app():
    if config.INIT_LOGGING:
        init_logging(config.LOG_LEVEL)

    app = FastAPI(title='lk-inventory')
    app.include_router(healthcheck_route)
    app.include_router(v1_routes)
    return app
