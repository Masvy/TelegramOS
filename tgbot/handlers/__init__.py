from .start import start_router
from .admin import admin_router

routers_list = [
    admin_router,
    start_router,
]

__all__ = [
    'routers_list',
]
