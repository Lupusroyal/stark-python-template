from sqlalchemy.orm import Session

from stark.core.security import verify_password
from stark.repositories.user_repository import UserRepository


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    repository = UserRepository(db)

    user = repository.get_by_email(email)

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
