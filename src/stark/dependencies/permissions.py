from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from stark.core.database import get_db
from stark.core.security import get_current_user
from stark.models.user import User
from stark.services.authorization_service import user_has_permission


def require_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado",
        )

    return current_user


def require_permission(permission_name: str):
    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        if not user_has_permission(
            db,
            current_user,
            permission_name,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente",
            )

        return current_user

    return permission_checker
