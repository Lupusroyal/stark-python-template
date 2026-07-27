from stark.core.database import SessionLocal
from stark.services.role_permission_service import (
    create_default_role_permissions,
)


def main():
    db = SessionLocal()

    try:
        create_default_role_permissions(db)
        print("Relacionamentos criados com sucesso!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
