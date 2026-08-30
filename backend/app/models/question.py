from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.question_difficulty import QuestionDifficulty
from app.models.base import Base
from app.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from app.models.interview_answer import InterviewAnswer
    from app.models.topic import Topic


class Question(TimestampMixin, Base):
    """
    Database model for interview questions.
    """

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
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
            name="question_difficulty_enum",
        ),
        nullable=False,
    )

    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    expected_answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    topic: Mapped["Topic"] = relationship(
        "Topic",
        back_populates="questions",
    )

    answers: Mapped[list["InterviewAnswer"]] = relationship(
        "InterviewAnswer",
        back_populates="question",
    )

    def __repr__(self) -> str:
        return (
            f"<Question("
            f"id={self.id}, "
            f"topic_id={self.topic_id}, "
            f"difficulty='{self.difficulty.value}'"
            f")>"
        )