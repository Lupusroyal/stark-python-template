from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
    username: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "user@example.com",
                "password": "123456",
            }
        }
    )


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "<jwt_access_token>",
                "refresh_token": "<refresh_token>",
                "token_type": "bearer",
            }
        }
    )


class RefreshTokenRequest(BaseModel):
    refresh_token: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "<refresh_token>",
            }
        }
    )
