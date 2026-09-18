"""
Security alerts and real-time event feed endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from core.database.connection import get_db
from core.database.models import Alert, User
from core.event_bus import event_bus
from api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

@router.get("")
async def get_alerts(
    resolved: Optional[bool] = None,
    severity: Optional[str] = None,
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db)
):
    """Retrieve security alerts merged with real-time event bus detections."""
    query = db.query(Alert)
    if resolved is not None:
        query = query.filter(Alert.resolved == resolved)
    if severity:
        query = query.filter(Alert.severity == severity.lower())

    db_alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()

    # Formulate response
    formatted_alerts = [
        {
            "id": a.id,
            "module_id": a.module_id,
            "title": a.title,
            "description": a.description,
            "severity": a.severity,
            "resolved": a.resolved,
            "timestamp": a.created_at.isoformat() if a.created_at else None
        }
        for a in db_alerts
    ]

    # Include recent unpersisted events from event bus
    recent_events = event_bus.get_recent_events(limit=20)

    return {
        "alerts": formatted_alerts,
        "recent_event_stream": recent_events
    }

@router.post("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Mark an alert as resolved."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.resolved = True
    if current_user:
        alert.resolved_by = current_user.id
    db.commit()
    return {"status": "success", "alert_id": alert_id, "resolved": True}
