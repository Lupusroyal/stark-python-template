from sqlalchemy.orm import Session

from stark.core.security import hash_password
from stark.models.user import User
from stark.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate):

    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_id(
    db: Session,
    user_id: int,
):
    return db.query(User).filter(User.id == user_id).first()


def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        return None

    user.name = user_data.name
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return user


def update_current_user(
    db: Session,
    current_user: User,
    user_data: UserUpdate,
):
    current_user.name = user_data.name
    current_user.email = user_data.email

    db.commit()
    db.refresh(current_user)

    return current_user


def deactivate_user(
    db: Session,
    user_id: int,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        return None

    user.is_active = False

    db.commit()
    db.refresh(user)

    return user


def activate_user(
    db: Session,
    user_id: int,
):
    user = get_user_by_id(db, user_id)

    if user is None:
        return None

    user.is_active = True

    db.commit()
    db.refresh(user)

    return user


def update_user_role(
    db: Session,
    user_id: int,
    role: str,
):
    user = get_user_by_id(db, user_id)

    if user is None:
        return None

    user.role = role

    db.commit()
    db.refresh(user)

    return user
