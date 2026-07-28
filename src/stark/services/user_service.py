from sqlalchemy.orm import Session

from stark.core.security import hash_password
from stark.models.user import User, UserRole
from stark.repositories.user_repository import UserRepository
from stark.schemas.user import UserCreate, UserUpdate


def create_user(
    db: Session,
    user: UserCreate,
):
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    repository = UserRepository(db)

    return repository.save(db_user)


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):
    repository = UserRepository(db)

    users = repository.list_all(
        skip,
        limit,
    )

    total = repository.count()

    return {
        "items": users,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


def get_user_by_id(
    db: Session,
    user_id: int,
):
    repository = UserRepository(db)

    return repository.get_by_id(user_id)


def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate,
):
    repository = UserRepository(db)

    user = repository.get_by_id(user_id)

    if user is None:
        return None

    user.name = user_data.name
    user.email = user_data.email

    return repository.update(user)


def update_current_user(
    db: Session,
    current_user: User,
    user_data: UserUpdate,
):
    repository = UserRepository(db)

    current_user.name = user_data.name
    current_user.email = user_data.email

    return repository.update(current_user)


def activate_user(
    db: Session,
    user_id: int,
):
    repository = UserRepository(db)

    user = repository.get_by_id(user_id)

    if user is None:
        return None

    user.is_active = True

    return repository.update(user)


def deactivate_user(
    db: Session,
    user_id: int,
):
    repository = UserRepository(db)

    user = repository.get_by_id(user_id)

    if user is None:
        return None

    user.is_active = False

    return repository.update(user)


def update_user_role(
    db: Session,
    user_id: int,
    role: UserRole,
):
    repository = UserRepository(db)

    user = repository.get_by_id(user_id)

    if user is None:
        return None

    user.role = role

    return repository.update(user)
