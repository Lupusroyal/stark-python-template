"""use user role enum

Revision ID: d7a10a777273
Revises: 191044c7806c
Create Date: 2026-07-25 19:08:17.088397

"""

from collections.abc import Sequence

revision: str = "d7a10a777273"
down_revision: str | Sequence[str] | None = "191044c7806c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
