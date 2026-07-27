"""add audit log details

Revision ID: 1002f250082e
Revises: e217e9a4054d
Create Date: 2026-07-27 19:20:42.185434

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1002f250082e"
down_revision: str | Sequence[str] | None = "e217e9a4054d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "audit_logs",
        sa.Column("details", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "audit_logs",
        "details",
    )
