from stark.core.security import hash_password
from stark.models.user import User


def test_admin_can_list_users(client, db_session):

    user = User(
        name="Admin",
        email="admin@example.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role="admin",
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@example.com",
            "password": "123456",
        },
    )

    token = response.json()["access_token"]

    response = client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
