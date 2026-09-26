from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.coding_question import (
    CodingQuestionBulkCreate,
    CodingQuestionCreate,
    CodingQuestionResponse,
    CodingQuestionUpdate,
)
from app.services.coding_question_service import (
    CodingQuestionService,
)


router = APIRouter(
    prefix="/coding-questions",
    tags=["Coding Questions"],
)


# =========================================================
# CREATE CODING QUESTION
# =========================================================

@router.post(
    "",
    response_model=CodingQuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_question(
    question_data: CodingQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CodingQuestionService(db)

    try:
        return service.create_question(
            question_data
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# =========================================================
# CREATE CODING QUESTIONS IN BULK
# =========================================================

@router.post(
    "/bulk",
    response_model=list[CodingQuestionResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_questions_bulk(
    bulk_data: CodingQuestionBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CodingQuestionService(db)

    try:
        return service.create_questions_bulk(
            bulk_data
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# =========================================================
# GET CODING QUESTIONS
# =========================================================
#
# Expected request:
#
# /coding-questions?language=python&difficulty=easy
#
# Topic selection is intentionally not required.
# =========================================================

@router.get(
    "",
    response_model=list[CodingQuestionResponse],
)
def get_questions(
    language: str | None = None,
    difficulty: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CodingQuestionService(db)

    try:
        return service.get_questions(
            language=language,
            difficulty=difficulty,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# =========================================================
# GET SINGLE CODING QUESTION
# =========================================================

@router.get(
    "/{question_id}",
    response_model=CodingQuestionResponse,
)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CodingQuestionService(db)

    question = service.get_question_by_id(
        question_id
    )

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )

    return question


# =========================================================
# UPDATE CODING QUESTION
# =========================================================

@router.put(
    "/{question_id}",
    response_model=CodingQuestionResponse,
)
def update_question(
    question_id: int,
    question_data: CodingQuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CodingQuestionService(db)

    try:
        return service.update_question(
            question_id,
            question_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


# =========================================================
# DELETE CODING QUESTION
# =========================================================

@router.delete(
    "/{question_id}",
    response_model=CodingQuestionResponse,
)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CodingQuestionService(db)

    try:
        return service.delete_question(
            question_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )