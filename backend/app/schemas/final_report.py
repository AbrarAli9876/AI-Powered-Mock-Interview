from pydantic import BaseModel, Field


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