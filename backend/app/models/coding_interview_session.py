from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.coding_language import CodingLanguage
from app.enums.interview_status import InterviewStatus
from app.enums.question_difficulty import QuestionDifficulty
from app.models.base import Base
from app.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from app.models.coding_interview_question import (
        CodingInterviewQuestion,
    )
    from app.models.user import User


class CodingInterviewSession(TimestampMixin, Base):
    """
    Database model representing a coding interview session.
    """

    __tablename__ = "coding_interview_sessions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
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
            name="coding_interview_language_enum",
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
            name="coding_interview_difficulty_enum",
        ),
        nullable=False,
        index=True,
    )

    total_questions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    current_question_number: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    status: Mapped[InterviewStatus] = mapped_column(
        Enum(
            InterviewStatus,
            values_callable=lambda enum_cls: [
                member.value
                for member in enum_cls
            ],
            native_enum=False,
            length=20,
            name="coding_interview_status_enum",
        ),
        default=InterviewStatus.IN_PROGRESS,
        nullable=False,
        index=True,
    )

    overall_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User",
    )

    questions: Mapped[
        list["CodingInterviewQuestion"]
    ] = relationship(
        "CodingInterviewQuestion",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="CodingInterviewQuestion.question_number",
    )

    def __repr__(self) -> str:
        return (
            f"<CodingInterviewSession("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"language='{self.language.value}', "
            f"difficulty='{self.difficulty.value}', "
            f"status='{self.status.value}')>"
        )