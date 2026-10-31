from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
import hashlib
from app.core.exceptions import (
    InactiveUserException,
    UserNotFoundException,
)
from app.database import get_db
from app.enums.user_role import UserRole
from app.models.user import User
from app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
)



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    # Print fingerprint BEFORE attempting JWT validation.
    print(
        "[TOKEN DEBUG] Received fingerprint:",
        hashlib.sha256(token.encode("utf-8")).hexdigest()[:12]
    )

    try:
        payload = decode_access_token(token)

        print("[AUTH DEBUG] JWT decoded successfully")

        user_id = payload.get("sub")
        print(f"[AUTH DEBUG] JWT subject: {user_id}")

        if not user_id:
            print("[AUTH DEBUG] Missing subject")
            raise UserNotFoundException()

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            print("[AUTH DEBUG] Invalid user ID format")
            raise UserNotFoundException()

    except JWTError as exc:
        print(
            f"[AUTH DEBUG] JWT validation failed: "
            f"{type(exc).__name__}"
        )
        raise UserNotFoundException()

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        print(f"[AUTH DEBUG] User ID {user_id} not found in database")
        raise UserNotFoundException()

    print(f"[AUTH DEBUG] User found: ID={user.id}")

    if not user.is_active:
        raise InactiveUserException()

    return user



def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Allow access only to users with the ADMIN role.
    """

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required.",
        )

    return current_user