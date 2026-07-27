from sqlalchemy.orm import Session

from stark.models.permission import Permission
from stark.models.role_permission import RolePermission
from stark.models.user import User


def user_has_permission(
    db: Session,
    user: User,
    permission_name: str,
) -> bool:
    permission = (
        db.query(Permission)
        .filter(
            Permission.name == permission_name,
        )
        .first()
    )

    if permission is None:
        return False

    role_permission = (
        db.query(RolePermission)
        .filter(
            RolePermission.role == user.role,
            RolePermission.permission_id == permission.id,
        )
        .first()
    )

    return role_permission is not None
