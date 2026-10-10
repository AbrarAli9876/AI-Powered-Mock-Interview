from decimal import Decimal

import logging



from sqlalchemy.orm import Session



from app.enums.interview_status import InterviewStatus

from app.enums.question_difficulty import QuestionDifficulty

from app.models.interview_answer import InterviewAnswer

from app.models.interview_session import InterviewSession

from app.models.question import Question

from app.schemas.interview_answer import (

    InterviewAnswerCreate,

    InterviewAnswerUpdate,

)

from app.services.adaptive_service import AdaptiveDifficultyService

from app.services.evaluation_service import EvaluationService

from app.services.interview_service import InterviewService

from app.services.question_service import QuestionService





logger = logging.getLogger(__name__)





class InterviewAnswerService:

    """

    Handles business logic related to interview answers.



    Responsibilities:

    - Validate interview ownership

    - Validate current question

    - Evaluate answers

    - Update adaptive difficulty

    - Track question progress

    - Automatically complete the interview

    - Calculate final score

    - Persist the completed interview

    - Generate the final AI report

    """



    def __init__(self, db: Session):

        self.db = db

        self.evaluation_service = EvaluationService(db)

        self.adaptive_service = AdaptiveDifficultyService()

        self.question_service = QuestionService(db)



    # =========================================================

    # CREATE ANSWER

    # =========================================================



    def create_answer(

        self,

        user_id: int,

        answer_data: InterviewAnswerCreate,

    ) -> InterviewAnswer:



        # -----------------------------------------------------

        # Find interview session

        # -----------------------------------------------------



        session = (

            self.db.query(InterviewSession)

            .filter(

                InterviewSession.id == answer_data.session_id,

                InterviewSession.user_id == user_id,

            )

            .first()

        )



        if not session:

            raise ValueError(

                "Interview session not found."

            )



        # -----------------------------------------------------

        # Interview must be active

        # -----------------------------------------------------



        if session.status != InterviewStatus.IN_PROGRESS:

            raise ValueError(

                "Answers can only be submitted for an "

                "in-progress interview."

            )



        # -----------------------------------------------------

        # There must be an active question

        # -----------------------------------------------------



        if session.current_question_id is None:

            raise ValueError(

                "There is no active question to answer."

            )



        # -----------------------------------------------------

        # Candidate must answer the active question

        # -----------------------------------------------------



        if (

            session.current_question_id

            != answer_data.question_id

        ):

            raise ValueError(

                "You must answer the current interview question."

            )



        # -----------------------------------------------------

        # Get question

        # -----------------------------------------------------



        question = (

            self.db.query(Question)

            .filter(

                Question.id == answer_data.question_id,

                Question.topic_id == session.topic_id,

            )

            .first()

        )



        if not question:

            raise ValueError(

                "Question not found for this interview topic."

            )



        # -----------------------------------------------------

        # Prevent duplicate answer

        # -----------------------------------------------------



        existing_answer = (

            self.db.query(InterviewAnswer)

            .filter(

                InterviewAnswer.session_id == session.id,

                InterviewAnswer.question_id == question.id,

            )

            .first()

        )



        if existing_answer:

            raise ValueError(

                "This question has already been answered "

                "in this interview."

            )



        # -----------------------------------------------------

        # Create answer

        # -----------------------------------------------------



        answer = InterviewAnswer(

            session_id=session.id,

            question_id=question.id,

            answer_text=answer_data.answer_text,

        )



        self.db.add(answer)

        self.db.flush()



        # -----------------------------------------------------

        # Evaluate answer using Gemini

        # -----------------------------------------------------



        try:

            self.evaluation_service.evaluate_answer(

                answer=answer,

                question=question,

            )

        except Exception as exc:

            self.db.rollback()



            logger.exception(

                "Answer evaluation failed for session %s.",

                session.id,

            )



            raise ValueError(

                f"Unable to evaluate the answer: {exc}"

            ) from exc



        # -----------------------------------------------------

        # Gemini must return an overall score

        # -----------------------------------------------------



        if answer.overall_score is None:

            self.db.rollback()



            raise ValueError(

                "Answer evaluation did not return "

                "an overall score."

            )



        # -----------------------------------------------------

        # Update adaptive performance

        # -----------------------------------------------------



        (

            next_difficulty,

            poor_streak,

            strong_streak,

        ) = self.adaptive_service.update_performance(

            current_difficulty=session.current_difficulty,

            poor_streak=session.poor_streak,

            strong_streak=session.strong_streak,

            score=float(answer.overall_score),

        )



        # -----------------------------------------------------

        # Update difficulty

        # -----------------------------------------------------



        session.current_difficulty = next_difficulty



        session.poor_streak = poor_streak

        session.strong_streak = strong_streak



        # -----------------------------------------------------

        # Record question count

        # -----------------------------------------------------



        # current_question_number counts answered questions.
        # total_questions is the configured target for this interview.
        session.current_question_number += 1



        # -----------------------------------------------------

        # The current question has now been answered

        # -----------------------------------------------------



        session.current_question_id = None



        self.db.flush()



        # -----------------------------------------------------

        # Determine whether more questions are available

        # -----------------------------------------------------



        reached_question_limit = (
            session.current_question_number >= session.total_questions
        )

        next_question_exists = (
            False
            if reached_question_limit
            else self._has_unanswered_questions(session=session)
        )



        # =====================================================

        # FINAL QUESTION

        # =====================================================



        if reached_question_limit or not next_question_exists:



            logger.info(

                "Interview %s has reached its final question.",

                session.id,

            )



            # -------------------------------------------------

            # Calculate final score BEFORE changing status

            # -------------------------------------------------



            final_score = self._calculate_overall_score(

                session.id

            )



            if final_score is None:

                self.db.rollback()



                raise ValueError(

                    "Unable to calculate the final "

                    "interview score."

                )



            # -------------------------------------------------

            # Mark interview COMPLETED

            # -------------------------------------------------



            session.overall_score = final_score



            session.status = InterviewStatus.COMPLETED



            session.current_question_id = None



            session.poor_streak = 0

            session.strong_streak = 0



            # -------------------------------------------------

            # IMPORTANT:

            #

            # Commit the completed interview FIRST.

            #

            # This guarantees that Gemini failure cannot

            # turn the completed interview into a failed

            # transaction.

            # -------------------------------------------------



            self.db.commit()



            self.db.refresh(session)

            self.db.refresh(answer)



            logger.info(

                "Interview %s marked COMPLETED with score %s.",

                session.id,

                session.overall_score,

            )



            # -------------------------------------------------

            # Generate final AI report

            #

            # This is intentionally AFTER the commit.

            # -------------------------------------------------



            try:

                interview_service = InterviewService(

                    self.db

                )



                interview_service.generate_final_report(

                    session

                )



                self.db.commit()

                self.db.refresh(session)



                logger.info(

                    "Final AI report generated for interview %s.",

                    session.id,

                )



            except Exception:

                # ---------------------------------------------

                # VERY IMPORTANT:

                #

                # Do NOT mark the interview abandoned.

                #

                # The interview is already COMPLETED in the DB.

                #

                # The report can be generated later.

                # ---------------------------------------------



                self.db.rollback()



                logger.exception(

                    "Final AI report generation failed "

                    "for interview %s.",

                    session.id,

                )



                # Reload the already committed interview.

                completed_session = (

                    self.db.query(InterviewSession)

                    .filter(

                        InterviewSession.id == session.id,

                        InterviewSession.user_id == user_id,

                    )

                    .first()

                )



                if completed_session:

                    session = completed_session



            # -------------------------------------------------

            # Return the final answer.

            # -------------------------------------------------



            self.db.refresh(answer)



            return answer



        # =====================================================

        # NON-FINAL QUESTION

        # =====================================================



        self.db.commit()



        self.db.refresh(answer)



        return answer



    # =========================================================

    # CHECK FOR UNANSWERED QUESTIONS

    # =========================================================



    def _has_unanswered_questions(

        self,

        session: InterviewSession,

    ) -> bool:

        """

        Determine whether at least one unanswered question

        remains for the interview.



        The difficulty fallback is:



        EASY:

            EASY -> MEDIUM -> HARD



        MEDIUM:

            MEDIUM -> HARD -> EASY



        HARD:

            HARD -> MEDIUM -> EASY

        """



        difficulty_order = {

            QuestionDifficulty.EASY: [

                QuestionDifficulty.EASY,

                QuestionDifficulty.MEDIUM,

                QuestionDifficulty.HARD,

            ],

            QuestionDifficulty.MEDIUM: [

                QuestionDifficulty.MEDIUM,

                QuestionDifficulty.HARD,

                QuestionDifficulty.EASY,

            ],

            QuestionDifficulty.HARD: [

                QuestionDifficulty.HARD,

                QuestionDifficulty.MEDIUM,

                QuestionDifficulty.EASY,

            ],

        }



        difficulties = difficulty_order[

            session.current_difficulty

        ]



        for difficulty in difficulties:



            question = (

                self.question_service.get_next_question(

                    session_id=session.id,

                    topic_id=session.topic_id,

                    difficulty=difficulty,

                )

            )



            if question is not None:

                return True



        return False



    # =========================================================

    # CALCULATE OVERALL SCORE

    # =========================================================



    def _calculate_overall_score(

        self,

        session_id: int,

    ) -> Decimal | None:

        """

        Calculate the final average score from all

        evaluated answers in the interview.

        """



        answers = (

            self.db.query(InterviewAnswer)

            .filter(

                InterviewAnswer.session_id == session_id,

                InterviewAnswer.overall_score.isnot(None),

            )

            .all()

        )



        if not answers:

            return None



        total_score = sum(

            Decimal(

                str(answer.overall_score)

            )

            for answer in answers

        )



        average_score = (

            total_score

            / Decimal(len(answers))

        )



        return average_score.quantize(

            Decimal("0.01")

        )



    # =========================================================

    # GET ANSWER BY ID

    # =========================================================



    def get_answer_by_id(

        self,

        answer_id: int,

        user_id: int,

    ) -> InterviewAnswer | None:



        return (

            self.db.query(InterviewAnswer)

            .join(InterviewSession)

            .filter(

                InterviewAnswer.id == answer_id,

                InterviewSession.user_id == user_id,

            )

            .first()

        )



    # =========================================================

    # GET ALL SESSION ANSWERS

    # =========================================================



    def get_session_answers(

        self,

        session_id: int,

        user_id: int,

    ) -> list[InterviewAnswer]:



        session = (

            self.db.query(InterviewSession)

            .filter(

                InterviewSession.id == session_id,

                InterviewSession.user_id == user_id,

            )

            .first()

        )



        if not session:

            raise ValueError(

                "Interview session not found."

            )



        return (

            self.db.query(InterviewAnswer)

            .filter(

                InterviewAnswer.session_id == session_id,

            )

            .order_by(

                InterviewAnswer.id.asc()

            )

            .all()

        )



    # =========================================================

    # UPDATE ANSWER

    # =========================================================



    def update_answer(

        self,

        answer_id: int,

        user_id: int,

        answer_data: InterviewAnswerUpdate,

    ) -> InterviewAnswer:



        answer = self.get_answer_by_id(

            answer_id,

            user_id,

        )



        if not answer:

            raise ValueError(

                "Interview answer not found."

            )



        if answer_data.overall_score is not None:

            answer.overall_score = (

                answer_data.overall_score

            )



        if answer_data.technical_score is not None:

            answer.technical_score = (

                answer_data.technical_score

            )



        if answer_data.communication_score is not None:

            answer.communication_score = (

                answer_data.communication_score

            )



        if answer_data.relevance_score is not None:

            answer.relevance_score = (

                answer_data.relevance_score

            )



        if answer_data.feedback is not None:

            answer.feedback = answer_data.feedback



        if answer_data.strengths is not None:

            answer.strengths = answer_data.strengths



        if answer_data.improvements is not None:

            answer.improvements = (

                answer_data.improvements

            )



        self.db.commit()

        self.db.refresh(answer)



        return answer