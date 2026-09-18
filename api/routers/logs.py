"""
Centralized log querying endpoints.
"""
from fastapi import APIRouter, Query
from typing import List, Dict, Any, Optional
from core.logger import get_all_recent_logs

router = APIRouter(prefix="/api/logs", tags=["Logs"])

@router.get("", response_model=List[Dict[str, Any]])
async def get_system_logs(
    level: Optional[str] = None,
    module: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(default=100, le=500)
):
    """Retrieve centralized logs across all modules."""
    logs = get_all_recent_logs(limit=500)

    if level:
        logs = [entry for entry in logs if entry.get("level", "").upper() == level.upper()]
    if module:
        logs = [entry for entry in logs if entry.get("module", "").lower() == module.lower()]
    if search:
        s = search.lower()
        logs = [entry for entry in logs if s in entry.get("message", "").lower()]

    return logs[-limit:]
