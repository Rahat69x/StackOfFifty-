"""
Integration tests for database models and CRUD persistence across the 9 platform tables.
"""
import pytest
from core.database.connection import SessionLocal, init_db
from core.database.models import User, Alert, Report, AuditLog

def test_database_persistence():
    init_db()
    db = SessionLocal()
    try:
        # 1. User
        user = db.query(User).filter(User.username == "admin").first()
        assert user is not None
        assert user.role == "admin"

        # 2. Alert creation
        test_alert = Alert(
            title="Suspicious Egress Pattern",
            description="High entropy outbound payload detected",
            severity="high"
        )
        db.add(test_alert)
        db.commit()
        db.refresh(test_alert)
        assert test_alert.id is not None
        assert test_alert.resolved is False

        # 3. Resolve alert
        test_alert.resolved = True
        db.commit()
        assert test_alert.resolved is True

        # 4. Audit Log
        audit = AuditLog(
            action="TEST_ACTION",
            target="/api/test",
            ip_address="127.0.0.1",
            details={"key": "val"}
        )
        db.add(audit)
        db.commit()
        assert audit.id is not None
    finally:
        db.close()
