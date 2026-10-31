
from datetime import datetime, timedelta, timezone
from typing import Any
import hashlib

import bcrypt
from jose import JWTError, jwt

from app.config import settings


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    """
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against a bcrypt hash.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT access token.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    # Diagnostic: generation configuration
    secret_fingerprint = hashlib.sha256(
        settings.SECRET_KEY.encode("utf-8")
    ).hexdigest()[:12]

    print(
        "[JWT CONFIG] GENERATION:",
        "algorithm =", settings.ALGORITHM,
        "secret fingerprint =", secret_fingerprint,
    )

    # Immediately verify the newly generated token.
    try:
        jwt.decode(
            encoded_jwt,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        print(
            "[JWT CONFIG] Immediate generation verification: SUCCESS"
        )

    except JWTError as exc:
        print(
            "[JWT CONFIG] Immediate generation verification: FAILED",
            type(exc).__name__,
            str(exc),
        )
        raise

    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.
    """

    secret_fingerprint = hashlib.sha256(
        settings.SECRET_KEY.encode("utf-8")
    ).hexdigest()[:12]

    print(
        "[JWT CONFIG] VALIDATION:",
        "algorithm =", settings.ALGORITHM,
        "secret fingerprint =", secret_fingerprint,
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        print("[JWT DEBUG] Token validation successful.")

        return payload

    except JWTError as exc:
        print(
            f"[JWT DEBUG] Validation error: "
            f"{type(exc).__name__}: {exc}"
        )

        raise JWTError("Invalid or expired token.") from exc
