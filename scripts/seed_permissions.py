from stark.core.database import SessionLocal
from stark.services.permission_service import create_default_permissions


def main():
    db = SessionLocal()

    try:
        create_default_permissions(db)
        print("Permissões criadas com sucesso!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
