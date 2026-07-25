from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from stark.core.database import get_db
from stark.core.security import create_access_token
from stark.schemas.auth import LoginRequest, TokenResponse
from stark.services.user_service import authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        data.email,
        data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
