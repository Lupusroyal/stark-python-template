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
