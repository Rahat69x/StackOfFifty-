"""
Report generation and query endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from core.database.connection import get_db
from core.database.models import Report
from core.module_registry import module_registry

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("")
async def list_reports(
    module_id: Optional[str] = None,
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db)
):
    """Retrieve historical and generated reports."""
    query = db.query(Report)
    if module_id:
        query = query.filter(Report.module_id == module_id)
    records = query.order_by(Report.created_at.desc()).limit(limit).all()

    reports = [
        {
            "id": r.id,
            "module_id": r.module_id,
            "title": r.title,
            "content": r.content,
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in records
    ]
    return reports

@router.post("/generate/{module_id}")
async def trigger_report_generation(module_id: str, db: Session = Depends(get_db)):
    """Trigger a live report generation for a module and save to database."""
    mod = module_registry.get(module_id)
    if not mod:
        raise HTTPException(status_code=404, detail=f"Active module '{module_id}' not found.")

    report_data = await mod.generate_report()
    report_record = Report(
        module_id=module_id,
        title=f"Security Audit Report - {mod.display_name}",
        content=report_data
    )
    db.add(report_record)
    db.commit()
    db.refresh(report_record)

    return {
        "id": report_record.id,
        "module_id": module_id,
        "title": report_record.title,
        "content": report_record.content,
        "created_at": report_record.created_at.isoformat()
    }
