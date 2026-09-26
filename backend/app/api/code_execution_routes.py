from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.code_execution import (
    CodeExecutionRequest,
    CodeExecutionResponse,
)
from app.services.code_execution_service import (
    CodeExecutionService,
)
from app.services.coding_question_service import (
    CodingQuestionService,
)


router = APIRouter(
    prefix="/code-execution",
    tags=["Code Execution"],
)


# =========================================================
# RUN CODE
# =========================================================

@router.post(
    "/run",
    response_model=CodeExecutionResponse,
)
def run_code(
    execution_data: CodeExecutionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Execute candidate code against the test cases
    configured for a coding question.
    """

    question_service = CodingQuestionService(db)

    question = (
        question_service.get_question_by_id(
            execution_data.coding_question_id
        )
    )

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )


    execution_service = CodeExecutionService()


    try:
        return execution_service.execute(
            question=question,
            code=execution_data.code,
        )


    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )


    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "An unexpected error occurred "
                "while executing the code."
            ),
        )