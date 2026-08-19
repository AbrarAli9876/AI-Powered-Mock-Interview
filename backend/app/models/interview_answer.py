from __future__ import annotations

from sqlalchemy import ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin


class InterviewAnswer(TimestampMixin, Base):
    """
    Database model representing an answer given
    by a user during an interview session.
    """

    __tablename__ = "interview_answers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("interview_sessions.id"),
        nullable=False,
        index=True,
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"),
        nullable=False,
        index=True,
    )

    answer_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    overall_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    technical_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    communication_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    relevance_score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    strengths: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    improvements: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    session: Mapped["InterviewSession"] = relationship(
        "InterviewSession",
        back_populates="answers",
    )

    question: Mapped["Question"] = relationship(
        "Question",
    )

    def __repr__(self) -> str:
        return (
            f"<InterviewAnswer("
            f"id={self.id}, "
            f"session_id={self.session_id}, "
            f"question_id={self.question_id}"
            f")>"
        )