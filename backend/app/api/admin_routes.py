from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_admin
from app.models.user import User
from app.schemas.admin import (
    AdminDashboardResponse,
    AdminInterviewDetailResponse,
    AdminInterviewResponse,
    AdminUserResponse,
    AdminUserStatusUpdate,
)
from app.services.admin_service import AdminService


router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
)


# =============================================================
# DASHBOARD
# =============================================================

@router.get(
    "/dashboard",
    response_model=AdminDashboardResponse,
)
def get_admin_dashboard(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Return administrator dashboard statistics.
    """

    service = AdminService(db)

    return service.get_dashboard_stats()


# =============================================================
# USER MANAGEMENT
# =============================================================

@router.get(
    "/users",
    response_model=list[AdminUserResponse],
)
def get_admin_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Return all application users.

    Admin access required.
    """

    service = AdminService(db)

    return service.get_users()


@router.get(
    "/users/{user_id}",
    response_model=AdminUserResponse,
)
def get_admin_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Return a specific user.
    """

    service = AdminService(db)

    user = service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user


@router.patch(
    "/users/{user_id}/status",
    response_model=AdminUserResponse,
)
def update_admin_user_status(
    user_id: int,
    status_data: AdminUserStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        get_current_admin
    ),
):
    """
    Activate or deactivate a user.

    Admin access required.
    """

    service = AdminService(db)

    try:
        return service.update_user_status(
            user_id=user_id,
            is_active=status_data.is_active,
            admin_user_id=current_admin.id,
        )

    except ValueError as exc:
        message = str(exc)

        if message == "User not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )


# =============================================================
# INTERVIEW MANAGEMENT
# =============================================================

@router.get(
    "/interviews",
    response_model=list[AdminInterviewResponse],
)
def get_admin_interviews(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Return all interview sessions.

    Admin access required.
    """

    service = AdminService(db)

    return service.get_interviews()


@router.get(
    "/interviews/{session_id}",
    response_model=AdminInterviewDetailResponse,
)
def get_admin_interview_detail(
    session_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Return complete interview details.

    Includes:
    - candidate information
    - questions
    - answers
    - individual AI evaluations
    - difficulty progression
    - final AI report
    """

    service = AdminService(db)

    try:
        return service.get_interview_detail(
            session_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )