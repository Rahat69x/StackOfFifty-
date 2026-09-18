"""
StackOfFifty - Central FastAPI Backend Application Entry Point.
"""
import os
import secrets
import time
from contextlib import asynccontextmanager
import psutil
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.logger import get_logger
from core.database.connection import init_db, SessionLocal
from core.database.models import User, Alert
from core.auth.jwt_handler import hash_password
from core.module_registry import module_registry
from core.config_loader import config_loader
from core.event_bus import event_bus

from api.middleware.logging_middleware import LoggingAndAuditMiddleware
from api.routers import (
    modules_router, auth_router, logs_router,
    alerts_router, reports_router, config_router
)

logger = get_logger("api.main")
START_TIME = time.time()

def seed_initial_admin():
    """Ensure at least one administrator account exists without hardcoded credentials."""
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.role == "admin").first()
        if not admin_user:
            username = os.environ.get("ADMIN_SEED_USERNAME", "admin").strip()
            email = os.environ.get("ADMIN_SEED_EMAIL", "admin@stackoffifty.local").strip()
            password = os.environ.get("ADMIN_SEED_PASSWORD", "").strip()

            if not password:
                # Generate high-entropy 24-character random password if none was supplied
                password = secrets.token_urlsafe(18)
                logger.warning("=" * 60)
                logger.warning("No ADMIN_SEED_PASSWORD was provided in environment.")
                logger.warning(f"Generated temporary master password for admin: {password}")
                logger.warning("Save this password or update it immediately in your profile.")
                logger.warning("=" * 60)

            admin = User(
                username=username,
                email=email,
                password_hash=hash_password(password),
                role="admin",
                is_active=True
            )
            db.add(admin)

            # Seed an initial welcome alert
            welcome_alert = Alert(
                title="StackOfFifty Platform Initialized",
                description="Core framework services and defensive module registry loaded successfully.",
                severity="info",
                resolved=False
            )
            db.add(welcome_alert)
            db.commit()
            logger.info(f"Initialized administrative account: '{username}'")
    except Exception as e:
        logger.error(f"Error during admin user seeding: {e}")
        db.rollback()
    finally:
        db.close()

def attach_event_listeners():
    """Subscribe platform persistence to the EventBus."""
    def on_security_event(event_payload: dict):
        # Persist high-severity detections as platform alerts
        event_type = event_payload.get("event_type", "")
        data = event_payload.get("data", {})
        sender = event_payload.get("sender", "")

        if any(term in event_type.lower() for term in ("probe", "violation", "dropped", "failed", "locked")):
            try:
                db = SessionLocal()
                alert = Alert(
                    module_id=sender,
                    title=f"Security Event: {event_type}",
                    description=str(data),
                    severity="high" if "probe" in event_type or "locked" in event_type else "medium",
                    resolved=False
                )
                db.add(alert)
                db.commit()
                db.close()
            except Exception as ex:
                logger.warning(f"Could not persist event alert: {ex}")

    event_bus.subscribe("*", on_security_event)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing StackOfFifty Cybersecurity Platform...")
    init_db()
    seed_initial_admin()
    attach_event_listeners()

    # Load modules
    module_registry.load_all()

    # Mount module custom API routers if provided
    for mod_id, mod in module_registry.modules.items():
        if hasattr(mod, "api_router") and mod.api_router:
            app.include_router(mod.api_router, prefix="/api/modules/custom")

    logger.info("StackOfFifty backend ready to service requests.")
    yield

    # Shutdown
    logger.info("Shutting down StackOfFifty platform...")
    for mod_id, mod in list(module_registry.modules.items()):
        try:
            await mod.stop()
        except Exception as e:
            logger.error(f"Error stopping module {mod_id}: {e}")

platform_info = config_loader.get_config().get("platform", {})

app = FastAPI(
    title=platform_info.get("name", "StackOfFifty"),
    description=platform_info.get("description", "Unified Defensive Cybersecurity Platform"),
    version=platform_info.get("version", "1.0.0"),
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers & Audit Middleware
app.add_middleware(LoggingAndAuditMiddleware)

# Include Central Routers
app.include_router(modules_router)
app.include_router(auth_router)
app.include_router(logs_router)
app.include_router(alerts_router)
app.include_router(reports_router)
app.include_router(config_router)

@app.get("/api/health")
async def platform_health():
    """Health check endpoint providing platform diagnostics and hardware metrics."""
    cpu_percent = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    uptime_seconds = int(time.time() - START_TIME)

    loaded_modules = len(module_registry.modules)
    total_configured = len(config_loader.get_config().get("modules", []))

    active_platform = config_loader.get_config().get("platform", {})
    return {
        "status": "healthy",
        "platform": active_platform.get("display_name", "StackOfFifty"),
        "version": active_platform.get("version", "1.0.0"),
        "uptime_seconds": uptime_seconds,
        "system": {
            "cpu_usage_percent": cpu_percent,
            "memory_usage_percent": memory.percent,
            "memory_available_mb": round(memory.available / (1024 * 1024), 2)
        },
        "modules": {
            "loaded_active_count": loaded_modules,
            "total_configured_count": total_configured
        }
    }

@app.exception_handler(Exception)
async def structured_exception_handler(request: Request, exc: Exception):
    """Global structured exception handler: never leak stack traces (spec page 51)."""
    logger.error(f"Unhandled error on {request.method} {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred during request processing.",
            "path": request.url.path
        }
    )
