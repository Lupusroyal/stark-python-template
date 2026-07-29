from sqlalchemy.orm import Session

from stark.models.permission import Permission
from stark.repositories.permission_repository import PermissionRepository
from stark.repositories.role_permission_repository import (
    RolePermissionRepository,
)

DEFAULT_PERMISSIONS = [
    {
        "name": "users.read",
        "description": "Visualizar usuários",
    },
    {
        "name": "users.update",
        "description": "Atualizar usuários",
    },
    {
        "name": "users.delete",
        "description": "Excluir usuários",
    },
    {
        "name": "audit.read",
        "description": "Visualizar logs de auditoria",
    },
    {
        "name": "permissions.read",
        "description": "Visualizar permissões",
    },
    {
        "name": "permissions.create",
        "description": "Criar permissões",
    },
    {
        "name": "permissions.update",
        "description": "Atualizar permissões",
    },
    {
        "name": "permissions.delete",
        "description": "Excluir permissões",
    },
]


def create_default_permissions(db: Session):
    repository = PermissionRepository(db)

    for permission_data in DEFAULT_PERMISSIONS:
        exists = repository.get_by_name(
            permission_data["name"],
        )

        if not exists:
            permission = Permission(**permission_data)

            repository.save(permission)


def has_permission(
    db: Session,
    role: str,
    permission_name: str,
) -> bool:
    permission_repository = PermissionRepository(db)
    role_permission_repository = RolePermissionRepository(db)

    permission = permission_repository.get_by_name(
        permission_name,
    )

    if permission is None:
        return False

    role_permission = role_permission_repository.get_role_permission(
        role,
        permission.id,
    )

    return role_permission is not None
