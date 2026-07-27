from sqlalchemy.orm import Session

from stark.models.permission import Permission

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
]


def create_default_permissions(db: Session):
    for permission_data in DEFAULT_PERMISSIONS:
        exists = (
            db.query(Permission)
            .filter(Permission.name == permission_data["name"])
            .first()
        )

        if not exists:
            permission = Permission(**permission_data)
            db.add(permission)

    db.commit()
