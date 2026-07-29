from sqlalchemy.orm import Session

from stark.core.exceptions import (
    PermissionAlreadyExistsException,
    PermissionNotFoundException,
)
from stark.models.permission import Permission
from stark.repositories.permission_repository import PermissionRepository
from stark.schemas.permission import (
    PermissionCreate,
    PermissionUpdate,
)


def get_permissions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):
    repository = PermissionRepository(db)

    permissions = repository.list_all(
        skip,
        limit,
    )

    total = repository.count()

    return {
        "items": permissions,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


def create_permission(
    db: Session,
    data: PermissionCreate,
):
    repository = PermissionRepository(db)

    existing = repository.get_by_name(
        data.name,
    )

    if existing is not None:
        raise PermissionAlreadyExistsException()

    permission = Permission(
        name=data.name,
        description=data.description,
    )

    return repository.save(permission)


def update_permission(
    db: Session,
    permission_id: int,
    data: PermissionUpdate,
):
    repository = PermissionRepository(db)

    permission = repository.get_by_id(
        permission_id,
    )

    if permission is None:
        raise PermissionNotFoundException()

    if data.name is not None and data.name != permission.name:
        existing = repository.get_by_name(
            data.name,
        )

        if existing is not None:
            raise PermissionAlreadyExistsException()

        permission.name = data.name

    if data.description is not None:
        permission.description = data.description

    return repository.update(permission)


def delete_permission(
    db: Session,
    permission_id: int,
):
    repository = PermissionRepository(db)

    permission = repository.get_by_id(
        permission_id,
    )

    if permission is None:
        raise PermissionNotFoundException()

    repository.delete(permission)
