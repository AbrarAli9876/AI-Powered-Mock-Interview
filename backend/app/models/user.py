from __future__ import annotations

from sqlalchemy import Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.user_role import UserRole
from app.models.base import Base
from app.models.mixins import TimestampMixin


class User(TimestampMixin, Base):
    """
    Database model for application users.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
            native_enum=False,
            length=20,
            name="user_role_enum",
        ),
        default=UserRole.USER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    interview_sessions: Mapped[list["InterviewSession"]] = relationship(
        "InterviewSession",
        back_populates="user",
    )

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, "
            f"email='{self.email}', "
            f"role='{self.role.value}')>"
        )