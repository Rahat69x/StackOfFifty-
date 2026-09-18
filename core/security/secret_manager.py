"""
Secret manager helper to safely access environment secrets.
"""
import os
from typing import Optional

def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """Retrieve secret key strictly from environment variables."""
    val = os.environ.get(key)
    if val is not None and val.strip():
        return val.strip()
    return default
