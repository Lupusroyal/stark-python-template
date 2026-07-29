def test_login(login_response):

    data = login_response.json()

    assert login_response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_rotation(client, login_response):

    refresh_token = login_response.json()["refresh_token"]

    refresh_response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert refresh_response.status_code == 200

    data = refresh_response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["refresh_token"] != refresh_token


def test_refresh_token_cannot_be_reused(client, login_response):

    refresh_token = login_response.json()["refresh_token"]

    first_refresh = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert first_refresh.status_code == 200

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["error"] == "INVALID_CREDENTIALS"
    assert data["message"] == "Credenciais inválidas"


def test_logout_revokes_refresh_token(client, login_response):

    refresh_token = login_response.json()["refresh_token"]

    logout_response = client.post(
        "/auth/logout",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert logout_response.status_code == 200

    data = logout_response.json()

    assert data["message"] == "Logged out successfully"

    refresh_response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert refresh_response.status_code == 401

    data = refresh_response.json()

    assert data["error"] == "INVALID_CREDENTIALS"
    assert data["message"] == "Credenciais inválidas"
