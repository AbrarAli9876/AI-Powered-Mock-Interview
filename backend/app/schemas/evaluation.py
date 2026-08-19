from pydantic import BaseModel, Field


class InterviewEvaluation(BaseModel):
    """
    Structured AI evaluation for a single interview answer.
    """

    overall_score: float = Field(
        ge=0,
        le=100,
    )

    technical_score: float = Field(
        ge=0,
        le=100,
    )

    communication_score: float = Field(
        ge=0,
        le=100,
    )

    relevance_score: float = Field(
        ge=0,
        le=100,
    )

    feedback: str

    strengths: str

    improvements: str


class FinalInterviewReport(BaseModel):
    """
    Structured final AI-generated interview report.
    """

    final_summary: str = Field(
        ...,
        min_length=1,
    )

    final_strengths: str = Field(
        ...,
        min_length=1,
    )

    final_weaknesses: str = Field(
        ...,
        min_length=1,
    )

    technical_assessment: str = Field(
        ...,
        min_length=1,
    )

    communication_assessment: str = Field(
        ...,
        min_length=1,
    )

    problem_solving_assessment: str = Field(
        ...,
        min_length=1,
    )

    final_recommendations: str = Field(
        ...,
        min_length=1,
    )