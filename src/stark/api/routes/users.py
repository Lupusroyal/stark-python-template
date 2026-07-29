from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from stark.core.database import get_db
from stark.core.exceptions import (
    EmailAlreadyExistsException,
    UserNotFoundException,
)
from stark.dependencies.auth import get_current_user
from stark.dependencies.permission import require_permission
from stark.models.user import User
from stark.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from stark.services.audit_service import create_audit_log
from stark.services.user_service import (
    create_user,
    deactivate_user,
    get_user_by_id,
    update_current_user,
    update_user,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
)
def create(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = create_user(db, user)

    if db_user is None:
        raise EmailAlreadyExistsException()

    return db_user


@router.get("/me")
def get_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }


@router.put("/me", response_model=UserResponse)
def update_profile(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_current_user(
        db,
        current_user,
        user,
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.read")),
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise UserNotFoundException()

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.update")),
):
    updated_user = update_user(
        db,
        user_id,
        user,
    )

    if updated_user is None:
        raise UserNotFoundException()

    create_audit_log(
        db,
        actor_id=current_user.id,
        action="USER_UPDATE",
        target_id=user_id,
    )

    return updated_user


@router.delete("/me")
def delete_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.delete")),
):
    deactivate_user(
        db,
        current_user.id,
    )

    create_audit_log(
        db,
        actor_id=current_user.id,
        action="USER_DELETE",
        target_id=current_user.id,
    )

    return {"message": "Usuário desativado com sucesso"}
