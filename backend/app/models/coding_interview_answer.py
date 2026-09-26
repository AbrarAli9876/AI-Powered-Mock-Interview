from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from app.models.coding_interview_session import (
        CodingInterviewSession,
    )
    from app.models.coding_interview_question import (
        CodingInterviewQuestion,
    )
    from app.models.coding_question import CodingQuestion


class CodingInterviewAnswer(TimestampMixin, Base):
    """
    Stores a candidate's submitted coding solution.
    """

    __tablename__ = "coding_interview_answers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey(
            "coding_interview_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    coding_interview_question_id: Mapped[int] = mapped_column(
        ForeignKey(
            "coding_interview_questions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    coding_question_id: Mapped[int] = mapped_column(
        ForeignKey(
            "coding_questions.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    question_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    total_test_cases: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    passed_test_cases: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    failed_test_cases: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    session: Mapped[
        "CodingInterviewSession"
    ] = relationship(
        "CodingInterviewSession",
    )

    interview_question: Mapped[
        "CodingInterviewQuestion"
    ] = relationship(
        "CodingInterviewQuestion",
    )

    coding_question: Mapped[
        "CodingQuestion"
    ] = relationship(
        "CodingQuestion",
    )

    def __repr__(self) -> str:
        return (
            f"<CodingInterviewAnswer("
            f"id={self.id}, "
            f"session_id={self.session_id}, "
            f"question_number={self.question_number}, "
            f"success={self.success})>"
        )