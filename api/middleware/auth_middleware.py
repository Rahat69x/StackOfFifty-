"""
Authentication and Role-Based Authorization Dependencies for FastAPI.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from core.database.connection import get_db
from core.database.models import User
from core.auth.jwt_handler import decode_token
from core.auth.rbac import has_sufficient_role
from core.config_loader import config_loader

security = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Retrieve and validate the authenticated user from JWT token."""
    features = config_loader.get_config().get("features", {})
    # If auth is explicitly disabled in config, return a synthetic admin
    if not features.get("enable_auth", True):
        return User(id="dev-admin", username="local_admin", role="admin", is_active=True)

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = db.query(User).filter(User.username == username).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

    return user

def require_role(required_role: str):
    """Factory creating an authorization dependency requiring at least the specified role."""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        features = config_loader.get_config().get("features", {})
        if not features.get("enable_rbac", True):
            return current_user

        if not has_sufficient_role(current_user.role, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Required role '{required_role}' exceeds user role '{current_user.role}'."
            )
        return current_user
    return role_checker
