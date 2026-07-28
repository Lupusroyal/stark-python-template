from sqlalchemy.orm import Session

from stark.models.audit_log import AuditLog
from stark.repositories.audit_repository import AuditRepository


def create_audit_log(
    db: Session,
    actor_id: int,
    action: str,
    target_id: int,
    details: dict | None = None,
):
    audit = AuditLog(
        actor_id=actor_id,
        action=action,
        target_id=target_id,
        details=details,
    )

    repository = AuditRepository(db)

    return repository.save(audit)


def get_audit_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):
    repository = AuditRepository(db)

    logs = repository.list_all(
        skip,
        limit,
    )

    total = repository.count()

    return {
        "items": logs,
        "total": total,
        "skip": skip,
        "limit": limit,
    }
