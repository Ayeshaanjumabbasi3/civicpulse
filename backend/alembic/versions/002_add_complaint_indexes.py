"""add complaint query indexes"""

from alembic import op

revision = "002_add_complaint_indexes"
down_revision = "001_create_complaints"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "ix_complaints_status_priority", "complaints", ["status", "priority"]
    )
    op.create_index("ix_complaints_created_at", "complaints", ["created_at"])


def downgrade():
    op.drop_index("ix_complaints_created_at", table_name="complaints")
    op.drop_index("ix_complaints_status_priority", table_name="complaints")
