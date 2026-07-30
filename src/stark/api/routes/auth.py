from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from stark.core.database import get_db
from stark.core.exceptions import InvalidCredentialsException
from stark.core.security import create_access_token
from stark.dependencies.auth import get_current_user
from stark.models.user import User
from stark.schemas.auth import (
    RefreshTokenRequest,
    TokenResponse,
)
from stark.schemas.error import ErrorResponse
from stark.services.auth_service import authenticate_user
from stark.services.token_service import TokenService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Autenticar usuário",
    description="Autentica um usuário utilizando e-mail e senha e retorna um Access Token e um Refresh Token.",
    responses={
        200: {"description": "Autenticação realizada com sucesso"},
        401: {
            "model": ErrorResponse,
            "description": "Credenciais inválidas",
        },
    },
)
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

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get(
    "/me",
    summary="Obter usuário autenticado",
    description="Retorna os dados do usuário autenticado.",
    responses={
        200: {"description": "Dados do usuário"},
        401: {
            "model": ErrorResponse,
            "description": "Credenciais inválidas",
        },
    },
)
def me(
    user: User = Depends(get_current_user),
):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Renovar tokens",
    description="Realiza a rotação do Refresh Token e gera um novo Access Token.",
    responses={
        200: {"description": "Tokens renovados"},
        401: {
            "model": ErrorResponse,
            "description": "Refresh Token inválido",
        },
    },
)
def refresh(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    token_service = TokenService(db)

    tokens = token_service.rotate_refresh_token(
        data.refresh_token,
    )

    if tokens is None:
        raise InvalidCredentialsException()

    return tokens


@router.post(
    "/logout",
    summary="Encerrar sessão",
    description="Revoga o Refresh Token informado, encerrando a sessão do usuário.",
    responses={
        200: {"description": "Logout realizado com sucesso"},
        401: {
            "model": ErrorResponse,
            "description": "Refresh Token inválido",
        },
    },
)
def logout(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    token_service = TokenService(db)

    revoked = token_service.revoke_refresh_token(
        data.refresh_token,
    )

    if not revoked:
        raise InvalidCredentialsException()

    return {
        "message": "Logged out successfully",
    }
