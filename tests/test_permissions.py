from stark.services.permission_service import has_permission


def test_admin_has_delete_permission(
    db_session,
    admin_user,
):
    result = has_permission(
        db_session,
        admin_user.role,
        "users.delete",
    )

    assert result is True


def test_regular_user_does_not_have_delete_permission(
    db_session,
    regular_user_db,
):
    result = has_permission(
        db_session,
        regular_user_db.role,
        "users.delete",
    )

    assert result is False


def test_user_cannot_delete_without_permission(
    client,
    regular_user,
    login_response,
):

    access_token = login_response.json()["access_token"]

    response = client.delete(
        "/users/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["error"] == "PERMISSION_DENIED"
    assert data["message"] == "Permissão insuficiente"


def test_admin_can_delete_account(
    client,
    admin_user,
    admin_token,
):

    response = client.delete(
        "/users/me",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Usuário desativado com sucesso"


def test_user_can_read_with_permission(
    client,
    regular_user_db,
    login_response,
):

    access_token = login_response.json()["access_token"]

    response = client.get(
        f"/users/{regular_user_db.id}",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == regular_user_db.email


def test_admin_can_read_user(
    client,
    admin_user,
    admin_token,
):

    response = client.get(
        f"/users/{admin_user.id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == admin_user.email


def test_user_cannot_update_other_user_without_permission(
    client,
    regular_user,
    login_response,
):

    access_token = login_response.json()["access_token"]

    response = client.put(
        "/users/999",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "name": "Tentativa",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["error"] == "PERMISSION_DENIED"
    assert data["message"] == "Permissão insuficiente"


def test_admin_can_update_user(
    client,
    admin_user,
    admin_token,
):

    response = client.put(
        f"/users/{admin_user.id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "name": "Administrador Atualizado",
            "email": admin_user.email,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Administrador Atualizado"
