from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.interview_status import InterviewStatus
from app.enums.question_difficulty import QuestionDifficulty
from app.models.base import Base
from app.models.mixins import TimestampMixin


class InterviewSession(TimestampMixin, Base):
    """
    Database model representing an interview session
    attempted by a user.
    """

    __tablename__ = "interview_sessions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
        nullable=False,
    )

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        index=True,
        nullable=False,
    )

    current_question_id: Mapped[int | None] = mapped_column(
        ForeignKey("questions.id"),
        index=True,
        nullable=True,
    )

    starting_difficulty: Mapped[QuestionDifficulty] = mapped_column(
        Enum(
            QuestionDifficulty,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
            native_enum=False,
            length=20,
            name="starting_difficulty_enum",
        ),
        nullable=False,
    )

    current_difficulty: Mapped[QuestionDifficulty] = mapped_column(
        Enum(
            QuestionDifficulty,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
            native_enum=False,
            length=20,
            name="current_difficulty_enum",
        ),
        nullable=False,
    )

    status: Mapped[InterviewStatus] = mapped_column(
        Enum(
            InterviewStatus,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
            native_enum=False,
            length=20,
            name="interview_status_enum",
        ),
        default=InterviewStatus.IN_PROGRESS,
        nullable=False,
    )

    total_questions: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    current_question_number: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    poor_streak: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    strong_streak: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    overall_score: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    # ---------------------------------------------------------
    # Final AI-generated interview report
    # ---------------------------------------------------------

    final_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    final_strengths: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    final_weaknesses: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    technical_assessment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    communication_assessment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    problem_solving_assessment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    final_recommendations: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    user: Mapped["User"] = relationship(
        "User",
        back_populates="interview_sessions",
    )

    topic: Mapped["Topic"] = relationship(
        "Topic",
        back_populates="interview_sessions",
    )

    answers: Mapped[list["InterviewAnswer"]] = relationship(
        "InterviewAnswer",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<InterviewSession("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"topic_id={self.topic_id}, "
            f"difficulty='{self.current_difficulty.value}', "
            f"status='{self.status.value}')>"
        )