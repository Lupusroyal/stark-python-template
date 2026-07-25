from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from stark.core.database import get_db
from stark.dependencies.permissions import require_admin
from stark.models.user import User
from stark.schemas.user import (
    UserAdminResponse,
    UserRoleUpdate,
)
from stark.services.user_service import (
    activate_user,
    deactivate_user,
    get_user_by_id,
    get_users,
    update_user_role,
)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get(
    "/users",
    response_model=list[UserAdminResponse],
)
def list_users_admin(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return get_users(db)


@router.get(
    "/users/{user_id}",
    response_model=UserAdminResponse,
)
def get_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    return user


@router.patch(
    "/users/{user_id}/activate",
    response_model=UserAdminResponse,
)
def activate_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = activate_user(
        db,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    return user


@router.patch(
    "/users/{user_id}/deactivate",
    response_model=UserAdminResponse,
)
def deactivate_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = deactivate_user(
        db,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    return user


@router.patch(
    "/users/{user_id}/role",
    response_model=UserAdminResponse,
)
def change_user_role(
    user_id: int,
    data: UserRoleUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = update_user_role(
        db,
        user_id,
        data.role,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    return user
