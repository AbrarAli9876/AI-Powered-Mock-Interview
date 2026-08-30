"""add coding questions

Revision ID: 79c3f79f4cbf
Revises: fd24c1c1c69a
Create Date: 2026-08-30 15:31:57.007247

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "79c3f79f4cbf"
down_revision: Union[str, Sequence[str], None] = "fd24c1c1c69a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create coding_questions table."""

    op.create_table(
        "coding_questions",

        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),

        sa.Column(
            "topic_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "language",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "difficulty",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "title",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "problem_statement",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "input_format",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "output_format",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "constraints",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "examples",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "starter_code",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["topic_id"],
            ["topics.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_coding_questions_topic_id"),
        "coding_questions",
        ["topic_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_coding_questions_language"),
        "coding_questions",
        ["language"],
        unique=False,
    )

    op.create_index(
        op.f("ix_coding_questions_difficulty"),
        "coding_questions",
        ["difficulty"],
        unique=False,
    )


def downgrade() -> None:
    """Drop coding_questions table."""

    op.drop_index(
        op.f("ix_coding_questions_difficulty"),
        table_name="coding_questions",
    )

    op.drop_index(
        op.f("ix_coding_questions_language"),
        table_name="coding_questions",
    )

    op.drop_index(
        op.f("ix_coding_questions_topic_id"),
        table_name="coding_questions",
    )

    op.drop_table("coding_questions")