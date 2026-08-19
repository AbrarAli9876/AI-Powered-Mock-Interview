from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.enums.interview_status import InterviewStatus
from app.enums.question_difficulty import QuestionDifficulty


class InterviewCreate(BaseModel):
    topic_id: int = Field(
        ...,
        gt=0,
    )

    starting_difficulty: QuestionDifficulty


class InterviewUpdate(BaseModel):
    status: InterviewStatus | None = None


class InterviewResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    user_id: int
    topic_id: int

    starting_difficulty: QuestionDifficulty
    current_difficulty: QuestionDifficulty

    status: InterviewStatus

    total_questions: int
    current_question_number: int

    poor_streak: int
    strong_streak: int

    overall_score: Decimal | None

    created_at: datetime
    updated_at: datetime


class InterviewResultAnswer(BaseModel):
    question_id: int
    question_text: str
    difficulty: QuestionDifficulty

    answer_text: str

    overall_score: float | None
    technical_score: float | None
    communication_score: float | None
    relevance_score: float | None

    feedback: str | None
    strengths: str | None
    improvements: str | None


class InterviewResultResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    session_id: int
    user_id: int
    topic_id: int

    starting_difficulty: QuestionDifficulty
    final_difficulty: QuestionDifficulty

    status: InterviewStatus

    total_questions: int
    current_question_number: int

    overall_score: Decimal | None

    created_at: datetime
    updated_at: datetime

    # ---------------------------------------------------------
    # Actual difficulty progression
    # ---------------------------------------------------------

    difficulty_progression: list[QuestionDifficulty]

    # ---------------------------------------------------------
    # Final AI-generated interview report
    # ---------------------------------------------------------

    final_summary: str | None
    final_strengths: str | None
    final_weaknesses: str | None

    technical_assessment: str | None
    communication_assessment: str | None
    problem_solving_assessment: str | None

    final_recommendations: str | None

    # ---------------------------------------------------------
    # Question-by-question results
    # ---------------------------------------------------------

    answers: list[InterviewResultAnswer]