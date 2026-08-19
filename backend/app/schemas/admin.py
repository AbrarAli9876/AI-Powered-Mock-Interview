from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr

from app.enums.interview_status import InterviewStatus
from app.enums.question_difficulty import QuestionDifficulty
from app.enums.user_role import UserRole


class AdminDashboardResponse(BaseModel):
    """
    Administrator dashboard statistics.
    """

    total_users: int
    total_interviews: int
    completed_interviews: int
    in_progress_interviews: int
    abandoned_interviews: int
    average_interview_score: Decimal | None


class AdminUserResponse(BaseModel):
    """
    User information visible to administrators.

    Password hashes are intentionally excluded.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AdminUserStatusUpdate(BaseModel):
    """
    Request for activating or deactivating a user.
    """

    is_active: bool


class AdminInterviewResponse(BaseModel):
    """
    Summary of an interview visible to administrators.
    """

    session_id: int

    user_id: int
    user_name: str
    user_email: EmailStr

    topic_id: int
    topic_name: str

    starting_difficulty: QuestionDifficulty
    final_difficulty: QuestionDifficulty

    status: InterviewStatus

    total_questions: int
    current_question_number: int

    overall_score: Decimal | None

    created_at: datetime
    updated_at: datetime


class AdminInterviewDetailResponse(BaseModel):
    """
    Complete interview information visible to administrators.
    """

    session_id: int

    user_id: int
    user_name: str
    user_email: EmailStr

    topic_id: int
    topic_name: str

    starting_difficulty: QuestionDifficulty
    final_difficulty: QuestionDifficulty

    status: InterviewStatus

    total_questions: int
    current_question_number: int

    overall_score: Decimal | None

    created_at: datetime
    updated_at: datetime

    difficulty_progression: list[QuestionDifficulty]

    final_summary: str | None
    final_strengths: str | None
    final_weaknesses: str | None

    technical_assessment: str | None
    communication_assessment: str | None
    problem_solving_assessment: str | None

    final_recommendations: str | None

    answers: list["AdminInterviewAnswerResponse"]


class AdminInterviewAnswerResponse(BaseModel):
    """
    Question-by-question interview evaluation
    visible to administrators.
    """

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