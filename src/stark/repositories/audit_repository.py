from sqlalchemy.orm import Session

from stark.models.audit_log import AuditLog


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        audit_log: AuditLog,
    ) -> AuditLog:
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)

        return audit_log

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditLog]:
        return (
            self.db.query(AuditLog)
            .order_by(AuditLog.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self) -> int:
        return self.db.query(AuditLog).count()
