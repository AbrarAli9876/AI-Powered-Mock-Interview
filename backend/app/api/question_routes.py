from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import (
    get_current_admin,
    get_current_user,
)
from app.enums.question_difficulty import QuestionDifficulty
from app.models.user import User
from app.schemas.question import (
    QuestionBulkCreate,
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
)
from app.services.question_service import QuestionService


router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.post(
    "",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Create a new interview question.
    Admin access required.
    """

    service = QuestionService(db)

    try:
        return service.create_question(
            question_data
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.post(
    "/bulk",
    response_model=list[QuestionResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_questions_bulk(
    bulk_data: QuestionBulkCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Create multiple interview questions.
    Admin access required.
    """

    service = QuestionService(db)

    try:
        return service.create_questions_bulk(
            bulk_data
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[QuestionResponse],
)
def get_questions(
    topic_id: int | None = Query(
        default=None,
        gt=0,
    ),
    difficulty: QuestionDifficulty | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Get interview questions with optional filters.
    Authentication required.
    """

    service = QuestionService(db)

    return service.get_questions(
        topic_id=topic_id,
        difficulty=difficulty,
    )


@router.get(
    "/{question_id}",
    response_model=QuestionResponse,
)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Get a question by ID.
    Authentication required.
    """

    service = QuestionService(db)

    question = service.get_question_by_id(
        question_id
    )

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found.",
        )

    return question


@router.put(
    "/{question_id}",
    response_model=QuestionResponse,
)
def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Update an existing interview question.
    Admin access required.
    """

    service = QuestionService(db)

    try:
        return service.update_question(
            question_id,
            question_data,
        )

    except ValueError as exc:
        message = str(exc)

        if message == "Question not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        if message == "Active topic not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )


@router.delete(
    "/{question_id}",
    response_model=QuestionResponse,
)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Delete an interview question.
    Admin access required.
    """

    service = QuestionService(db)

    try:
        return service.delete_question(
            question_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )