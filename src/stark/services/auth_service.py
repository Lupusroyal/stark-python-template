from sqlalchemy.orm import Session

from stark.core.security import verify_password
from stark.models.user import User


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
