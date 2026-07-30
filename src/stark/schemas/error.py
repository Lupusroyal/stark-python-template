from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    message: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "PERMISSION_DENIED",
                "message": "Permissão insuficiente",
            }
        }
    }
