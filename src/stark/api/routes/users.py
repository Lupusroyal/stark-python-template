from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from stark.core.database import get_db
from stark.core.security import get_current_user
from stark.models.user import User
from stark.schemas.user import UserCreate, UserResponse
from stark.services.user_service import create_user, get_users

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


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_users(db)


@router.get("/me")
def get_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }
