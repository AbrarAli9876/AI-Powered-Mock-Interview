from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.coding_language import CodingLanguage
from app.enums.question_difficulty import QuestionDifficulty
from app.models.base import Base
from app.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from app.models.coding_test_case import CodingTestCase
    from app.models.topic import Topic


class CodingQuestion(TimestampMixin, Base):
    """
    Database model for coding interview questions.
    """

    __tablename__ = "coding_questions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        nullable=False,
        index=True,
    )

    language: Mapped[CodingLanguage] = mapped_column(
        Enum(
            CodingLanguage,
            values_callable=lambda enum_cls: [
                member.value
                for member in enum_cls
            ],
            native_enum=False,
            length=20,
            name="coding_language_enum",
        ),
        nullable=False,
        index=True,
    )

    difficulty: Mapped[QuestionDifficulty] = mapped_column(
        Enum(
            QuestionDifficulty,
            values_callable=lambda enum_cls: [
                member.value
                for member in enum_cls
            ],
            native_enum=False,
            length=20,
            name="coding_question_difficulty_enum",
        ),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    problem_statement: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    input_format: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    output_format: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    constraints: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    examples: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    starter_code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # =========================================================
    # HINTS
    # =========================================================

    hint_1: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    hint_2: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # =========================================================
    # RELATIONSHIPS
    # =========================================================

    topic: Mapped["Topic"] = relationship(
        "Topic",
        back_populates="coding_questions",
    )

    test_cases: Mapped[list["CodingTestCase"]] = relationship(
        "CodingTestCase",
        back_populates="coding_question",
        cascade="all, delete-orphan",
        order_by="CodingTestCase.execution_order",
    )

    def __repr__(self) -> str:
        return (
            f"<CodingQuestion("
            f"id={self.id}, "
            f"topic_id={self.topic_id}, "
            f"language='{self.language.value}', "
            f"difficulty='{self.difficulty.value}'"
            f")>"
        )