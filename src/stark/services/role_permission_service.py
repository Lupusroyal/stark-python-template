from sqlalchemy.orm import Session

from stark.models.role_permission import RolePermission
from stark.repositories.permission_repository import PermissionRepository
from stark.repositories.role_permission_repository import (
    RolePermissionRepository,
)

DEFAULT_ROLE_PERMISSIONS = {
    "admin": [
        "users.read",
        "users.update",
        "users.delete",
        "audit.read",
        "permissions.read",
        "permissions.create",
        "permissions.update",
        "permissions.delete",
    ],
    "user": [
        "users.read",
    ],
}


def create_default_role_permissions(db: Session):
    permission_repository = PermissionRepository(db)
    role_permission_repository = RolePermissionRepository(db)

    for role, permissions in DEFAULT_ROLE_PERMISSIONS.items():
        for permission_name in permissions:
            permission = permission_repository.get_by_name(
                permission_name,
            )

            if permission is None:
                continue

            exists = role_permission_repository.get_role_permission(
                role,
                permission.id,
            )

            if not exists:
                role_permission = RolePermission(
                    role=role,
                    permission_id=permission.id,
                )

                role_permission_repository.save(role_permission)
