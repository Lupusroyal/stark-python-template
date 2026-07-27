from sqlalchemy.orm import Session

from stark.models.audit_log import AuditLog


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

    db.add(audit)
    db.commit()
    db.refresh(audit)

    return audit


def get_audit_logs(db: Session):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
