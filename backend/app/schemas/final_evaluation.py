from pydantic import BaseModel, Field


class FinalInterviewEvaluation(BaseModel):
    """
    Comprehensive AI-generated evaluation of the
    candidate's complete interview performance.
    """

    final_summary: str = Field(
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

    key_strengths: str = Field(
        ...,
        min_length=1,
    )

    key_weaknesses: str = Field(
        ...,
        min_length=1,
    )

    recurring_mistakes: str = Field(
        ...,
        min_length=1,
    )

    improvement_areas: str = Field(
        ...,
        min_length=1,
    )

    recommendations: str = Field(
        ...,
        min_length=1,
    )

    final_assessment: str = Field(
        ...,
        min_length=1,
    )