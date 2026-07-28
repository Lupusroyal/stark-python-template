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
    data = response.json()

    assert isinstance(data, dict)
    assert "items" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert isinstance(data["items"], list)


def test_user_cannot_view_audit_logs(
    client,
    db_session,
):
    from stark.core.security import hash_password
    from stark.models.user import User, UserRole

    user = User(
        name="Usuário Comum",
        email="common@example.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.USER,
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "common@example.com",
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


def test_change_user_role_creates_audit_log(
    client,
    admin_token,
    db_session,
):
    from stark.core.security import hash_password
    from stark.models.audit_log import AuditLog
    from stark.models.user import User, UserRole

    user = User(
        name="Usuário Role Teste",
        email="role@example.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.USER,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = client.patch(
        f"/admin/users/{user.id}/role",
        json={
            "role": "admin",
        },
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    logs = db_session.query(AuditLog).all()

    assert len(logs) == 1
    assert logs[0].action == "change_role"
    assert logs[0].target_id == user.id
    assert logs[0].details["old_role"] == "user"
    assert logs[0].details["new_role"] == "admin"


def test_user_cannot_deactivate_user(
    client,
    db_session,
):
    from stark.core.security import hash_password
    from stark.models.user import User, UserRole

    user = User(
        name="Usuário Comum",
        email="common2@example.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.USER,
    )

    target = User(
        name="Usuário Alvo",
        email="target@example.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.USER,
    )

    db_session.add_all([user, target])
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "common2@example.com",
            "password": "123456",
        },
    )

    token = response.json()["access_token"]

    response = client.patch(
        f"/admin/users/{target.id}/deactivate",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_user_cannot_change_user_role(
    client,
    db_session,
):
    from stark.core.security import hash_password
    from stark.models.user import User, UserRole

    user = User(
        name="Usuário Sem Permissão",
        email="roleblock@example.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.USER,
    )

    target = User(
        name="Usuário Alvo Role",
        email="targetrole@example.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.USER,
    )

    db_session.add_all([user, target])
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "roleblock@example.com",
            "password": "123456",
        },
    )

    token = response.json()["access_token"]

    response = client.patch(
        f"/admin/users/{target.id}/role",
        json={
            "role": "admin",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_user_cannot_activate_user(
    client,
    db_session,
):
    from stark.core.security import hash_password
    from stark.models.user import User, UserRole

    user = User(
        name="Usuário Sem Permissão Activate",
        email="activateblock@example.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.USER,
    )

    target = User(
        name="Usuário Desativado",
        email="inactive@example.com",
        hashed_password=hash_password("123456"),
        is_active=False,
        role=UserRole.USER,
    )

    db_session.add_all([user, target])
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "activateblock@example.com",
            "password": "123456",
        },
    )

    token = response.json()["access_token"]

    response = client.patch(
        f"/admin/users/{target.id}/activate",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_admin_can_list_permissions(
    client,
    admin_token,
):
    response = client.get(
        "/admin/permissions",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, dict)
    assert "items" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert isinstance(data["items"], list)


def test_user_cannot_list_permissions(
    client,
    db_session,
):
    from stark.core.security import hash_password
    from stark.models.user import User, UserRole

    user = User(
        name="Usuário Comum",
        email="userpermissions@example.com",
        hashed_password=hash_password("123456"),
        is_active=True,
        role=UserRole.USER,
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "userpermissions@example.com",
            "password": "123456",
        },
    )

    token = response.json()["access_token"]

    response = client.get(
        "/admin/permissions",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403
