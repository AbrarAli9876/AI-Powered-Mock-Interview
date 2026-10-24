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

from app.schemas.coding_interview import (
    CodingInterviewCreate,
    CodingInterviewResponse,
    CodingInterviewQuestionResponse,
)

from app.schemas.coding_interview_answer import (
    CodingInterviewSubmitRequest,
    CodingInterviewSubmitResponse,
)

from app.schemas.coding_interview_result import (
    CodingInterviewResultResponse,
)

from app.services.coding_interview_service import (
    CodingInterviewService,
)


router = APIRouter(
    prefix="/coding-interviews",
    tags=["Coding Interviews"],
)


# =========================================================
# CREATE CODING INTERVIEW
# =========================================================

@router.post(
    "",
    response_model=CodingInterviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_coding_interview(
    interview_data: CodingInterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Start a new coding interview.

    The candidate chooses:

    - programming language
    - difficulty
    - number of questions

    The selected difficulty remains fixed throughout
    the interview.
    """

    service = CodingInterviewService(db)

    try:
        return service.create_interview(
            user_id=current_user.id,
            interview_data=interview_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "An unexpected error occurred "
                "while creating the coding interview."
            ),
        ) from exc


# =========================================================
# LIST USER CODING INTERVIEWS (RECENT HISTORY)
# =========================================================

@router.get(
    "",
    response_model=list[CodingInterviewResponse],
)
def get_coding_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CodingInterviewService(db)
    return service.get_user_interviews(user_id=current_user.id)


# =========================================================
# GET CODING INTERVIEW
# =========================================================

@router.get(
    "/{session_id}",
    response_model=CodingInterviewResponse,
)
def get_coding_interview(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a coding interview session.
    """

    service = CodingInterviewService(db)

    try:
        return service.get_interview(
            session_id=session_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


# =========================================================
# GET CURRENT QUESTION
# =========================================================

@router.get(
    "/{session_id}/current-question",
    response_model=CodingInterviewQuestionResponse,
)
def get_current_question(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return the current coding question
    for the interview.
    """

    service = CodingInterviewService(db)

    try:
        return service.get_current_question(
            session_id=session_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


# =========================================================
# SUBMIT CODING ANSWER
# =========================================================

@router.post(
    "/{session_id}/submit",
    response_model=CodingInterviewSubmitResponse,
)
def submit_coding_answer(
    session_id: int,
    submission: CodingInterviewSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit the candidate's code for the current question.

    The submitted code is executed against the configured
    test cases.

    The result is stored in the database.

    If this is the final question, the interview is
    automatically completed.
    """

    service = CodingInterviewService(db)

    try:
        return service.submit_answer(
            session_id=session_id,
            user_id=current_user.id,
            code=submission.code,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "An unexpected error occurred "
                "while executing the submitted code."
            ),
        ) from exc


# =========================================================
# NEXT QUESTION
# =========================================================

@router.post(
    "/{session_id}/next-question",
    response_model=CodingInterviewQuestionResponse,
)
def next_question(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Move to the next coding question.

    The current question must already have been submitted.

    The difficulty remains unchanged.
    """

    service = CodingInterviewService(db)

    try:
        return service.move_to_next_question(
            session_id=session_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


# =========================================================
# SKIP CURRENT QUESTION
# =========================================================

@router.post(
    "/{session_id}/skip-question",
    response_model=dict,
)
def skip_current_question(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Skip the current question and continue, or finish if it is last."""
    service = CodingInterviewService(db)
    try:
        return service.skip_current_question(
            session_id=session_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


# =========================================================
# COMPLETE CODING INTERVIEW
# =========================================================

@router.post(
    "/{session_id}/complete",
    response_model=CodingInterviewResponse,
)
def complete_coding_interview(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Complete the coding interview.

    The interview can only be explicitly completed
    after all questions have been answered.

    Normally, submitting the final question automatically
    completes the interview.
    """

    service = CodingInterviewService(db)

    try:
        return service.complete_interview(
            session_id=session_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


# =========================================================
# ABANDON CODING INTERVIEW
# =========================================================

@router.post(
    "/{session_id}/abandon",
    response_model=CodingInterviewResponse,
)
def abandon_coding_interview(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Abandon an in-progress coding interview.
    """

    service = CodingInterviewService(db)

    try:
        return service.abandon_interview(
            session_id=session_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


# =========================================================
# GET CODING INTERVIEW RESULT
# =========================================================

@router.get(
    "/{session_id}/result",
    response_model=CodingInterviewResultResponse,
)
def get_coding_interview_result(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get the final result of a completed coding interview.
    """

    service = CodingInterviewService(db)

    try:
        return service.get_interview_result(
            session_id=session_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc