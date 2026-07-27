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


def test_admin_can_view_audit_logs(
    client,
    admin_token,
):
    response = client.get(
        "/admin/audit-logs",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_deactivate_user_creates_audit_log(
    client,
    admin_token,
    db_session,
):
    from stark.core.security import hash_password
    from stark.models.audit_log import AuditLog
    from stark.models.user import User, UserRole

    user = User(
        name="Usuário Teste",
        email="teste@example.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.USER,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = client.patch(
        f"/admin/users/{user.id}/deactivate",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    logs = db_session.query(AuditLog).all()

    assert len(logs) == 1
    assert logs[0].action == "deactivate_user"
    assert logs[0].target_id == user.id
