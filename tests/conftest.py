import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from stark.core.database import Base, get_db
from stark.core.security import create_access_token, hash_password
from stark.main import app
from stark.models.user import User, UserRole
from stark.services.permission_service import create_default_permissions
from stark.services.role_permission_service import create_default_role_permissions

TEST_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/stark_test"


engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    create_default_permissions(db)
    create_default_role_permissions(db)

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session):
    user = User(
        name="Administrador",
        email="admin@test.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.ADMIN,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def admin_token(admin_user):
    return create_access_token(
        {
            "sub": str(admin_user.id),
        }
    )


@pytest.fixture
def user_data():
    return {
        "name": "Yago",
        "email": "yago@example.com",
        "password": "123456",
    }


@pytest.fixture
def regular_user(client, user_data):

    response = client.post(
        "/users/",
        json=user_data,
    )

    assert response.status_code == 201

    return user_data


@pytest.fixture
def login_response(client, regular_user):

    response = client.post(
        "/auth/login",
        data={
            "username": regular_user["email"],
            "password": regular_user["password"],
        },
    )

    assert response.status_code == 200

    return response


@pytest.fixture
def regular_user_db(db_session):

    user = User(
        name="Usuário",
        email="user@test.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.USER,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user
