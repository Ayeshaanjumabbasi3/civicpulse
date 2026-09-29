"""create complaints table"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "001_create_complaints"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute(
        "CREATE TYPE category_enum AS ENUM ('water','electricity','sanitation','roads','streetlights','other')"
    )
    op.execute("CREATE TYPE priority_enum AS ENUM ('high','normal','low')")
    op.execute(
        "CREATE TYPE status_enum AS ENUM ('open','in_progress','resolved','rejected')"
    )
    category = postgresql.ENUM(name="category_enum", create_type=False)
    priority = postgresql.ENUM(name="priority_enum", create_type=False)
    status = postgresql.ENUM(name="status_enum", create_type=False)
    op.create_table(
        "complaints",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("location", sa.String(200), nullable=False),
        sa.Column("reporter_contact", sa.String(), nullable=True),
        sa.Column("category", category, nullable=False),
        sa.Column("priority", priority, nullable=False),
        sa.Column("status", status, server_default="open", nullable=False),
        sa.Column("ai_summary", sa.String(140), nullable=False),
        sa.Column("triaged_by", sa.String(), nullable=False),
        sa.Column("triage_latency_ms", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("complaints")
    op.execute("DROP TYPE status_enum")
    op.execute("DROP TYPE priority_enum")
    op.execute("DROP TYPE category_enum")
