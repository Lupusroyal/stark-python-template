from pydantic import BaseModel, ConfigDict, EmailStr


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
    role: str

    class Config:
        from_attributes = True


class UserRoleUpdate(BaseModel):
    role: str
