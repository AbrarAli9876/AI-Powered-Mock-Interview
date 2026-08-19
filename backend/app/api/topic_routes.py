from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import (
    get_current_admin,
    get_current_user,
)
from app.models.user import User
from app.schemas.topic import (
    TopicCreate,
    TopicResponse,
    TopicUpdate,
)
from app.services.topic_service import TopicService

router = APIRouter(
    prefix="/topics",
    tags=["Topics"],
)


@router.post(
    "",
    response_model=TopicResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_topic(
    topic_data: TopicCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = TopicService(db)

    try:
        return service.create_topic(topic_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[TopicResponse],
)
def get_topics(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    service = TopicService(db)

    return service.get_active_topics()


@router.get(
    "/{topic_id}",
    response_model=TopicResponse,
)
def get_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    service = TopicService(db)

    topic = service.get_topic_by_id(topic_id)

    if not topic or not topic.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found.",
        )

    return topic


@router.put(
    "/{topic_id}",
    response_model=TopicResponse,
)
def update_topic(
    topic_id: int,
    topic_data: TopicUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = TopicService(db)

    try:
        return service.update_topic(
            topic_id,
            topic_data,
        )
    except ValueError as exc:
        message = str(exc)

        if message == "Topic not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
        )


@router.delete(
    "/{topic_id}",
    response_model=TopicResponse,
)
def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = TopicService(db)

    try:
        return service.delete_topic(topic_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )