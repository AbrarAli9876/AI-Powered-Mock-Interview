from sqlalchemy.orm import Session

from app.core.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)
from app.models.user import User
from app.schemas.user import Token, UserLogin, UserRegister
from app.utils.security import (
    create_access_token,
    hash_password,
    verify_password,
)


class AuthService:
    """
    Service responsible for user authentication and authorization.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        """
        Fetch a user by email.
        """
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def register_user(self, user_data: UserRegister) -> User:
        """
        Register a new user.
        """

        existing_user = self.get_user_by_email(user_data.email)

        if existing_user:
            raise EmailAlreadyExistsException()

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def authenticate_user(self, login_data: UserLogin) -> Token:
        """
        Authenticate user and generate JWT token.
        """

        user = self.get_user_by_email(login_data.email)

        if not user:
            raise InvalidCredentialsException()

        if not verify_password(
            login_data.password,
            user.password_hash,
        ):
            raise InvalidCredentialsException()

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.value,
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )