from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums.question_difficulty import QuestionDifficulty


class QuestionCreate(BaseModel):
    """
    Schema used when creating a new interview question.
    """

    topic_id: int = Field(
        ...,
        gt=0,
    )

    difficulty: QuestionDifficulty

    question_text: str = Field(
        ...,
        min_length=5,
    )

    expected_answer: str = Field(
        ...,
        min_length=5,
    )


class QuestionBulkCreate(BaseModel):
    """
    Schema used when creating multiple interview questions.
    """

    questions: list[QuestionCreate] = Field(
        ...,
        min_length=1,
        max_length=500,
    )


class QuestionUpdate(BaseModel):
    """
    Schema used when updating an existing question.
    """

    topic_id: int | None = Field(
        default=None,
        gt=0,
    )

    difficulty: QuestionDifficulty | None = None

    question_text: str | None = Field(
        default=None,
        min_length=5,
    )

    expected_answer: str | None = Field(
        default=None,
        min_length=5,
    )


class QuestionResponse(BaseModel):
    """
    Schema returned by the API.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    topic_id: int
    difficulty: QuestionDifficulty
    question_text: str
    expected_answer: str
    created_at: datetime
    updated_at: datetime