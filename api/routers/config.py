"""
Platform configuration inspection and live update endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from core.config_loader import config_loader
from core.module_registry import module_registry
from api.middleware.auth_middleware import get_current_user
from core.database.models import User

router = APIRouter(prefix="/api/config", tags=["Configuration"])

@router.get("")
async def get_configuration():
    """Retrieve active platform configuration."""
    cfg = config_loader.get_config()
    # Mask sensitive credentials
    safe_cfg = dict(cfg)
    if "database" in safe_cfg and isinstance(safe_cfg["database"], dict):
        db_copy = dict(safe_cfg["database"])
        db_copy["password"] = "******" if db_copy.get("password") else ""
        safe_cfg["database"] = db_copy
    return safe_cfg

@router.post("/update")
async def update_configuration(
    updates: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Apply runtime modifications to platform configuration (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin permissions required to modify platform configuration.")

    updated = config_loader.update_platform_config(updates)
    module_registry.reload_master_config()
    return {"status": "success", "configuration": updated}
