"""
FastAPI Routers for StackOfFifty.
"""
from api.routers.modules import router as modules_router
from api.routers.auth import router as auth_router
from api.routers.logs import router as logs_router
from api.routers.alerts import router as alerts_router
from api.routers.reports import router as reports_router
from api.routers.config import router as config_router

__all__ = [
    "modules_router", "auth_router", "logs_router",
    "alerts_router", "reports_router", "config_router"
]
