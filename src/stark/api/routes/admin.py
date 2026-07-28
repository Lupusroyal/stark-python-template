from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from stark.core.database import get_db
from stark.core.exceptions import UserNotFoundException
from stark.core.permissions import Permissions
from stark.dependencies.pagination import PaginationParams
from stark.dependencies.permissions import (
    require_permission,
)
from stark.models.user import User
from stark.schemas.pagination import PaginatedResponse
from stark.schemas.permission import PermissionResponse
from stark.schemas.user import (
    AuditLogResponse,
    UserAdminResponse,
    UserRoleUpdate,
)
from stark.services.audit_service import (
    create_audit_log,
    get_audit_logs,
)
from stark.services.permission_crud_service import get_permissions
from stark.services.user_service import (
    activate_user,
    deactivate_user,
    get_user_by_id,
    get_users,
    update_user_role,
)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get(
    "/users",
    response_model=PaginatedResponse[UserAdminResponse],
)
def list_users_admin(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission(Permissions.USERS_READ)),
):
    return get_users(
        db,
        pagination.skip,
        pagination.limit,
    )


@router.get(
    "/users/{user_id}",
    response_model=UserAdminResponse,
)
def get_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission(Permissions.USERS_READ)),
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise UserNotFoundException()

    return user


@router.patch(
    "/users/{user_id}/activate",
    response_model=UserAdminResponse,
)
def activate_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission(Permissions.USERS_UPDATE)),
):
    user = activate_user(
        db,
        user_id,
    )

    if user is None:
        raise UserNotFoundException()

    create_audit_log(
        db,
        admin.id,
        "activate_user",
        user.id,
    )

    return user


@router.patch(
    "/users/{user_id}/deactivate",
    response_model=UserAdminResponse,
)
def deactivate_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission(Permissions.USERS_UPDATE)),
):
    user = deactivate_user(
        db,
        user_id,
    )

    if user is None:
        raise UserNotFoundException()

    create_audit_log(
        db,
        admin.id,
        "deactivate_user",
        user.id,
    )

    return user


@router.patch(
    "/users/{user_id}/role",
    response_model=UserAdminResponse,
)
def change_user_role(
    user_id: int,
    data: UserRoleUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission(Permissions.USERS_UPDATE)),
):
    existing_user = get_user_by_id(
        db,
        user_id,
    )

    if existing_user is None:
        raise UserNotFoundException()

    old_role = existing_user.role

    user = update_user_role(
        db,
        user_id,
        data.role,
    )

    if user is None:
        raise UserNotFoundException()

    create_audit_log(
        db,
        admin.id,
        "change_role",
        user.id,
        details={
            "old_role": old_role,
            "new_role": data.role,
        },
    )

    return user


@router.get(
    "/permissions",
    response_model=PaginatedResponse[PermissionResponse],
)
def list_permissions(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission(Permissions.PERMISSIONS_READ)),
):
    return get_permissions(
        db,
        pagination.skip,
        pagination.limit,
    )


@router.get(
    "/audit-logs",
    response_model=list[AuditLogResponse],
)
@router.get(
    "/audit-logs",
    response_model=PaginatedResponse[AuditLogResponse],
)
def list_audit_logs(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission(Permissions.AUDIT_READ)),
):
    return get_audit_logs(
        db,
        pagination.skip,
        pagination.limit,
    )
