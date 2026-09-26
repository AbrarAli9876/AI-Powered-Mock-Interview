from decimal import Decimal

from pydantic import BaseModel, Field


class CodingInterviewSubmitRequest(BaseModel):
    """
    Candidate's final code submission.
    """

    code: str = Field(
        ...,
        min_length=1,
    )


class CodingInterviewSubmitResponse(BaseModel):
    """
    Result returned after submitting a coding solution.
    """

    answer_id: int

    session_id: int

    question_number: int

    success: bool

    total_test_cases: int

    passed_test_cases: int

    failed_test_cases: int

    score: Decimal | None

    feedback: str | None

    is_last_question: bool