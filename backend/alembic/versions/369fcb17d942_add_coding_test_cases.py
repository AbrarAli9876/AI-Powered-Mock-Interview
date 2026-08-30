"""add coding test cases

Revision ID: 369fcb17d942
Revises: 79c3f79f4cbf
Create Date: 2026-08-30 15:43:08.520799

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "369fcb17d942"

down_revision: Union[str, Sequence[str], None] = "79c3f79f4cbf"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create coding_test_cases table."""

    op.create_table(
        "coding_test_cases",

        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),

        sa.Column(
            "coding_question_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "input_data",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "expected_output",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "is_hidden",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),

        sa.Column(
            "execution_order",
            sa.Integer(),
            nullable=False,
            server_default="0",
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
            ["coding_question_id"],
            ["coding_questions.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_coding_test_cases_coding_question_id"),
        "coding_test_cases",
        ["coding_question_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop coding_test_cases table."""

    op.drop_index(
        op.f("ix_coding_test_cases_coding_question_id"),
        table_name="coding_test_cases",
    )

    op.drop_table("coding_test_cases")