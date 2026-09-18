"""
Database connection manager supporting PostgreSQL with zero-config SQLite fallback.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from core.logger import get_logger

logger = get_logger("database")

Base = declarative_base()

def get_database_url() -> str:
    """Resolve database URL based on environment or fallback to SQLite."""
    db_host = os.environ.get("DB_HOST", "").strip()
    if db_host:
        user = os.environ.get("DB_USER", "aegis_user")
        password = os.environ.get("DB_PASSWORD", "aegis_secure_password")
        port = os.environ.get("DB_PORT", "5432")
        db_name = os.environ.get("DB_NAME", "stackoffifty")
        url = f"postgresql://{user}:{password}@{db_host}:{port}/{db_name}"
        logger.info(f"Using PostgreSQL database connection on {db_host}:{port}")
        return url

    sqlite_path = os.environ.get("DB_SQLITE_PATH", "stackoffifty.db")
    logger.info(f"Using local SQLite fallback database at {sqlite_path}")
    return f"sqlite:///{sqlite_path}"

db_url = get_database_url()
connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

engine = create_engine(
    db_url,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """FastAPI dependency for obtaining a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all database tables."""
    from core.database import models  # Ensure models are imported
    Base.metadata.create_all(bind=engine)
    logger.info("Database schemas verified and initialized successfully.")
