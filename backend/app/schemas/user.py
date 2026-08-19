from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums.user_role import UserRole


class UserRegister(BaseModel):
    """
    Schema for user registration requests.
    """

    full_name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        examples=["Abrar Ahmed"],
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["StrongPassword123"],
    )


class UserLogin(BaseModel):
    """
    Schema for user login requests.
    """

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


class UserResponse(BaseModel):
    """
    Schema returned to the client.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    """
    JWT access token response.
    """

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Decoded JWT payload.
    """

    sub: str
    exp: int