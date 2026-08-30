from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin


if TYPE_CHECKING:
    from app.models.coding_question import CodingQuestion
    from app.models.interview_session import InterviewSession
    from app.models.question import Question


class Topic(TimestampMixin, Base):
    """
    Database model for interview topics.
    """

    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="topic",
    )

    coding_questions: Mapped[list["CodingQuestion"]] = relationship(
        "CodingQuestion",
        back_populates="topic",
    )

    interview_sessions: Mapped[list["InterviewSession"]] = relationship(
        "InterviewSession",
        back_populates="topic",
    )

    def __repr__(self) -> str:
        return (
            f"<Topic(id={self.id}, name='{self.name}')>"
        )