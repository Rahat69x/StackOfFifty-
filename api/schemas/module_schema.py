"""
Pydantic schemas for module operations.
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ModuleConfigUpdate(BaseModel):
    settings: Dict[str, Any] = Field(..., description="Key-value configuration settings to update")

class ModuleResponse(BaseModel):
    id: str
    name: str
    display_name: str
    category: str
    version: str
    status: str
    permission_level: str
    lab_only: bool
    is_loaded: bool = False
    runtime_status: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

class ModuleExecutionResponse(BaseModel):
    status: str
    module: str
    details: Optional[Dict[str, Any]] = None
