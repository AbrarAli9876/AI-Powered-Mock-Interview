from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InterviewAnswerCreate(BaseModel):
    session_id: int = Field(..., gt=0)
    question_id: int = Field(..., gt=0)
    answer_text: str = Field(..., min_length=1)


class InterviewAnswerUpdate(BaseModel):
    overall_score: float | None = Field(default=None, ge=0, le=100)
    technical_score: float | None = Field(default=None, ge=0, le=100)
    communication_score: float | None = Field(default=None, ge=0, le=100)
    relevance_score: float | None = Field(default=None, ge=0, le=100)
    feedback: str | None = None
    strengths: str | None = None
    improvements: str | None = None


class InterviewAnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    question_id: int
    answer_text: str
    overall_score: float | None
    technical_score: float | None
    communication_score: float | None
    relevance_score: float | None
    feedback: str | None
    strengths: str | None
    improvements: str | None
    created_at: datetime
    updated_at: datetime