from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CodingTestCaseCreate(BaseModel):
    """
    Schema used when creating a coding test case.
    """

    coding_question_id: int = Field(
        ...,
        gt=0,
    )

    input_data: str = Field(
        ...,
    )

    expected_output: str = Field(
        ...,
    )

    is_hidden: bool = False

    execution_order: int = Field(
        default=0,
        ge=0,
    )


class CodingTestCaseResponse(BaseModel):
    """
    Schema returned by the coding test case API.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    coding_question_id: int

    input_data: str

    expected_output: str

    is_hidden: bool

    execution_order: int

    created_at: datetime

    updated_at: datetime