from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    actor_id: int
    action: str
    target_id: int
    details: dict | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "actor_id": 1,
                "action": "change_role",
                "target_id": 5,
                "details": {
                    "old_role": "user",
                    "new_role": "admin",
                },
                "created_at": "2026-07-30T14:30:00Z",
            }
        },
    )
