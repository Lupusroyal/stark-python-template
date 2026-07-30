from fastapi.testclient import TestClient


class InternalTestError(Exception):
    pass


def test_validation_error_returns_standard_format(
    client: TestClient,
):
    response = client.post(
        "/users",
        json={
            "name": "",
            "email": "email-invalido",
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"] == "VALIDATION_ERROR"
    assert data["message"] == "Dados inválidos"
    assert "details" in data


def test_invalid_credentials_returns_standard_format(
    client,
):
    response = client.post(
        "/auth/login",
        data={
            "username": "naoexiste@example.com",
            "password": "senhaerrada",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["error"] == "INVALID_CREDENTIALS"
    assert data["message"] == "Credenciais inválidas"


def test_permission_denied_returns_standard_format(
    client,
    db_session,
):
    from stark.core.security import hash_password
    from stark.models.user import User, UserRole

    user = User(
        name="Usuário Comum",
        email="error403@example.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.USER,
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "error403@example.com",
            "password": "123456",
        },
    )

    token = response.json()["access_token"]

    response = client.get(
        "/admin/audit-logs",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["error"] == "PERMISSION_DENIED"
    assert data["message"] == "Permissão insuficiente"


def test_internal_server_error_returns_standard_format(
    client,
):
    from fastapi import APIRouter

    from stark.main import app

    router = APIRouter()

    @router.get("/test-error")
    def test_error():
        raise InternalTestError("erro de teste")

    app.include_router(router)

    response = client.get(
        "/test-error",
    )

    assert response.status_code == 500

    data = response.json()

    assert data["error"] == "INTERNAL_SERVER_ERROR"
    assert data["message"] == "Erro interno do servidor"
