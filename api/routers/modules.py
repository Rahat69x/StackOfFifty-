"""
Module control and management endpoints for StackOfFifty.
"""
from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Dict, Any, Optional
from core.module_registry import module_registry
from core.config_loader import config_loader
from core.auth.rbac import has_sufficient_role
from api.middleware.auth_middleware import get_current_user
from core.database.models import User
from api.schemas.module_schema import ModuleConfigUpdate

router = APIRouter(prefix="/api/modules", tags=["Modules"])

def get_module_or_404(module_id: str):
    """Resolve active or configured module."""
    mod = module_registry.get(module_id)
    if not mod:
        # Check if it exists in catalog but isn't loaded yet
        cfg = config_loader.get_module_config(module_id)
        if not cfg:
            raise HTTPException(status_code=404, detail=f"Module '{module_id}' not found.")
        raise HTTPException(
            status_code=400,
            detail=f"Module '{module_id}' ({cfg.get('display_name')}) is registered but not loaded or is currently disabled."
        )
    return mod

def verify_module_access(mod, user: Optional[User]):
    """Enforce per-module permission level."""
    if not user:
        return
    required_role = mod.config.get("permission_level", "viewer")
    if not has_sufficient_role(user.role, required_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Operation requires '{required_role}' permission. Your role is '{user.role}'."
        )

@router.get("", response_model=List[Dict[str, Any]])
async def list_modules(
    category: Optional[str] = None,
    status: Optional[str] = None,
    q: Optional[str] = None
):
    """List all modules from catalog with real-time status and optional filters."""
    catalog = module_registry.list_all_catalog()
    filtered = catalog

    if category:
        filtered = [m for m in filtered if m.get("category", "").lower() == category.lower()]
    if status:
        filtered = [m for m in filtered if m.get("runtime_status", "").lower() == status.lower() or m.get("status", "").lower() == status.lower()]
    if q:
        query = q.lower()
        filtered = [
            m for m in filtered
            if query in m.get("name", "").lower()
            or query in m.get("display_name", "").lower()
            or query in m.get("category", "").lower()
        ]

    return filtered

@router.get("/categories")
async def list_categories():
    """List all 12 platform security categories."""
    return config_loader.get_config().get("categories", [])

@router.get("/search")
async def search_modules(q: str = Query(..., min_length=1)):
    """Search modules by name, display name, or category."""
    return await list_modules(q=q)

@router.post("/{module_id}/start")
async def start_module(module_id: str, current_user: Optional[User] = Depends(get_current_user)):
    """Start an active module."""
    mod = get_module_or_404(module_id)
    verify_module_access(mod, current_user)
    result = await mod.start()
    return {"status": "success", "action": "start", "result": result}

@router.post("/{module_id}/stop")
async def stop_module(module_id: str, current_user: Optional[User] = Depends(get_current_user)):
    """Stop an active module."""
    mod = get_module_or_404(module_id)
    verify_module_access(mod, current_user)
    result = await mod.stop()
    return {"status": "success", "action": "stop", "result": result}

@router.post("/{module_id}/reload")
async def reload_module(module_id: str, current_user: Optional[User] = Depends(get_current_user)):
    """Hot-reload a module without restarting the platform."""
    if current_user and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hot-reloading requires admin permission.")
    try:
        mod = module_registry.reload(module_id)
        return {"status": "success", "action": "reload", "module": mod.display_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hot-reload failed: {str(e)}")

@router.get("/{module_id}/status")
async def get_module_status(module_id: str):
    """Retrieve current module health and execution status."""
    mod = get_module_or_404(module_id)
    return await mod.status_check()

@router.get("/{module_id}/results")
async def get_module_results(module_id: str):
    """Retrieve latest results and telemetry from the module."""
    mod = get_module_or_404(module_id)
    return await mod.get_results()

@router.get("/{module_id}/logs")
async def get_module_logs(module_id: str, limit: int = Query(default=100, le=500)):
    """Retrieve recent logs for a specific module."""
    mod = get_module_or_404(module_id)
    return await mod.get_logs(limit)

@router.post("/{module_id}/configure")
async def configure_module(
    module_id: str,
    payload: ModuleConfigUpdate,
    current_user: Optional[User] = Depends(get_current_user)
):
    """Update module runtime configuration."""
    mod = get_module_or_404(module_id)
    verify_module_access(mod, current_user)
    return await mod.configure(payload.settings)

@router.get("/{module_id}/report")
async def generate_module_report(module_id: str):
    """Generate a structured activity report for this module."""
    mod = get_module_or_404(module_id)
    return await mod.generate_report()
