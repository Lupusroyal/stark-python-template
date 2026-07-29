from fastapi import Depends
from sqlalchemy.orm import Session

from stark.core.database import get_db
from stark.core.exceptions import PermissionDeniedException
from stark.dependencies.auth import get_current_user
from stark.models.user import User
from stark.services.permission_service import has_permission


def require_permission(permission_name: str):

    def permission_checker(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):

        allowed = has_permission(
            db,
            user.role,
            permission_name,
        )

        if not allowed:
            raise PermissionDeniedException()

        return user

    return permission_checker
