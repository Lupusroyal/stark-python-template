from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from stark.core.database import get_db
from stark.core.security import get_current_user
from stark.models.user import User
from stark.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
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


@router.post("/", response_model=UserResponse)
def create(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = create_user(db, user)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado",
        )

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
    current_user: User = Depends(get_current_user),
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


@router.put("/{user_id}", response_model=UserResponse)
def update(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_user = update_user(
        db,
        user_id,
        user,
    )

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    return updated_user


@router.delete("/me")
def delete_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deactivate_user(
        db,
        current_user.id,
    )

    return {"message": "Usuário desativado com sucesso"}
