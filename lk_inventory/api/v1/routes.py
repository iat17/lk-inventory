from lk_inventory.app.api_slash_router import APISlashRouter
from lk_inventory.api.v1.views import base_routes

v1_routes = APISlashRouter(prefix='/api/v1', tags=['v1'])
v1_routes.include_router(base_routes)
