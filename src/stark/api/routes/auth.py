from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from stark.core.database import get_db
from stark.core.exceptions import InvalidCredentialsException
from stark.core.security import create_access_token
from stark.dependencies.auth import get_current_user
from stark.models.user import User
from stark.schemas.auth import TokenResponse
from stark.services.auth_service import authenticate_user
from stark.services.token_service import TokenService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not user:
        raise InvalidCredentialsException()

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        }
    )

    token_service = TokenService(db)

    refresh_token = token_service.create_refresh_token(
        user.id,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me")
def me(
    user: User = Depends(get_current_user),
):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }
