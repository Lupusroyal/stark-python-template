from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from stark.models.user import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    name: str
    email: EmailStr


class UserAdminResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserRoleUpdate(BaseModel):
    role: UserRole


class AuditLogResponse(BaseModel):
    id: int
    actor_id: int
    action: str
    target_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
