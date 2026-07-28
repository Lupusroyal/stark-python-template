from sqlalchemy.orm import Session

from stark.models.permission import Permission


class PermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(
        self,
        name: str,
    ) -> Permission | None:
        return self.db.query(Permission).filter(Permission.name == name).first()

    def get_by_id(
        self,
        permission_id: int,
    ) -> Permission | None:
        return self.db.query(Permission).filter(Permission.id == permission_id).first()

    def list_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Permission]:
        return (
            self.db.query(Permission)
            .order_by(Permission.name)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self) -> int:
        return self.db.query(Permission).count()

    def save(
        self,
        permission: Permission,
    ) -> Permission:
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)

        return permission

    def delete(
        self,
        permission: Permission,
    ) -> None:
        self.db.delete(permission)
        self.db.commit()
