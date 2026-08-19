from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.interview import (
    InterviewCreate,
    InterviewResponse,
    InterviewResultResponse,
    InterviewUpdate,
)
from app.schemas.question import QuestionResponse
from app.services.interview_service import InterviewService


router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"],
)


@router.post(
    "",
    response_model=InterviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interview(
    interview_data: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)

    try:
        return service.create_interview(
            current_user,
            interview_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[InterviewResponse],
)
def get_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)

    return service.get_user_interviews(
        current_user.id
    )


@router.get(
    "/{session_id}/result",
    response_model=InterviewResultResponse,
)
def get_interview_result(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)

    try:
        return service.get_interview_result(
            session_id,
            current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )


@router.get(
    "/{session_id}/next-question",
    response_model=QuestionResponse,
)
def get_next_question(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)

    try:
        return service.get_next_question(
            session_id,
            current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )


@router.get(
    "/{session_id}",
    response_model=InterviewResponse,
)
def get_interview(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)

    interview = service.get_interview_by_id(
        session_id
    )

    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found.",
        )

    if interview.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this interview.",
        )

    return interview


@router.put(
    "/{session_id}",
    response_model=InterviewResponse,
)
def update_interview(
    session_id: int,
    interview_data: InterviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)

    try:
        return service.update_interview(
            session_id,
            current_user.id,
            interview_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )


@router.post(
    "/{session_id}/complete",
    response_model=InterviewResponse,
)
def complete_interview(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)

    try:
        return service.complete_interview(
            session_id,
            current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )


@router.post(
    "/{session_id}/abandon",
    response_model=InterviewResponse,
)
def abandon_interview(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InterviewService(db)

    try:
        return service.abandon_interview(
            session_id,
            current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )