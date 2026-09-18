"""
SQLAlchemy ORM models mirroring the 9 platform tables from Step 10 of the spec.
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Boolean, DateTime, Text, JSON, ForeignKey, Integer
)
from sqlalchemy.orm import relationship
from core.database.connection import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="viewer", nullable=False)  # admin, researcher, viewer
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    executions = relationship("ModuleExecution", back_populates="user")
    alerts_resolved = relationship("Alert", back_populates="resolver")
    reports_generated = relationship("Report", back_populates="creator")

class ModuleModel(Base):
    __tablename__ = "modules"

    id = Column(String(50), primary_key=True)  # mod_001, etc.
    name = Column(String(100), nullable=False, index=True)
    display_name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    version = Column(String(20), default="1.0.0")
    status = Column(String(20), default="enabled")  # enabled, disabled, running, stopped
    config = Column(JSON, default=dict)
    lab_only = Column(Boolean, default=False)
    last_started = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    executions = relationship("ModuleExecution", back_populates="module")

class ModuleExecution(Base):
    __tablename__ = "module_executions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    module_id = Column(String(50), ForeignKey("modules.id"), nullable=False)
    started_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    started_at = Column(DateTime, default=utc_now)
    ended_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="running")  # running, completed, failed
    result = Column(JSON, default=dict)

    module = relationship("ModuleModel", back_populates="executions")
    user = relationship("User", back_populates="executions")

class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    module_id = Column(String(50), nullable=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    severity = Column(String(20), default="info")  # critical, high, medium, low, info
    payload = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=utc_now, index=True)

class LogModel(Base):
    __tablename__ = "logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    module_id = Column(String(50), nullable=True, index=True)
    level = Column(String(10), default="INFO", index=True)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    message = Column(Text, nullable=False)
    metadata_json = Column("metadata", JSON, default=dict)
    timestamp = Column(DateTime, default=utc_now, index=True)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    module_id = Column(String(50), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(20), default="medium", index=True)  # critical, high, medium, low, info
    resolved = Column(Boolean, default=False, index=True)
    resolved_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=utc_now, index=True)

    resolver = relationship("User", back_populates="alerts_resolved")

class Report(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    module_id = Column(String(50), nullable=True, index=True)
    generated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now, index=True)

    creator = relationship("User", back_populates="reports_generated")

class ConfigurationModel(Base):
    __tablename__ = "configurations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    scope = Column(String(50), default="platform", index=True)  # platform or module_id
    key = Column(String(100), nullable=False, index=True)
    value = Column(JSON, default=dict)
    updated_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False, index=True)
    target = Column(String(100), nullable=True)
    details = Column(JSON, default=dict)
    ip_address = Column(String(45), nullable=True)
    timestamp = Column(DateTime, default=utc_now, index=True)
