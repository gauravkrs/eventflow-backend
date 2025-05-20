from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"

class PermissionBase(BaseModel):
    user_id: int
    role: RoleEnum

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    role: RoleEnum

class PermissionResponse(PermissionBase):
    id: int
    event_id: int

    class Config:
        from_attributes = True
