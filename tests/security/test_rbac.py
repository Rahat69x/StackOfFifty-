"""
Security tests for Role-Based Access Control and authentication hierarchy.
"""
import pytest
from core.auth.rbac import has_sufficient_role, check_role_permission
from core.auth.jwt_handler import create_access_token, decode_token, hash_password, verify_password

def test_rbac_hierarchy():
    # Admin has access to everything
    assert has_sufficient_role("admin", "admin") is True
    assert has_sufficient_role("admin", "researcher") is True
    assert has_sufficient_role("admin", "viewer") is True

    # Researcher has access to researcher and viewer
    assert has_sufficient_role("researcher", "admin") is False
    assert has_sufficient_role("researcher", "researcher") is True
    assert has_sufficient_role("researcher", "viewer") is True

    # Viewer has access only to viewer
    assert has_sufficient_role("viewer", "admin") is False
    assert has_sufficient_role("viewer", "researcher") is False
    assert has_sufficient_role("viewer", "viewer") is True

def test_password_hashing_security():
    secret = "TopSecretPassword2026!"
    hashed = hash_password(secret)
    assert hashed != secret
    assert verify_password(secret, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_issuance_and_decoding():
    payload = {"sub": "analyst_alice", "role": "researcher"}
    token = create_access_token(payload)
    decoded = decode_token(token)
    assert decoded is not None
    assert decoded["sub"] == "analyst_alice"
    assert decoded["role"] == "researcher"
    assert decoded["type"] == "access"
