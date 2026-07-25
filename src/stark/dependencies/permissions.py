from fastapi import Depends, HTTPException, status

from stark.core.security import get_current_user
from stark.models.user import User


def require_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado",
        )

    return current_user
