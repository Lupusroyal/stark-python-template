from sqlalchemy.orm import Session

from stark.models.user import User
from stark.repositories.permission_repository import PermissionRepository
from stark.repositories.role_permission_repository import (
    RolePermissionRepository,
)


def user_has_permission(
    db: Session,
    user: User,
    permission_name: str,
) -> bool:
    permission_repository = PermissionRepository(db)

    permission = permission_repository.get_by_name(
        permission_name,
    )

    if permission is None:
        return False

    role_repository = RolePermissionRepository(db)

    role_permission = role_repository.get_role_permission(
        user.role,
        permission.id,
    )

    return role_permission is not None
