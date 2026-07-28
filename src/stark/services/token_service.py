from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from stark.core.security import (
    create_refresh_token,
    hash_token,
)
from stark.models.refresh_token import RefreshToken
from stark.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)


class TokenService:
    def __init__(self, db: Session):
        self.repository = RefreshTokenRepository(db)

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
