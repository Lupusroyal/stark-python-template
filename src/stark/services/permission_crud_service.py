from sqlalchemy.orm import Session

from stark.repositories.permission_repository import PermissionRepository


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
