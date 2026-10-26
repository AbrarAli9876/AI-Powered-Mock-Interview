"""add password reset tokens

Revision ID: c21f8a7b4d90
Revises: 727cf1809ce5
Create Date: 2026-10-25
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c21f8a7b4d90"
down_revision: Union[str, Sequence[str], None] = "727cf1809ce5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "password_reset_tokens",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "token_hash",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "used_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )

    op.create_index(
        op.f("ix_password_reset_tokens_user_id"),
        "password_reset_tokens",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        "ix_password_reset_tokens_user_used",
        "password_reset_tokens",
        ["user_id", "used_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_password_reset_tokens_user_used",
        table_name="password_reset_tokens",
    )

    op.drop_index(
        op.f("ix_password_reset_tokens_user_id"),
        table_name="password_reset_tokens",
    )

    op.drop_table("password_reset_tokens")