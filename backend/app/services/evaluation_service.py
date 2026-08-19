from sqlalchemy.orm import Session

from app.ai.gemini_client import GeminiEvaluationClient
from app.models.interview_answer import InterviewAnswer
from app.models.interview_session import InterviewSession
from app.models.question import Question
from app.schemas.final_report import FinalInterviewReport


class EvaluationService:
    """
    Handles AI evaluation of interview answers
    and generation of final interview reports.
    """

    def __init__(self, db: Session):
        self.db = db
        self.gemini = GeminiEvaluationClient()

    def evaluate_answer(
        self,
        answer: InterviewAnswer,
        question: Question,
    ) -> InterviewAnswer:
        """
        Evaluate one interview answer using Gemini.
        """

        evaluation = self.gemini.evaluate_answer(
            question=question.question_text,
            expected_answer=question.expected_answer,
            candidate_answer=answer.answer_text,
        )

        answer.overall_score = (
            evaluation.overall_score
        )

        answer.technical_score = (
            evaluation.technical_score
        )

        answer.communication_score = (
            evaluation.communication_score
        )

        answer.relevance_score = (
            evaluation.relevance_score
        )

        answer.feedback = evaluation.feedback

        answer.strengths = evaluation.strengths

        answer.improvements = evaluation.improvements

        return answer

    def generate_final_report(
        self,
        session: InterviewSession,
    ) -> FinalInterviewReport:
        """
        Generate the final AI report for a completed interview.
        """

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
                == session.id,
            )
            .order_by(
                InterviewAnswer.id.asc()
            )
            .all()
        )

        if not answers:
            raise ValueError(
                "Cannot generate a final report "
                "without interview answers."
            )

        progression = []

        answer_sections = []

        for index, (answer, question) in enumerate(
            answers,
            start=1,
        ):
            difficulty = question.difficulty.value

            progression.append(
                difficulty
            )

            answer_sections.append(
                f"""
Question {index}
--------------
Difficulty: {difficulty}

Question:
{question.question_text}

Candidate Answer:
{answer.answer_text}

Overall Score:
{answer.overall_score}

Technical Score:
{answer.technical_score}

Communication Score:
{answer.communication_score}

Relevance Score:
{answer.relevance_score}

Feedback:
{answer.feedback}

Strengths:
{answer.strengths}

Improvements:
{answer.improvements}
"""
            )

        difficulty_progression = " → ".join(
            progression
        )

        answers_text = "\n".join(
            answer_sections
        )

        overall_score = float(
            session.overall_score
            if session.overall_score is not None
            else 0
        )

        topic_name = (
            session.topic.name
            if session.topic is not None
            else str(session.topic_id)
        )

        return self.gemini.generate_final_report(
            topic=topic_name,
            starting_difficulty=(
                session.starting_difficulty.value
            ),
            final_difficulty=(
                session.current_difficulty.value
            ),
            overall_score=overall_score,
            difficulty_progression=difficulty_progression,
            answers_text=answers_text,
        )