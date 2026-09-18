"""
Input sanitization and regex validation utilities.
"""
import re
from fastapi import HTTPException

MODULE_ID_PATTERN = re.compile(r"^mod_[0-9]{3}$")
SLUG_PATTERN = re.compile(r"^[a-z0-9_]{3,50}$")

def sanitize_string(val: str, max_length: int = 255) -> str:
    """Strip dangerous characters and enforce length boundaries."""
    if not isinstance(val, str):
        return ""
    # Strip control characters
    cleaned = "".join(ch for ch in val if ch.isprintable())
    return cleaned[:max_length].strip()

def validate_module_id(module_id: str) -> str:
    """Ensure module_id adheres to mod_XXX pattern."""
    if not MODULE_ID_PATTERN.match(module_id):
        raise HTTPException(status_code=400, detail=f"Invalid module ID '{module_id}'. Expected format 'mod_XXX'.")
    return module_id
