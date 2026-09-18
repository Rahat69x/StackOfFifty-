"""
Authentication endpoints for AegisCore.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import timedelta
from core.database.connection import get_db
from core.database.models import User
from core.auth.jwt_handler import (
    verify_password, create_access_token, create_refresh_token,
    decode_token, hash_password
)
from api.schemas.user_schema import UserLogin, TokenResponse, UserResponse, UserRegister
from api.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate with username and password, returns JWT tokens."""
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )

    token_data = {"sub": user.username, "role": user.role, "id": user.id}
    access_token = create_access_token(token_data, expires_delta=timedelta(minutes=30))
    refresh_token = create_refresh_token(token_data, expires_delta=timedelta(days=7))

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        role=user.role,
        username=user.username
    )

@router.post("/refresh")
async def refresh_token(payload: dict, db: Session = Depends(get_db)):
    """Exchange a valid refresh token for a new access token."""
    raw_token = payload.get("refresh_token")
    if not raw_token:
        raise HTTPException(status_code=400, detail="Missing refresh token")

    data = decode_token(raw_token)
    if not data or data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    username = data.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User is no longer active")

    token_data = {"sub": user.username, "role": user.role, "id": user.id}
    new_access_token = create_access_token(token_data, expires_delta=timedelta(minutes=30))
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Log out current session."""
    return {"status": "success", "message": f"User '{current_user.username}' logged out."}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Return authenticated user profile and roles."""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active
    )
