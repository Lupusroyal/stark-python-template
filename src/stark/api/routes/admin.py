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
from stark.repositories.permission_repository import PermissionRepository
from stark.schemas.audit import AuditLogResponse
from stark.schemas.error import ErrorResponse
from stark.schemas.pagination import PaginatedResponse
from stark.schemas.permission import (
    PermissionCreate,
    PermissionResponse,
    PermissionUpdate,
)
from stark.schemas.user import (
    UserAdminResponse,
    UserRoleUpdate,
)
from stark.services.audit_service import (
    create_audit_log,
    get_audit_logs,
)
from stark.services.permission_crud_service import (
    create_permission,
    delete_permission,
    get_permissions,
    update_permission,
)
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
    summary="Listar usuários",
    description="Retorna uma lista paginada de usuários.",
    responses={
        200: {"description": "Lista de usuários"},
        401: {
            "model": ErrorResponse,
            "description": "Não autenticado",
        },
        403: {
            "model": ErrorResponse,
            "description": "Permissão insuficiente",
        },
    },
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
    summary="Buscar usuário",
    description="Retorna os dados de um usuário específico.",
    responses={
        200: {"description": "Usuário encontrado"},
        401: {
            "model": ErrorResponse,
            "description": "Não autenticado",
        },
        403: {
            "model": ErrorResponse,
            "description": "Permissão insuficiente",
        },
        404: {
            "model": ErrorResponse,
            "description": "Usuário não encontrado",
        },
    },
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
    summary="Ativar usuário",
    description="Ativa um usuário desativado.",
    responses={
        200: {"description": "Usuário ativado"},
        401: {
            "model": ErrorResponse,
            "description": "Não autenticado",
        },
        403: {
            "model": ErrorResponse,
            "description": "Permissão insuficiente",
        },
        404: {
            "model": ErrorResponse,
            "description": "Usuário não encontrado",
        },
    },
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
    summary="Desativar usuário",
    description="Desativa um usuário.",
    responses={
        200: {"description": "Usuário desativado"},
        401: {
            "model": ErrorResponse,
            "description": "Não autenticado",
        },
        403: {
            "model": ErrorResponse,
            "description": "Permissão insuficiente",
        },
        404: {
            "model": ErrorResponse,
            "description": "Usuário não encontrado",
        },
    },
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
    summary="Alterar papel do usuário",
    description="Altera o papel (role) de um usuário.",
    responses={
        200: {"description": "Role atualizada"},
        401: {
            "model": ErrorResponse,
            "description": "Não autenticado",
        },
        403: {
            "model": ErrorResponse,
            "description": "Permissão insuficiente",
        },
        404: {
            "model": ErrorResponse,
            "description": "Usuário não encontrado",
        },
    },
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
    summary="Listar permissões",
    description="Retorna uma lista paginada de permissões cadastradas.",
    responses={
        200: {"description": "Lista de permissões"},
        401: {
            "model": ErrorResponse,
            "description": "Não autenticado",
        },
        403: {
            "model": ErrorResponse,
            "description": "Permissão insuficiente",
        },
    },
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


@router.post(
    "/permissions",
    response_model=PermissionResponse,
    status_code=201,
    summary="Criar permissão",
    description="Cria uma nova permissão para utilização no sistema de RBAC.",
    responses={
        201: {"description": "Permissão criada"},
        401: {
            "model": ErrorResponse,
            "description": "Não autenticado",
        },
        403: {
            "model": ErrorResponse,
            "description": "Permissão insuficiente",
        },
        409: {
            "model": ErrorResponse,
            "description": "Permissão já existe",
        },
    },
)
def create_permission_admin(
    data: PermissionCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission(Permissions.PERMISSIONS_CREATE)),
):
    permission = create_permission(
        db,
        data,
    )

    create_audit_log(
        db,
        admin.id,
        "create_permission",
        permission.id,
        details={
            "name": permission.name,
        },
    )

    return permission


@router.put(
    "/permissions/{permission_id}",
    response_model=PermissionResponse,
    summary="Atualizar permissão",
    description="Atualiza o nome e/ou descrição de uma permissão.",
    responses={
        200: {"description": "Permissão atualizada"},
        401: {
            "model": ErrorResponse,
            "description": "Não autenticado",
        },
        403: {
            "model": ErrorResponse,
            "description": "Permissão insuficiente",
        },
        404: {
            "model": ErrorResponse,
            "description": "Permissão não encontrada",
        },
        409: {
            "model": ErrorResponse,
            "description": "Permissão já existe",
        },
    },
)
def update_permission_admin(
    permission_id: int,
    data: PermissionUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_permission(Permissions.PERMISSIONS_UPDATE)),
):
    permission = update_permission(
        db,
        permission_id,
        data,
    )

    create_audit_log(
        db,
        admin.id,
        "update_permission",
        permission.id,
        details={
            "name": permission.name,
        },
    )

    return permission


@router.delete(
    "/permissions/{permission_id}",
    status_code=204,
    summary="Excluir permissão",
    description="Remove uma permissão do sistema.",
    responses={
        204: {"description": "Permissão removida"},
        401: {
            "model": ErrorResponse,
            "description": "Não autenticado",
        },
        403: {
            "model": ErrorResponse,
            "description": "Permissão insuficiente",
        },
        404: {
            "model": ErrorResponse,
            "description": "Permissão não encontrada",
        },
    },
)
def delete_permission_admin(
    permission_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(
        require_permission(Permissions.PERMISSIONS_DELETE),
    ),
):
    repository = PermissionRepository(db)

    permission = repository.get_by_id(
        permission_id,
    )

    delete_permission(
        db,
        permission_id,
    )

    if permission is not None:
        create_audit_log(
            db,
            admin.id,
            "delete_permission",
            permission.id,
            details={
                "name": permission.name,
            },
        )


@router.get(
    "/audit-logs",
    response_model=PaginatedResponse[AuditLogResponse],
    summary="Listar auditoria",
    description="Retorna uma lista paginada dos registros de auditoria do sistema.",
    responses={
        200: {"description": "Lista de auditoria"},
        401: {
            "model": ErrorResponse,
            "description": "Não autenticado",
        },
        403: {
            "model": ErrorResponse,
            "description": "Permissão insuficiente",
        },
    },
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
