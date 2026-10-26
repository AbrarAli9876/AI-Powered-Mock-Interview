from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import (
    Token,
    UserLogin,
    UserRegister,
    UserResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
)
from app.services.auth_service import AuthService
from app.services.password_reset_service import PasswordResetService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    """Register a new user."""

    auth_service = AuthService(db)

    return auth_service.register_user(user)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    """Authenticate a user using JSON credentials."""

    auth_service = AuthService(db)

    return auth_service.authenticate_user(user)


@router.post(
    "/token",
    response_model=Token,
)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """OAuth2-compatible login endpoint used by Swagger."""

    login_data = UserLogin(
        email=form_data.username,
        password=form_data.password,
    )

    auth_service = AuthService(db)

    return auth_service.authenticate_user(login_data)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """Return the currently authenticated user."""

    return current_user


@router.post("/forgot-password")
def forgot_password(
    request: PasswordResetRequest,
    db: Session = Depends(get_db),
):
    """Send password-reset instructions without revealing account existence."""

    service = PasswordResetService(db)

    return service.request_reset(str(request.email))


@router.post("/reset-password")
def reset_password(
    request: PasswordResetConfirm,
    db: Session = Depends(get_db),
):
    """Validate a single-use reset token and save the new password."""

    service = PasswordResetService(db)

    return service.reset_password(
        request.token,
        request.new_password,
    )