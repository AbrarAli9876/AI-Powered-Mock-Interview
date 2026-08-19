from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

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
    """
    Retrieve the currently authenticated user from the JWT token.
    """

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if not user_id:
            raise UserNotFoundException()

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise UserNotFoundException()

    except JWTError:
        raise UserNotFoundException()

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise UserNotFoundException()

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