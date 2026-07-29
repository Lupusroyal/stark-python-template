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
