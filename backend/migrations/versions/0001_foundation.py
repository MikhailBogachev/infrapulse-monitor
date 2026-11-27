"""Establish the foundation schema revision and expose it to the runtime role."""

from alembic import op

revision = "0001_foundation"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("GRANT SELECT ON TABLE alembic_version TO infrapulse_app")


def downgrade() -> None:
    op.execute("REVOKE SELECT ON TABLE alembic_version FROM infrapulse_app")
