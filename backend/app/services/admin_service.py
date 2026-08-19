from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.enums.interview_status import InterviewStatus
from app.enums.user_role import UserRole
from app.models.interview_answer import InterviewAnswer
from app.models.interview_session import InterviewSession
from app.models.question import Question
from app.models.topic import Topic
from app.models.user import User


class AdminService:
    """
    Handles business logic for administrator functionality.
    """

    def __init__(self, db: Session):
        self.db = db

    # =========================================================
    # DASHBOARD
    # =========================================================

    def get_dashboard_stats(self) -> dict:
        """
        Return high-level application statistics.
        """

        total_users = (
            self.db.query(func.count(User.id))
            .scalar()
            or 0
        )

        total_interviews = (
            self.db.query(
                func.count(InterviewSession.id)
            )
            .scalar()
            or 0
        )

        completed_interviews = (
            self.db.query(
                func.count(InterviewSession.id)
            )
            .filter(
                InterviewSession.status
                == InterviewStatus.COMPLETED
            )
            .scalar()
            or 0
        )

        in_progress_interviews = (
            self.db.query(
                func.count(InterviewSession.id)
            )
            .filter(
                InterviewSession.status
                == InterviewStatus.IN_PROGRESS
            )
            .scalar()
            or 0
        )

        abandoned_interviews = (
            self.db.query(
                func.count(InterviewSession.id)
            )
            .filter(
                InterviewSession.status
                == InterviewStatus.ABANDONED
            )
            .scalar()
            or 0
        )

        average_score = (
            self.db.query(
                func.avg(
                    InterviewSession.overall_score
                )
            )
            .filter(
                InterviewSession.overall_score.isnot(None)
            )
            .scalar()
        )

        if average_score is not None:
            average_score = Decimal(
                str(average_score)
            ).quantize(
                Decimal("0.01")
            )

        return {
            "total_users": total_users,
            "total_interviews": total_interviews,
            "completed_interviews": completed_interviews,
            "in_progress_interviews": in_progress_interviews,
            "abandoned_interviews": abandoned_interviews,
            "average_interview_score": average_score,
        }

    # =========================================================
    # USER MANAGEMENT
    # =========================================================

    def get_users(self) -> list[User]:
        """
        Return all application users.

        Password hashes are never exposed through the schema.
        """

        return (
            self.db.query(User)
            .order_by(User.id.asc())
            .all()
        )

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        """
        Retrieve a user by ID.
        """

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def update_user_status(
        self,
        user_id: int,
        is_active: bool,
        admin_user_id: int,
    ) -> User:
        """
        Activate or deactivate a user.

        Safety rules:
        - Admin cannot deactivate their own account.
        - The last active admin cannot be deactivated.
        """

        user = self.get_user_by_id(user_id)

        if not user:
            raise ValueError(
                "User not found."
            )

        # Prevent an administrator from
        # accidentally disabling themselves.
        if (
            user.id == admin_user_id
            and not is_active
        ):
            raise ValueError(
                "You cannot deactivate your own account."
            )

        # Prevent the last active administrator
        # from being disabled.
        if (
            user.role == UserRole.ADMIN
            and not is_active
            and user.is_active
        ):
            active_admin_count = (
                self.db.query(func.count(User.id))
                .filter(
                    User.role == UserRole.ADMIN,
                    User.is_active.is_(True),
                )
                .scalar()
                or 0
            )

            if active_admin_count <= 1:
                raise ValueError(
                    "The last active administrator "
                    "cannot be deactivated."
                )

        user.is_active = is_active

        self.db.commit()
        self.db.refresh(user)

        return user

    # =========================================================
    # INTERVIEW MANAGEMENT
    # =========================================================

    def get_interviews(
        self,
    ) -> list[dict]:
        """
        Return all interview sessions with
        candidate and topic information.
        """

        rows = (
            self.db.query(
                InterviewSession,
                User,
                Topic,
            )
            .join(
                User,
                InterviewSession.user_id == User.id,
            )
            .join(
                Topic,
                InterviewSession.topic_id == Topic.id,
            )
            .order_by(
                InterviewSession.id.desc()
            )
            .all()
        )

        results = []

        for interview, user, topic in rows:
            results.append(
                {
                    "session_id": interview.id,
                    "user_id": user.id,
                    "user_name": user.full_name,
                    "user_email": user.email,
                    "topic_id": topic.id,
                    "topic_name": topic.name,
                    "starting_difficulty": (
                        interview.starting_difficulty
                    ),
                    "final_difficulty": (
                        interview.current_difficulty
                    ),
                    "status": interview.status,
                    "total_questions": (
                        interview.total_questions
                    ),
                    "current_question_number": (
                        interview.current_question_number
                    ),
                    "overall_score": (
                        interview.overall_score
                    ),
                    "created_at": interview.created_at,
                    "updated_at": interview.updated_at,
                }
            )

        return results

    def get_interview_detail(
        self,
        session_id: int,
    ) -> dict:
        """
        Return the complete interview including:
        - candidate
        - topic
        - difficulty progression
        - question answers
        - individual evaluations
        - final AI report
        """

        row = (
            self.db.query(
                InterviewSession,
                User,
                Topic,
            )
            .join(
                User,
                InterviewSession.user_id == User.id,
            )
            .join(
                Topic,
                InterviewSession.topic_id == Topic.id,
            )
            .filter(
                InterviewSession.id == session_id
            )
            .first()
        )

        if not row:
            raise ValueError(
                "Interview not found."
            )

        interview, user, topic = row

        answers = (
            self.db.query(
                InterviewAnswer,
                Question,
            )
            .join(
                Question,
                InterviewAnswer.question_id
                == Question.id,
            )
            .filter(
                InterviewAnswer.session_id
                == session_id,
            )
            .order_by(
                InterviewAnswer.id.asc()
            )
            .all()
        )

        result_answers = []

        for answer, question in answers:
            result_answers.append(
                {
                    "question_id": question.id,
                    "question_text": (
                        question.question_text
                    ),
                    "difficulty": question.difficulty,
                    "answer_text": answer.answer_text,
                    "overall_score": (
                        float(answer.overall_score)
                        if answer.overall_score
                        is not None
                        else None
                    ),
                    "technical_score": (
                        float(answer.technical_score)
                        if answer.technical_score
                        is not None
                        else None
                    ),
                    "communication_score": (
                        float(
                            answer.communication_score
                        )
                        if answer.communication_score
                        is not None
                        else None
                    ),
                    "relevance_score": (
                        float(answer.relevance_score)
                        if answer.relevance_score
                        is not None
                        else None
                    ),
                    "feedback": answer.feedback,
                    "strengths": answer.strengths,
                    "improvements": answer.improvements,
                }
            )

        return {
            "session_id": interview.id,

            "user_id": user.id,
            "user_name": user.full_name,
            "user_email": user.email,

            "topic_id": topic.id,
            "topic_name": topic.name,

            "starting_difficulty": (
                interview.starting_difficulty
            ),
            "final_difficulty": (
                interview.current_difficulty
            ),

            "status": interview.status,

            "total_questions": (
                interview.total_questions
            ),
            "current_question_number": (
                interview.current_question_number
            ),

            "overall_score": interview.overall_score,

            "created_at": interview.created_at,
            "updated_at": interview.updated_at,

            "difficulty_progression": (
                interview.difficulty_progression
                or []
            ),

            "final_summary": (
                interview.final_summary
            ),
            "final_strengths": (
                interview.final_strengths
            ),
            "final_weaknesses": (
                interview.final_weaknesses
            ),

            "technical_assessment": (
                interview.technical_assessment
            ),
            "communication_assessment": (
                interview.communication_assessment
            ),
            "problem_solving_assessment": (
                interview.problem_solving_assessment
            ),

            "final_recommendations": (
                interview.final_recommendations
            ),

            "answers": result_answers,
        }