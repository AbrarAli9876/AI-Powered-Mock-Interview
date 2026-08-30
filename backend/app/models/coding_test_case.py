from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from app.models.coding_question import CodingQuestion


class CodingTestCase(TimestampMixin, Base):
    """
    Database model representing a test case
    used to evaluate a coding question.
    """

    __tablename__ = "coding_test_cases"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    coding_question_id: Mapped[int] = mapped_column(
        ForeignKey("coding_questions.id"),
        nullable=False,
        index=True,
    )

    input_data: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    expected_output: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    execution_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    coding_question: Mapped["CodingQuestion"] = relationship(
        "CodingQuestion",
        back_populates="test_cases",
    )

    def __repr__(self) -> str:
        return (
            f"<CodingTestCase("
            f"id={self.id}, "
            f"coding_question_id={self.coding_question_id}, "
            f"is_hidden={self.is_hidden}"
            f")>"
        )