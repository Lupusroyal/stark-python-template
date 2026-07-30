from pydantic import BaseModel, ConfigDict, EmailStr

from stark.models.user import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "João Silva",
                "email": "joao@example.com",
                "password": "123456",
            }
        }
    )


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "João Silva",
                "email": "joao@example.com",
            }
        },
    )


class UserUpdate(BaseModel):
    name: str
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "João Atualizado",
                "email": "joao@example.com",
            }
        }
    )


class UserAdminResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Administrador",
                "email": "admin@example.com",
                "is_active": True,
                "role": "admin",
            }
        },
    )


class UserRoleUpdate(BaseModel):
    role: UserRole

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role": "admin",
            }
        }
    )
