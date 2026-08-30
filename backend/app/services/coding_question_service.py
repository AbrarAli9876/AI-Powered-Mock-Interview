from sqlalchemy.orm import Session

from app.enums.coding_language import CodingLanguage
from app.enums.question_difficulty import QuestionDifficulty
from app.models.coding_question import CodingQuestion
from app.models.topic import Topic
from app.schemas.coding_question import (
    CodingQuestionBulkCreate,
    CodingQuestionCreate,
    CodingQuestionUpdate,
)


class CodingQuestionService:
    """
    Handles business logic related to coding questions.
    """

    def __init__(self, db: Session):
        self.db = db


    def create_question(
        self,
        question_data: CodingQuestionCreate,
    ) -> CodingQuestion:
        """
        Create a new coding question.
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

        question = CodingQuestion(
            topic_id=question_data.topic_id,
            language=question_data.language,
            difficulty=question_data.difficulty,
            title=question_data.title,
            problem_statement=(
                question_data.problem_statement
            ),
            input_format=question_data.input_format,
            output_format=question_data.output_format,
            constraints=question_data.constraints,
            examples=question_data.examples,
            starter_code=question_data.starter_code,
        )

        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)

        return question


    def create_questions_bulk(
        self,
        bulk_data: CodingQuestionBulkCreate,
    ) -> list[CodingQuestion]:
        """
        Create multiple coding questions
        in a single transaction.
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
                "Active topic not found for "
                f"topic ID(s): {missing_ids}"
            )

        questions = [
            CodingQuestion(
                topic_id=question.topic_id,
                language=question.language,
                difficulty=question.difficulty,
                title=question.title,
                problem_statement=(
                    question.problem_statement
                ),
                input_format=question.input_format,
                output_format=question.output_format,
                constraints=question.constraints,
                examples=question.examples,
                starter_code=question.starter_code,
            )
            for question in bulk_data.questions
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
        language: CodingLanguage | None = None,
        difficulty: QuestionDifficulty | None = None,
    ) -> list[CodingQuestion]:
        """
        Return coding questions with optional filters.
        """

        query = self.db.query(CodingQuestion)

        if topic_id is not None:
            query = query.filter(
                CodingQuestion.topic_id == topic_id
            )

        if language is not None:
            query = query.filter(
                CodingQuestion.language == language
            )

        if difficulty is not None:
            query = query.filter(
                CodingQuestion.difficulty == difficulty
            )

        return (
            query
            .order_by(CodingQuestion.id.asc())
            .all()
        )


    def get_question_by_id(
        self,
        question_id: int,
    ) -> CodingQuestion | None:
        """
        Retrieve a coding question by ID.
        """

        return (
            self.db.query(CodingQuestion)
            .filter(
                CodingQuestion.id == question_id
            )
            .first()
        )


    def update_question(
        self,
        question_id: int,
        question_data: CodingQuestionUpdate,
    ) -> CodingQuestion:
        """
        Update an existing coding question.
        """

        question = self.get_question_by_id(
            question_id
        )

        if not question:
            raise ValueError(
                "Coding question not found."
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

        if question_data.language is not None:
            question.language = (
                question_data.language
            )

        if question_data.difficulty is not None:
            question.difficulty = (
                question_data.difficulty
            )

        if question_data.title is not None:
            question.title = question_data.title

        if question_data.problem_statement is not None:
            question.problem_statement = (
                question_data.problem_statement
            )

        if question_data.input_format is not None:
            question.input_format = (
                question_data.input_format
            )

        if question_data.output_format is not None:
            question.output_format = (
                question_data.output_format
            )

        if question_data.constraints is not None:
            question.constraints = (
                question_data.constraints
            )

        if question_data.examples is not None:
            question.examples = (
                question_data.examples
            )

        if question_data.starter_code is not None:
            question.starter_code = (
                question_data.starter_code
            )

        self.db.commit()
        self.db.refresh(question)

        return question


    def delete_question(
        self,
        question_id: int,
    ) -> CodingQuestion:
        """
        Permanently delete a coding question.
        """

        question = self.get_question_by_id(
            question_id
        )

        if not question:
            raise ValueError(
                "Coding question not found."
            )

        self.db.delete(question)
        self.db.commit()

        return question