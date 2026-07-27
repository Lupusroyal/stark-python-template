from sqlalchemy.orm import Session

from stark.models.permission import Permission
from stark.models.role_permission import RolePermission

DEFAULT_ROLE_PERMISSIONS = {
    "admin": [
        "users.read",
        "users.update",
        "users.delete",
        "audit.read",
    ],
    "user": [
        "users.read",
    ],
}


def create_default_role_permissions(db: Session):
    for role, permissions in DEFAULT_ROLE_PERMISSIONS.items():
        for permission_name in permissions:
            permission = (
                db.query(Permission).filter(Permission.name == permission_name).first()
            )

            if permission is None:
                continue

            exists = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role == role,
                    RolePermission.permission_id == permission.id,
                )
                .first()
            )

            if not exists:
                role_permission = RolePermission(
                    role=role,
                    permission_id=permission.id,
                )

                db.add(role_permission)

    db.commit()
