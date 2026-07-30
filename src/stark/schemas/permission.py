from pydantic import BaseModel, ConfigDict


class PermissionCreate(BaseModel):
    name: str
    description: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "users.create",
                "description": "Permite criar usuários",
            }
        }
    )


class PermissionUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "description": "Descrição atualizada",
            }
        }
    )


class PermissionResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "users.create",
                "description": "Permite criar usuários",
            }
        },
    )
