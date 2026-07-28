from sqlalchemy.orm import Session

from stark.models.permission import Permission
from stark.repositories.permission_repository import PermissionRepository

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
