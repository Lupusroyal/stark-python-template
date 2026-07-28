from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from stark.core.security import (
    create_access_token,
    create_refresh_token,
    hash_token,
)
from stark.models.refresh_token import RefreshToken
from stark.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from stark.repositories.user_repository import UserRepository
from stark.schemas.auth import TokenResponse


class TokenService:
    def __init__(self, db: Session):
        self.repository = RefreshTokenRepository(db)
        self.user_repository = UserRepository(db)

    def create_refresh_token(
        self,
        user_id: int,
    ) -> str:

        token = create_refresh_token()

        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=hash_token(token),
            expires_at=datetime.now(UTC) + timedelta(days=7),
        )

        self.repository.create(refresh_token)

        return token

    def validate_refresh_token(
        self,
        token: str,
    ) -> RefreshToken | None:

        token_hash = hash_token(token)

        return self.repository.get_valid_token(
            token_hash,
        )

    def create_access_token_from_refresh(
        self,
        token: str,
    ) -> str | None:

        refresh_token = self.validate_refresh_token(token)

        if refresh_token is None:
            return None

        user = self.user_repository.get_by_id(
            refresh_token.user_id,
        )

        if user is None:
            return None

        return create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

    def revoke_refresh_token(
        self,
        token: str,
    ) -> bool:
        refresh_token = self.validate_refresh_token(token)

        if refresh_token is None:
            return False

        self.repository.revoke(refresh_token)

        return True

    def rotate_refresh_token(
        self,
        token: str,
    ) -> TokenResponse | None:

        refresh_token = self.validate_refresh_token(
            token,
        )

        if refresh_token is None:
            return None

        user = self.user_repository.get_by_id(
            refresh_token.user_id,
        )

        if user is None:
            return None

        self.repository.revoke(
            refresh_token,
        )

        new_refresh_token = self.create_refresh_token(
            user.id,
        )

        new_access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )
