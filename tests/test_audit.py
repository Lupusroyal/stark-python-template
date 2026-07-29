from stark.models.audit_log import AuditLog


def test_admin_delete_creates_audit_log(
    client,
    admin_user,
    admin_token,
    db_session,
):

    response = client.delete(
        "/users/me",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    audit = (
        db_session.query(AuditLog)
        .filter(
            AuditLog.action == "USER_DELETE",
            AuditLog.actor_id == admin_user.id,
        )
        .first()
    )

    assert audit is not None
    assert audit.target_id == admin_user.id


def test_admin_update_creates_audit_log(
    client,
    admin_user,
    admin_token,
    db_session,
):

    response = client.put(
        f"/users/{admin_user.id}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "name": "Administrador Alterado",
            "email": admin_user.email,
        },
    )

    assert response.status_code == 200

    audit = (
        db_session.query(AuditLog)
        .filter(
            AuditLog.action == "USER_UPDATE",
            AuditLog.actor_id == admin_user.id,
        )
        .first()
    )

    assert audit is not None
    assert audit.target_id == admin_user.id
