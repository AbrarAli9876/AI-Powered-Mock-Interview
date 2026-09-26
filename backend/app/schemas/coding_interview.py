from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.enums.coding_language import CodingLanguage
from app.enums.interview_status import InterviewStatus
from app.enums.question_difficulty import QuestionDifficulty
from app.schemas.coding_question import CodingQuestionResponse


class CodingInterviewCreate(BaseModel):
    """
    Data required to start a coding interview.
    """

    language: CodingLanguage

    difficulty: QuestionDifficulty

    total_questions: int = Field(
        ...,
        ge=3,
        le=10,
    )


class CodingInterviewResponse(BaseModel):
    """
    Coding interview session response.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    user_id: int

    language: CodingLanguage

    difficulty: QuestionDifficulty

    total_questions: int

    current_question_number: int

    status: InterviewStatus

    overall_score: Decimal | None

    created_at: datetime

    updated_at: datetime


class CodingInterviewQuestionResponse(BaseModel):
    """
    Current coding interview question.
    """

    question_number: int

    total_questions: int

    question: CodingQuestionResponse