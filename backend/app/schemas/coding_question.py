from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums.coding_language import CodingLanguage
from app.enums.question_difficulty import QuestionDifficulty


class CodingQuestionCreate(BaseModel):
    """
    Schema used when creating a coding question.
    """

    topic_id: int = Field(
        ...,
        gt=0,
    )

    language: CodingLanguage

    difficulty: QuestionDifficulty

    title: str = Field(
        ...,
        min_length=3,
    )

    problem_statement: str = Field(
        ...,
        min_length=10,
    )

    input_format: str = Field(
        ...,
        min_length=1,
    )

    output_format: str = Field(
        ...,
        min_length=1,
    )

    constraints: str = Field(
        ...,
        min_length=1,
    )

    examples: str = Field(
        ...,
        min_length=1,
    )

    starter_code: str = Field(
        ...,
        min_length=1,
    )


class CodingQuestionBulkCreate(BaseModel):
    """
    Schema used when creating multiple coding questions.
    """

    questions: list[CodingQuestionCreate] = Field(
        ...,
        min_length=1,
        max_length=500,
    )


class CodingQuestionUpdate(BaseModel):
    """
    Schema used when updating a coding question.
    """

    topic_id: int | None = Field(
        default=None,
        gt=0,
    )

    language: CodingLanguage | None = None

    difficulty: QuestionDifficulty | None = None

    title: str | None = Field(
        default=None,
        min_length=3,
    )

    problem_statement: str | None = Field(
        default=None,
        min_length=10,
    )

    input_format: str | None = Field(
        default=None,
        min_length=1,
    )

    output_format: str | None = Field(
        default=None,
        min_length=1,
    )

    constraints: str | None = Field(
        default=None,
        min_length=1,
    )

    examples: str | None = Field(
        default=None,
        min_length=1,
    )

    starter_code: str | None = Field(
        default=None,
        min_length=1,
    )


class CodingQuestionResponse(BaseModel):
    """
    Schema returned by the coding question API.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    topic_id: int

    language: CodingLanguage

    difficulty: QuestionDifficulty

    title: str
    problem_statement: str

    input_format: str
    output_format: str

    constraints: str
    examples: str
    starter_code: str

    created_at: datetime
    updated_at: datetime