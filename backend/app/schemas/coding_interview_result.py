from decimal import Decimal

from pydantic import BaseModel


class CodingInterviewResultAnswer(BaseModel):
    """
    Result of one coding interview question.
    """

    question_number: int

    coding_question_id: int

    title: str

    language: str

    difficulty: str

    code: str

    success: bool

    total_test_cases: int

    passed_test_cases: int

    failed_test_cases: int

    score: Decimal | None

    feedback: str | None


class CodingInterviewResultResponse(BaseModel):
    """
    Final result of a coding interview.
    """

    session_id: int

    language: str

    difficulty: str

    status: str

    total_questions: int

    attempted_questions: int

    solved_questions: int = 0

    unanswered_questions: int = 0

    skipped_questions: int = 0

    total_test_cases: int

    passed_test_cases: int

    failed_test_cases: int

    overall_score: Decimal

    answers: list[CodingInterviewResultAnswer]