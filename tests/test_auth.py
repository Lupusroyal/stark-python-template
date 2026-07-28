def test_login(client):

    client.post(
        "/users/",
        json={
            "name": "Yago",
            "email": "yago@example.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "yago@example.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in data


def test_refresh_token_rotation(client):

    client.post(
        "/users/",
        json={
            "name": "Yago",
            "email": "yago@example.com",
            "password": "123456",
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "yago@example.com",
            "password": "123456",
        },
    )

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
