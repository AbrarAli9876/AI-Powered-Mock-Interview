from __future__ import annotations

import random

from sqlalchemy.orm import Session

from app.enums.interview_status import InterviewStatus
from app.models.coding_interview_question import (
    CodingInterviewQuestion,
)
from app.models.coding_interview_session import (
    CodingInterviewSession,
)
from app.models.coding_question import CodingQuestion
from app.schemas.coding_interview import (
    CodingInterviewCreate,
    CodingInterviewQuestionResponse,
)
from app.models.coding_interview_answer import (
    CodingInterviewAnswer,
)
from app.schemas.coding_interview_answer import (
    CodingInterviewSubmitResponse,
)
from app.services.code_execution_service import (
    CodeExecutionService,
)
from app.schemas.coding_interview_result import (
    CodingInterviewResultResponse,
    CodingInterviewResultAnswer,
)


class CodingInterviewService:
    """
    Handles coding interview session logic.

    Coding interviews do NOT use adaptive difficulty.
    The selected difficulty remains fixed for the
    entire interview.
    """

    def __init__(self, db: Session):
        self.db = db

    # =========================================================
    # LIST USER CODING INTERVIEWS (RECENT HISTORY)
    # =========================================================

    def get_user_interviews(self, user_id: int) -> list[CodingInterviewSession]:
        return (
            self.db.query(CodingInterviewSession)
            .filter(CodingInterviewSession.user_id == user_id)
            .order_by(CodingInterviewSession.created_at.desc())
            .all()
        )

    # =========================================================
    # START CODING INTERVIEW
    # =========================================================

    def create_interview(
        self,
        user_id: int,
        interview_data: CodingInterviewCreate,
    ) -> CodingInterviewSession:
        """
        Create a coding interview and randomly select
        the required number of questions.

        The user is identified using user_id.
        """

        requested_count = interview_data.total_questions

        # -----------------------------------------------------
        # Find available questions
        # -----------------------------------------------------

        available_questions = (
            self.db.query(CodingQuestion)
            .filter(
                CodingQuestion.language
                == interview_data.language,
                CodingQuestion.difficulty
                == interview_data.difficulty,
            )
            .all()
        )

        # -----------------------------------------------------
        # Validate question availability
        # -----------------------------------------------------

        if len(available_questions) < requested_count:
            raise ValueError(
                "Not enough coding questions are available "
                f"for {interview_data.language.value} "
                f"{interview_data.difficulty.value}. "
                f"Requested {requested_count}, "
                f"but only {len(available_questions)} "
                "are available."
            )

        # -----------------------------------------------------
        # Randomly select questions
        # -----------------------------------------------------

        selected_questions = random.sample(
            available_questions,
            requested_count,
        )

        # -----------------------------------------------------
        # Create interview session
        # -----------------------------------------------------

        session = CodingInterviewSession(
            user_id=user_id,
            language=interview_data.language,
            difficulty=interview_data.difficulty,
            total_questions=requested_count,
            current_question_number=1,
            status=InterviewStatus.IN_PROGRESS,
        )

        self.db.add(session)

        # Flush first so session.id is available
        self.db.flush()

        # -----------------------------------------------------
        # Save selected questions
        # -----------------------------------------------------

        for number, question in enumerate(
            selected_questions,
            start=1,
        ):
            session_question = CodingInterviewQuestion(
                session_id=session.id,
                coding_question_id=question.id,
                question_number=number,
                answered=False,
            )

            self.db.add(session_question)

        # -----------------------------------------------------
        # Save everything
        # -----------------------------------------------------

        self.db.commit()
        self.db.refresh(session)

        return session

    # =========================================================
    # GET CODING INTERVIEW
    # =========================================================

    def get_interview(
        self,
        session_id: int,
        user_id: int,
    ) -> CodingInterviewSession:
        """
        Get a coding interview belonging to the given user.
        """

        session = (
            self.db.query(CodingInterviewSession)
            .filter(
                CodingInterviewSession.id == session_id,
                CodingInterviewSession.user_id == user_id,
            )
            .first()
        )

        if not session:
            raise ValueError(
                "Coding interview not found."
            )

        return session

    # =========================================================
    # GET CURRENT QUESTION
    # =========================================================

    def get_current_question(
        self,
        session_id: int,
        user_id: int,
    ) -> CodingInterviewQuestionResponse:
        """
        Return the current coding question.
        """

        session = self.get_interview(
            session_id=session_id,
            user_id=user_id,
        )

        if session.status != InterviewStatus.IN_PROGRESS:
            raise ValueError(
                "Coding interview is no longer in progress."
            )

        selected_question = (
            self.db.query(CodingInterviewQuestion)
            .filter(
                CodingInterviewQuestion.session_id
                == session.id,
                CodingInterviewQuestion.question_number
                == session.current_question_number,
            )
            .first()
        )

        if not selected_question:
            raise ValueError(
                "Current coding interview question "
                "was not found."
            )

        return CodingInterviewQuestionResponse(
            question_number=(
                selected_question.question_number
            ),
            total_questions=session.total_questions,
            question=selected_question.coding_question,
        )

    # =========================================================
    # MOVE TO NEXT QUESTION
    # =========================================================

    def move_to_next_question(
        self,
        session_id: int,
        user_id: int,
    ) -> CodingInterviewQuestionResponse:
        """
        Move to the next coding question.

        The current question must already be answered.
        """

        session = self.get_interview(
            session_id=session_id,
            user_id=user_id,
        )

        if session.status != InterviewStatus.IN_PROGRESS:
            raise ValueError(
                "Coding interview is no longer in progress."
            )

        current = (
            self.db.query(CodingInterviewQuestion)
            .filter(
                CodingInterviewQuestion.session_id
                == session.id,
                CodingInterviewQuestion.question_number
                == session.current_question_number,
            )
            .first()
        )

        if not current:
            raise ValueError(
                "Current coding interview question "
                "was not found."
            )

        # -----------------------------------------------------
        # Current question must be answered
        # -----------------------------------------------------

        if not current.answered:
            raise ValueError(
                "You must submit the current question "
                "before moving to the next question."
            )

        # -----------------------------------------------------
        # Check whether this is the last question
        # -----------------------------------------------------

        if (
            session.current_question_number
            >= session.total_questions
        ):
            raise ValueError(
                "This is the last coding interview question."
            )

        # -----------------------------------------------------
        # Move forward
        # -----------------------------------------------------

        session.current_question_number += 1

        self.db.commit()
        self.db.refresh(session)

        return self.get_current_question(
            session_id=session.id,
            user_id=user_id,
        )

    # =========================================================
    # SKIP CURRENT QUESTION
    # =========================================================

    def skip_current_question(
        self,
        session_id: int,
        user_id: int,
    ) -> dict:
        """Mark the current question as skipped and advance.

        The existing ``answered`` flag is used as a processed flag here:
        a skipped question is marked processed, but has no answer record.
        The result calculation distinguishes the two using answer records.
        """
        session = self.get_interview(
            session_id=session_id,
            user_id=user_id,
        )

        if session.status != InterviewStatus.IN_PROGRESS:
            raise ValueError("Coding interview is no longer in progress.")

        current = (
            self.db.query(CodingInterviewQuestion)
            .filter(
                CodingInterviewQuestion.session_id == session.id,
                CodingInterviewQuestion.question_number == session.current_question_number,
            )
            .first()
        )

        if not current:
            raise ValueError("Current coding interview question was not found.")

        # A submitted question cannot be skipped retroactively.
        existing_answer = (
            self.db.query(CodingInterviewAnswer)
            .filter(
                CodingInterviewAnswer.session_id == session.id,
                CodingInterviewAnswer.question_number == current.question_number,
            )
            .first()
        )
        if existing_answer:
            raise ValueError("This question has already been submitted.")

        current.answered = True
        question_number = current.question_number
        is_last_question = question_number >= session.total_questions

        if is_last_question:
            session.status = InterviewStatus.COMPLETED
            self.db.commit()
            return {
                "is_last_question": True,
                "question_number": question_number,
                "next_question": None,
            }

        session.current_question_number += 1
        self.db.commit()
        self.db.refresh(session)

        next_question = self.get_current_question(
            session_id=session.id,
            user_id=user_id,
        )
        return {
            "is_last_question": False,
            "question_number": question_number,
            "next_question": next_question,
        }

    # =========================================================
    # SUBMIT CODING ANSWER
    # =========================================================

    def submit_answer(
        self,
        session_id: int,
        user_id: int,
        code: str,
    ) -> CodingInterviewSubmitResponse:
        """
        Execute and store the candidate's solution
        for the current coding interview question.
        """

        session = self.get_interview(
            session_id=session_id,
            user_id=user_id,
        )

        if session.status != InterviewStatus.IN_PROGRESS:
            raise ValueError(
                "Coding interview is no longer in progress."
            )

        if not code or not code.strip():
            raise ValueError(
                "Code cannot be empty."
            )

        # -----------------------------------------------------
        # Get current selected question
        # -----------------------------------------------------

        interview_question = (
            self.db.query(CodingInterviewQuestion)
            .filter(
                CodingInterviewQuestion.session_id
                == session.id,
                CodingInterviewQuestion.question_number
                == session.current_question_number,
            )
            .first()
        )

        if not interview_question:
            raise ValueError(
                "Current coding interview question "
                "was not found."
            )

        # -----------------------------------------------------
        # Prevent duplicate submission
        # -----------------------------------------------------

        existing_answer = (
            self.db.query(CodingInterviewAnswer)
            .filter(
                CodingInterviewAnswer.session_id
                == session.id,
                CodingInterviewAnswer
                .coding_interview_question_id
                == interview_question.id,
            )
            .first()
        )

        if existing_answer:
            raise ValueError(
                "This coding question has already "
                "been submitted."
            )

        # -----------------------------------------------------
        # Execute candidate code
        # -----------------------------------------------------

        execution_service = CodeExecutionService()

        execution_result = execution_service.execute(
            question=interview_question.coding_question,
            code=code,
        )

        # -----------------------------------------------------
        # Calculate score
        # -----------------------------------------------------

        total = execution_result.total_test_cases
        passed = execution_result.passed_test_cases

        score = (
            (passed / total) * 100
            if total > 0
            else 0
        )

        # -----------------------------------------------------
        # Store answer
        # -----------------------------------------------------

        answer = CodingInterviewAnswer(
            session_id=session.id,
            coding_interview_question_id=(
                interview_question.id
            ),
            coding_question_id=(
                interview_question.coding_question_id
            ),
            question_number=(
                interview_question.question_number
            ),
            code=code,
            success=execution_result.success,
            total_test_cases=total,
            passed_test_cases=passed,
            failed_test_cases=(
                execution_result.failed_test_cases
            ),
            score=score,
            feedback=(
                "All test cases passed."
                if execution_result.success
                else (
                    f"{passed} out of {total} "
                    "test cases passed."
                )
            ),
        )

        self.db.add(answer)

        # -----------------------------------------------------
        # Mark question as answered
        # -----------------------------------------------------

        interview_question.answered = True

        is_last_question = (
            session.current_question_number
            >= session.total_questions
        )

        # -----------------------------------------------------
        # Automatically complete after final question
        # -----------------------------------------------------

        if is_last_question:
            session.status = (
                InterviewStatus.COMPLETED
            )

        self.db.commit()
        self.db.refresh(answer)

        return CodingInterviewSubmitResponse(
            answer_id=answer.id,
            session_id=session.id,
            question_number=(
                interview_question.question_number
            ),
            success=execution_result.success,
            total_test_cases=total,
            passed_test_cases=passed,
            failed_test_cases=(
                execution_result.failed_test_cases
            ),
            score=score,
            feedback=answer.feedback,
            is_last_question=is_last_question,
        )

    # =========================================================
    # COMPLETE CODING INTERVIEW
    # =========================================================

    def complete_interview(
        self,
        session_id: int,
        user_id: int,
    ) -> CodingInterviewSession:
        """
        Explicitly complete a coding interview.

        Normally the final question automatically completes
        the interview. This method is provided for the
        explicit completion endpoint.
        """

        session = self.get_interview(
            session_id=session_id,
            user_id=user_id,
        )

        if session.status == InterviewStatus.COMPLETED:
            return session

        if session.status != InterviewStatus.IN_PROGRESS:
            raise ValueError(
                "Only an in-progress coding interview "
                "can be completed."
            )

        # Completing early is allowed. The result report records
        # attempted and unanswered questions separately.
        session.status = InterviewStatus.COMPLETED

        self.db.commit()
        self.db.refresh(session)

        return session

    # =========================================================
    # ABANDON CODING INTERVIEW
    # =========================================================

    def abandon_interview(
        self,
        session_id: int,
        user_id: int,
    ) -> CodingInterviewSession:
        """
        Abandon an in-progress coding interview.
        """

        session = self.get_interview(
            session_id=session_id,
            user_id=user_id,
        )

        if session.status != InterviewStatus.IN_PROGRESS:
            raise ValueError(
                "Only an in-progress coding interview "
                "can be abandoned."
            )

        session.status = InterviewStatus.ABANDONED

        self.db.commit()
        self.db.refresh(session)

        return session

    # =========================================================
    # GET CODING INTERVIEW RESULT
    # =========================================================

    def get_interview_result(
        self,
        session_id: int,
        user_id: int,
    ) -> CodingInterviewResultResponse:
        """
        Return the final result of a completed coding interview.
        """

        session = self.get_interview(
            session_id=session_id,
            user_id=user_id,
        )

        if session.status == InterviewStatus.IN_PROGRESS:
            raise ValueError(
                "End the coding interview before viewing its result."
            )

        # -----------------------------------------------------
        # Get submitted answers
        # -----------------------------------------------------

        answers = (
            self.db.query(CodingInterviewAnswer)
            .filter(
                CodingInterviewAnswer.session_id
                == session.id,
            )
            .order_by(
                CodingInterviewAnswer.question_number.asc()
            )
            .all()
        )


        # -----------------------------------------------------
        # Prepare result answers
        # -----------------------------------------------------

        result_answers: list[
            CodingInterviewResultAnswer
        ] = []

        total_test_cases = 0
        passed_test_cases = 0
        failed_test_cases = 0

        total_score = 0.0

        # -----------------------------------------------------
        # Process every answer
        # -----------------------------------------------------

        for answer in answers:

            coding_question = (
                answer.coding_question
            )

            total_test_cases += (
                answer.total_test_cases
            )

            passed_test_cases += (
                answer.passed_test_cases
            )

            failed_test_cases += (
                answer.failed_test_cases
            )

            if answer.score is not None:
                total_score += float(
                    answer.score
                )

            result_answers.append(
                CodingInterviewResultAnswer(
                    question_number=(
                        answer.question_number
                    ),
                    coding_question_id=(
                        answer.coding_question_id
                    ),
                    title=coding_question.title,
                    language=(
                        coding_question.language.value
                    ),
                    difficulty=(
                        coding_question.difficulty.value
                    ),
                    code=answer.code,
                    success=answer.success,
                    total_test_cases=(
                        answer.total_test_cases
                    ),
                    passed_test_cases=(
                        answer.passed_test_cases
                    ),
                    failed_test_cases=(
                        answer.failed_test_cases
                    ),
                    score=answer.score,
                    feedback=answer.feedback,
                )
            )

        # -----------------------------------------------------
        # Calculate question statuses
        # -----------------------------------------------------

        interview_questions = (
            self.db.query(CodingInterviewQuestion)
            .filter(CodingInterviewQuestion.session_id == session.id)
            .all()
        )
        submitted_question_numbers = {answer.question_number for answer in answers}
        solved_questions = sum(1 for answer in answers if answer.success)
        skipped_questions = sum(
            1
            for question in interview_questions
            if question.answered and question.question_number not in submitted_question_numbers
        )
        attempted_questions = len(answers)
        # Unanswered means not solved. It includes explicitly skipped questions,
        # never-visited questions, and submitted solutions that did not pass.
        unanswered_questions = max(session.total_questions - solved_questions, 0)

        # -----------------------------------------------------
        # Calculate overall score
        # -----------------------------------------------------

        overall_score = (
            total_score / attempted_questions
            if attempted_questions > 0
            else 0
        )

        # -----------------------------------------------------
        # Return final result
        # -----------------------------------------------------

        return CodingInterviewResultResponse(
            session_id=session.id,
            language=session.language.value,
            difficulty=session.difficulty.value,
            status=session.status.value,
            total_questions=session.total_questions,
            attempted_questions=attempted_questions,
            solved_questions=solved_questions,
            unanswered_questions=unanswered_questions,
            skipped_questions=skipped_questions,
            total_test_cases=total_test_cases,
            passed_test_cases=passed_test_cases,
            failed_test_cases=failed_test_cases,
            overall_score=overall_score,
            answers=result_answers,
        )