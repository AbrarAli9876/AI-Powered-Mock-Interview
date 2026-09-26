from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from app.models.coding_interview_session import (
        CodingInterviewSession,
    )
    from app.models.coding_question import CodingQuestion


class CodingInterviewQuestion(TimestampMixin, Base):
    """
    Stores the questions selected for a coding interview
    and their order within that interview.
    """

    __tablename__ = "coding_interview_questions"

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

    answered: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    session: Mapped[
        "CodingInterviewSession"
    ] = relationship(
        "CodingInterviewSession",
        back_populates="questions",
    )

    coding_question: Mapped[
        "CodingQuestion"
    ] = relationship(
        "CodingQuestion",
    )

    def __repr__(self) -> str:
        return (
            f"<CodingInterviewQuestion("
            f"id={self.id}, "
            f"session_id={self.session_id}, "
            f"coding_question_id={self.coding_question_id}, "
            f"question_number={self.question_number})>"
        )