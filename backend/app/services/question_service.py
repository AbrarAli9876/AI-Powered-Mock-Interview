from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.enums.question_difficulty import QuestionDifficulty
from app.models.interview_answer import InterviewAnswer
from app.models.question import Question
from app.models.topic import Topic
from app.schemas.question import (
    QuestionBulkCreate,
    QuestionCreate,
    QuestionUpdate,
)


class QuestionService:
    """
    Handles business logic related to interview questions.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_question(
        self,
        question_data: QuestionCreate,
    ) -> Question:
        """
        Create a new interview question.
        """

        topic = (
            self.db.query(Topic)
            .filter(
                Topic.id == question_data.topic_id,
                Topic.is_active.is_(True),
            )
            .first()
        )

        if not topic:
            raise ValueError(
                "Active topic not found."
            )

        question = Question(
            topic_id=question_data.topic_id,
            difficulty=question_data.difficulty,
            question_text=question_data.question_text,
            expected_answer=question_data.expected_answer,
        )

        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)

        return question

    def create_questions_bulk(
        self,
        bulk_data: QuestionBulkCreate,
    ) -> list[Question]:
        """
        Create multiple interview questions
        in a single database transaction.
        """

        topic_ids = {
            question.topic_id
            for question in bulk_data.questions
        }

        active_topics = (
            self.db.query(Topic)
            .filter(
                Topic.id.in_(topic_ids),
                Topic.is_active.is_(True),
            )
            .all()
        )

        active_topic_ids = {
            topic.id
            for topic in active_topics
        }

        missing_topic_ids = (
            topic_ids - active_topic_ids
        )

        if missing_topic_ids:
            missing_ids = ", ".join(
                str(topic_id)
                for topic_id in sorted(
                    missing_topic_ids
                )
            )

            raise ValueError(
                f"Active topic not found for topic ID(s): "
                f"{missing_ids}"
            )

        questions = [
            Question(
                topic_id=question_data.topic_id,
                difficulty=question_data.difficulty,
                question_text=question_data.question_text,
                expected_answer=question_data.expected_answer,
            )
            for question_data in bulk_data.questions
        ]

        try:
            self.db.add_all(questions)
            self.db.commit()

            for question in questions:
                self.db.refresh(question)

        except Exception:
            self.db.rollback()
            raise

        return questions

    def get_questions(
        self,
        topic_id: int | None = None,
        difficulty: QuestionDifficulty | None = None,
    ) -> list[Question]:
        """
        Return questions with optional topic
        and difficulty filters.
        """

        query = self.db.query(Question)

        if topic_id is not None:
            query = query.filter(
                Question.topic_id == topic_id
            )

        if difficulty is not None:
            query = query.filter(
                Question.difficulty == difficulty
            )

        return (
            query
            .order_by(Question.id.asc())
            .all()
        )

    def get_next_question(
        self,
        session_id: int,
        topic_id: int,
        difficulty: QuestionDifficulty,
    ) -> Question | None:
        """
        Return the next unanswered question.

        The requested difficulty is preferred.

        If no unanswered question exists at the
        requested difficulty, the service falls back
        to the other difficulty levels.

        The interview is considered exhausted only
        when no unanswered question remains at any
        difficulty level.
        """

        answered_question_ids = select(
            InterviewAnswer.question_id
        ).where(
            InterviewAnswer.session_id == session_id
        )

        difficulty_order = {
            QuestionDifficulty.EASY: [
                QuestionDifficulty.EASY,
                QuestionDifficulty.MEDIUM,
                QuestionDifficulty.HARD,
            ],
            QuestionDifficulty.MEDIUM: [
                QuestionDifficulty.MEDIUM,
                QuestionDifficulty.EASY,
                QuestionDifficulty.HARD,
            ],
            QuestionDifficulty.HARD: [
                QuestionDifficulty.HARD,
                QuestionDifficulty.MEDIUM,
                QuestionDifficulty.EASY,
            ],
        }

        difficulties = difficulty_order[difficulty]

        for current_difficulty in difficulties:

            question = (
                self.db.query(Question)
                .filter(
                    Question.topic_id == topic_id,
                    Question.difficulty == current_difficulty,
                    ~Question.id.in_(
                        answered_question_ids
                    ),
                )
                .order_by(
                    func.rand()
                )
                .first()
            )

            if question:
                return question

        return None

    def get_question_by_id(
        self,
        question_id: int,
    ) -> Question | None:
        """
        Retrieve a question by ID.
        """

        return (
            self.db.query(Question)
            .filter(
                Question.id == question_id
            )
            .first()
        )

    def update_question(
        self,
        question_id: int,
        question_data: QuestionUpdate,
    ) -> Question:
        """
        Update an existing interview question.
        """

        question = self.get_question_by_id(
            question_id
        )

        if not question:
            raise ValueError(
                "Question not found."
            )

        if question_data.topic_id is not None:
            topic = (
                self.db.query(Topic)
                .filter(
                    Topic.id == question_data.topic_id,
                    Topic.is_active.is_(True),
                )
                .first()
            )

            if not topic:
                raise ValueError(
                    "Active topic not found."
                )

            question.topic_id = (
                question_data.topic_id
            )

        if question_data.difficulty is not None:
            question.difficulty = (
                question_data.difficulty
            )

        if question_data.question_text is not None:
            question.question_text = (
                question_data.question_text
            )

        if question_data.expected_answer is not None:
            question.expected_answer = (
                question_data.expected_answer
            )

        self.db.commit()
        self.db.refresh(question)

        return question

    def delete_question(
        self,
        question_id: int,
    ) -> Question:
        """
        Permanently delete an interview question.
        """

        question = self.get_question_by_id(
            question_id
        )

        if not question:
            raise ValueError(
                "Question not found."
            )

        self.db.delete(question)
        self.db.commit()

        return question