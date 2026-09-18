"""
API routes for E2EE Protocol & Key Exchange Auditor.
"""
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/e2ee_messaging_audit_core", tags=["E2EE Protocol & Key Exchange Auditor"])

module_instance = None

def set_module(mod):
    global module_instance
    module_instance = mod

def get_module():
    global module_instance
    if module_instance is None:
        try:
            import main
            if hasattr(main, "default_module"):
                module_instance = main.default_module
            elif hasattr(main, "Module"):
                module_instance = main.Module()
        except Exception:
            pass
    return module_instance

@router.get("/status")
async def get_module_status():
    mod = get_module()
    if not mod:
        raise HTTPException(status_code=503, detail="Module not initialized")
    return await mod.get_results()
