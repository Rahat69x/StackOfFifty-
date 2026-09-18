"""
API routes for IoT Device UPnP & mDNS Auditor.
"""
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/upnp_mdns_iot_auditor", tags=["IoT Device UPnP & mDNS Auditor"])

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
