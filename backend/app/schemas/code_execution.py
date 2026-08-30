from pydantic import BaseModel, Field


class CodeExecutionRequest(BaseModel):
    """
    Schema used when running candidate code.
    """

    coding_question_id: int = Field(
        ...,
        gt=0,
    )

    code: str = Field(
        ...,
        min_length=1,
    )


class TestCaseResult(BaseModel):
    """
    Result of one test case.
    """

    test_case_number: int

    passed: bool

    input_data: str

    expected_output: str

    actual_output: str

    error: str | None = None

    execution_time_ms: float | None = None


class CodeExecutionResponse(BaseModel):
    """
    Response returned after executing candidate code.
    """

    success: bool

    language: str

    total_test_cases: int

    passed_test_cases: int

    failed_test_cases: int

    results: list[TestCaseResult]