"""
Role-Based Access Control (RBAC) definitions and enforcement.
"""
from enum import Enum
from typing import Dict

class Role(str, Enum):
    ADMIN = "admin"
    RESEARCHER = "researcher"
    VIEWER = "viewer"

ROLE_HIERARCHY: Dict[str, int] = {
    Role.ADMIN.value: 3,
    Role.RESEARCHER.value: 2,
    Role.VIEWER.value: 1
}

def has_sufficient_role(user_role: str, required_role: str) -> bool:
    """Evaluate if user's role meets or exceeds the required permission level."""
    user_level = ROLE_HIERARCHY.get(user_role.lower(), 0)
    req_level = ROLE_HIERARCHY.get(required_role.lower(), 0)
    return user_level >= req_level

def check_role_permission(user_role: str, module_permission_level: str) -> bool:
    """Validate user against a module's configured permission level."""
    return has_sufficient_role(user_role, module_permission_level)
