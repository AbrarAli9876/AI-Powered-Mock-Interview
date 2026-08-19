from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TopicCreate(BaseModel):
    """
    Schema used when creating a new topic.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    description: str = Field(
        ...,
        min_length=2,
    )


class TopicUpdate(BaseModel):
    """
    Schema used when updating an existing topic.
    """

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        min_length=2,
    )

    is_active: bool | None = None


class TopicResponse(BaseModel):
    """
    Schema returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime