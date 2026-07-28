from sqlalchemy.orm import Session

from stark.models.role_permission import RolePermission


class RolePermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_role_permission(
        self,
        role: str,
        permission_id: int,
    ) -> RolePermission | None:
        return (
            self.db.query(RolePermission)
            .filter(
                RolePermission.role == role,
                RolePermission.permission_id == permission_id,
            )
            .first()
        )

    def save(
        self,
        role_permission: RolePermission,
    ) -> RolePermission:
        self.db.add(role_permission)
        self.db.commit()
        self.db.refresh(role_permission)

        return role_permission

    def list_by_role(
        self,
        role: str,
    ) -> list[RolePermission]:
        return self.db.query(RolePermission).filter(RolePermission.role == role).all()
