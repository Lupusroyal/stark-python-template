from fastapi.testclient import TestClient

from stark.main import app

client = TestClient(app)


def test_create_user(client):

    response = client.post(
        "/users/",
        json={
            "name": "Yago",
            "email": "yago@example.com",
            "password": "123456",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "yago@example.com"
