import hashlib
import secrets
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from urllib.parse import quote

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import settings
from app.models.password_reset_token import PasswordResetToken
from app.models.user import User
from app.utils.security import hash_password


RESET_TOKEN_TTL_MINUTES = 15

GENERIC_REQUEST_MESSAGE = (
    "If an account exists for that email, password-reset instructions will be sent."
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _smtp_is_configured() -> bool:
    return bool(
        settings.SMTP_HOST
        and settings.SMTP_PORT
        and settings.SMTP_USERNAME
        and settings.SMTP_PASSWORD
        and settings.SMTP_FROM_EMAIL
    )


def _send_reset_email(email: str, reset_url: str) -> None:
    message = EmailMessage()

    message["Subject"] = "Reset your AI Mock Interview password"
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = email

    message.set_content(
        "We received a request to reset your AI Mock Interview account password.\n\n"
        f"Use this link within {RESET_TOKEN_TTL_MINUTES} minutes "
        "to choose a new password:\n"
        f"{reset_url}\n\n"
        "This link can only be used once. "
        "If you did not request this, you can ignore this email."
    )

    message.add_alternative(
        "<p>We received a request to reset your AI Mock Interview account password.</p>"
        f"<p><a href=\"{reset_url}\">Reset your password</a>. "
        f"This link expires in {RESET_TOKEN_TTL_MINUTES} minutes "
        "and can only be used once.</p>"
        "<p>If you did not request this, you can ignore this email.</p>",
        subtype="html",
    )

    with smtplib.SMTP(
        settings.SMTP_HOST,
        settings.SMTP_PORT,
        timeout=15,
    ) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(
            settings.SMTP_USERNAME,
            settings.SMTP_PASSWORD,
        )

        server.send_message(message)


class PasswordResetService:
    def __init__(self, db: Session):
        self.db = db

    def request_reset(self, email: str) -> dict[str, str]:
        # Ensure SMTP is configured before processing requests.
        if not _smtp_is_configured():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    "Password-reset email is not configured. "
                    "Set the SMTP settings on the backend."
                ),
            )

        normalized_email = email.strip().lower()

        user = (
            self.db.query(User)
            .filter(func.lower(User.email) == normalized_email)
            .first()
        )

        # Do not reveal whether an email address is registered.
        if user is None or not user.is_active:
            return {"message": GENERIC_REQUEST_MESSAGE}

        now = _utc_now()

        # Invalidate older unused links for this account.
        (
            self.db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.used_at.is_(None),
            )
            .update(
                {PasswordResetToken.used_at: now},
                synchronize_session=False,
            )
        )

        # Generate a secure random token.
        raw_token = secrets.token_urlsafe(32)

        token_record = PasswordResetToken(
            user_id=user.id,
            token_hash=_hash_token(raw_token),
            expires_at=now + timedelta(
                minutes=RESET_TOKEN_TTL_MINUTES
            ),
        )

        self.db.add(token_record)

        try:
            self.db.flush()

            reset_url = (
                f"{settings.FRONTEND_BASE_URL.rstrip('/')}"
                f"/reset-password?token={quote(raw_token)}"
            )

            _send_reset_email(
                user.email,
                reset_url,
            )

            self.db.commit()

        except Exception as exc:
            self.db.rollback()

            if isinstance(exc, HTTPException):
                raise

            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=(
                    "Unable to send the password-reset email. "
                    "Check the backend SMTP configuration and try again."
                ),
            ) from exc

        return {"message": GENERIC_REQUEST_MESSAGE}

    def reset_password(
        self,
        token: str,
        new_password: str,
    ) -> dict[str, str]:
        # Compare the submitted token's hash with the stored hash.
        token_record = (
            self.db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.token_hash == _hash_token(token)
            )
            .first()
        )

        now = _utc_now()

        if token_record is None or token_record.used_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "This password-reset link is invalid or has already "
                    "been used. Request a new link."
                ),
            )

        expires_at = token_record.expires_at

        # Some database drivers return naive datetimes.
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at <= now:
            token_record.used_at = now
            self.db.commit()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "This password-reset link has expired. "
                    "Request a new link."
                ),
            )

        user = (
            self.db.query(User)
            .filter(User.id == token_record.user_id)
            .first()
        )

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "This password-reset link is invalid. "
                    "Request a new link."
                ),
            )

        # Use the project's existing password-hashing utility.
        user.password_hash = hash_password(new_password)

        # Mark the current token as used.
        token_record.used_at = now

        # Invalidate every other outstanding reset link for this user.
        (
            self.db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.id != token_record.id,
                PasswordResetToken.used_at.is_(None),
            )
            .update(
                {PasswordResetToken.used_at: now},
                synchronize_session=False,
            )
        )

        self.db.commit()

        return {
            "message": (
                "Your password has been reset successfully. "
                "You can now sign in."
            )
        }