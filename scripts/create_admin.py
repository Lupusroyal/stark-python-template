from getpass import getpass

from stark.core.database import SessionLocal
from stark.core.security import hash_password
from stark.models.user import User, UserRole
from stark.repositories.user_repository import UserRepository


def main():
    db = SessionLocal()

    try:
        name = input("Nome do administrador: ")
        email = input("Email: ")
        password = getpass("Senha: ")

        repository = UserRepository(db)

        existing = repository.get_by_email(email)

        if existing:
            print("Usuário já existe.")
            return

        admin = User(
            name=name,
            email=email,
            hashed_password=hash_password(password),
            role=UserRole.ADMIN,
            is_active=True,
        )

        repository.save(admin)

        print("Administrador criado com sucesso!")

    finally:
        db.close()


if __name__ == "__main__":
    main()
