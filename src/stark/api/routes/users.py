from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from stark.core.database import get_db
from stark.schemas.user import UserCreate, UserResponse
from stark.services.user_service import create_user, get_users

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserResponse)
def create(
    user: UserCreate,
    db: Session = Depends(get_db),  # noqa: B008
):
    return create_user(db, user)


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),  # noqa: B008
):
    return get_users(db)
