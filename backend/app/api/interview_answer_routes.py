from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.interview_answer import (
    InterviewAnswerCreate,
    InterviewAnswerResponse,
    InterviewAnswerUpdate,
)
from app.services.interview_answer_service import (
    InterviewAnswerService,
)


router = APIRouter(
    prefix="/interview-answers",
    tags=["Interview Answers"],
)


# =========================================================
# CREATE INTERVIEW ANSWER
# =========================================================

@router.post(
    "",
    response_model=InterviewAnswerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_answer(
    answer_data: InterviewAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewAnswerService(db)

    try:
        return service.create_answer(
            current_user.id,
            answer_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


# =========================================================
# GET ALL ANSWERS FOR AN INTERVIEW
# =========================================================

@router.get(
    "/session/{session_id}",
    response_model=list[InterviewAnswerResponse],
)
def get_session_answers(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewAnswerService(db)

    try:
        return service.get_session_answers(
            session_id,
            current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


# =========================================================
# GET SINGLE ANSWER
# =========================================================

@router.get(
    "/{answer_id}",
    response_model=InterviewAnswerResponse,
)
def get_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewAnswerService(db)

    answer = service.get_answer_by_id(
        answer_id,
        current_user.id,
    )

    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview answer not found.",
        )

    return answer


# =========================================================
# UPDATE ANSWER
# =========================================================

@router.put(
    "/{answer_id}",
    response_model=InterviewAnswerResponse,
)
def update_answer(
    answer_id: int,
    answer_data: InterviewAnswerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewAnswerService(db)

    try:
        return service.update_answer(
            answer_id,
            current_user.id,
            answer_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc