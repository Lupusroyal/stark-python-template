from stark.core.security import hash_password
from stark.models.user import User
from stark.repositories.user_repository import UserRepository


def test_user_repository_save_and_get_by_email(
    db_session,
):
    repository = UserRepository(db_session)

    user = User(
        name="Repository Test",
        email="repository@test.com",
        hashed_password=hash_password("123456"),
        is_active=True,
    )

    saved_user = repository.save(user)

    found_user = repository.get_by_email(
        "repository@test.com",
    )

    assert saved_user.id == found_user.id
    assert found_user.email == "repository@test.com"


from stark.models.audit_log import AuditLog
from stark.models.permission import Permission
from stark.models.role_permission import RolePermission
from stark.repositories.audit_repository import AuditRepository
from stark.repositories.permission_repository import PermissionRepository
from stark.repositories.role_permission_repository import (
    RolePermissionRepository,
)


def test_permission_repository(
    db_session,
):
    repository = PermissionRepository(db_session)

    permission = Permission(
        name="test.permission",
        description="Permissão de teste",
    )

    saved = repository.save(permission)

    found = repository.get_by_name(
        "test.permission",
    )

    assert saved.id == found.id
    assert found.name == "test.permission"


def test_role_permission_repository(
    db_session,
):
    permission_repository = PermissionRepository(
        db_session,
    )

    role_repository = RolePermissionRepository(
        db_session,
    )

    permission = Permission(
        name="repository.role.test",
        description="Teste role permission",
    )

    permission_repository.save(permission)

    role_permission = RolePermission(
        role="admin",
        permission_id=permission.id,
    )

    saved = role_repository.save(role_permission)

    found = role_repository.get_role_permission(
        "admin",
        permission.id,
    )

    assert saved.id == found.id
    assert found.role == "admin"


def test_audit_repository(
    db_session,
):
    repository = AuditRepository(db_session)

    audit = AuditLog(
        actor_id=1,
        action="test_action",
        target_id=1,
    )

    saved = repository.save(audit)

    logs = repository.list_all()

    assert saved.id in [log.id for log in logs]
