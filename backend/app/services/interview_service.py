from __future__ import annotations



from decimal import Decimal



from sqlalchemy.orm import Session



from app.ai.gemini_client import GeminiEvaluationClient

from app.enums.interview_status import InterviewStatus

from app.enums.question_difficulty import QuestionDifficulty

from app.models.interview_answer import InterviewAnswer

from app.models.interview_session import InterviewSession

from app.models.question import Question

from app.models.topic import Topic

from app.models.user import User

from app.schemas.interview import (

    InterviewCreate,

    InterviewResultAnswer,

    InterviewResultResponse,

    InterviewUpdate,

)

from app.services.question_service import QuestionService





class InterviewService:

    """

    Handles business logic related to interview sessions.

    """



    def __init__(self, db: Session):

        self.db = db

        self.question_service = QuestionService(db)

        self.gemini = GeminiEvaluationClient()



    # =========================================================

    # CREATE INTERVIEW

    # =========================================================



    def create_interview(

        self,

        user: User,

        interview_data: InterviewCreate,

    ) -> InterviewSession:

        """

        Create a new interview session.

        """



        topic = (

            self.db.query(Topic)

            .filter(

                Topic.id == interview_data.topic_id,

                Topic.is_active.is_(True),

            )

            .first()

        )



        if not topic:

            raise ValueError("Active topic not found.")



        interview = InterviewSession(

            user_id=user.id,

            topic_id=interview_data.topic_id,

            starting_difficulty=interview_data.starting_difficulty,

            current_difficulty=interview_data.starting_difficulty,

            current_question_id=None,

            status=InterviewStatus.IN_PROGRESS,

            # total_questions stores the configured target for this session.
            total_questions=interview_data.question_count,

            current_question_number=0,

            poor_streak=0,

            strong_streak=0,

        )



        self.db.add(interview)

        self.db.commit()

        self.db.refresh(interview)



        return interview



    # =========================================================

    # GET USER INTERVIEWS

    # =========================================================



    def get_user_interviews(

        self,

        user_id: int,

    ) -> list[InterviewSession]:

        """

        Return all interview sessions belonging to the user.

        """



        return (

            self.db.query(InterviewSession)

            .filter(

                InterviewSession.user_id == user_id

            )

            .order_by(

                InterviewSession.id.desc()

            )

            .all()

        )



    # =========================================================

    # GET INTERVIEW BY ID

    # =========================================================



    def get_interview_by_id(

        self,

        session_id: int,

    ) -> InterviewSession | None:

        """

        Retrieve an interview session by ID.

        """



        return (

            self.db.query(InterviewSession)

            .filter(

                InterviewSession.id == session_id

            )

            .first()

        )



    # =========================================================

    # GET NEXT QUESTION

    # =========================================================



    def get_next_question(

        self,

        session_id: int,

        user_id: int,

    ) -> Question:

        """

        Return the current question for an interview.



        If a current question already exists, the same question

        is returned.



        If there is no current question, a new unanswered

        question is selected according to adaptive difficulty.

        """



        interview = self.get_interview_by_id(session_id)



        if not interview:

            raise ValueError("Interview not found.")



        if interview.user_id != user_id:

            raise PermissionError(

                "You do not own this interview."

            )



        if interview.status != InterviewStatus.IN_PROGRESS:

            raise ValueError(

                "Interview is no longer in progress."

            )



        # -----------------------------------------------------

        # Return existing current question

        # -----------------------------------------------------



        if interview.current_question_id is not None:



            current_question = (

                self.db.query(Question)

                .filter(

                    Question.id == interview.current_question_id,

                    Question.topic_id == interview.topic_id,

                )

                .first()

            )



            if not current_question:

                raise ValueError(

                    "Current interview question was not found."

                )



            return current_question



        # -----------------------------------------------------

        # Adaptive difficulty fallback order

        # -----------------------------------------------------



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

            interview.current_difficulty

        ]



        # -----------------------------------------------------

        # Find unanswered question

        # -----------------------------------------------------



        for difficulty in difficulties:



            question = (

                self.question_service.get_next_question(

                    session_id=session_id,

                    topic_id=interview.topic_id,

                    difficulty=difficulty,

                )

            )



            if question:



                interview.current_question_id = question.id



                self.db.commit()

                self.db.refresh(interview)



                return question



        # -----------------------------------------------------

        # No unanswered questions remain

        # -----------------------------------------------------



        raise ValueError(

            "No unanswered questions are available "

            "for this interview."

        )



    # =========================================================

    # GET INTERVIEW RESULT

    # =========================================================



    def get_interview_result(

        self,

        session_id: int,

        user_id: int,

    ) -> InterviewResultResponse:

        """

        Return the complete interview result.

        """



        interview = (

            self.db.query(InterviewSession)

            .filter(

                InterviewSession.id == session_id,

                InterviewSession.user_id == user_id,

            )

            .first()

        )



        if not interview:

            raise ValueError("Interview not found.")



        answers = (

            self.db.query(

                InterviewAnswer,

                Question,

            )

            .join(

                Question,

                InterviewAnswer.question_id == Question.id,

            )

            .filter(

                InterviewAnswer.session_id == session_id,

            )

            .order_by(

                InterviewAnswer.id.asc()

            )

            .all()

        )



        result_answers = []



        for answer, question in answers:



            result_answers.append(

                InterviewResultAnswer(

                    question_id=question.id,

                    question_text=question.question_text,

                    difficulty=question.difficulty,

                    answer_text=answer.answer_text,



                    overall_score=(

                        float(answer.overall_score)

                        if answer.overall_score is not None

                        else None

                    ),



                    technical_score=(

                        float(answer.technical_score)

                        if answer.technical_score is not None

                        else None

                    ),



                    communication_score=(

                        float(answer.communication_score)

                        if answer.communication_score is not None

                        else None

                    ),



                    relevance_score=(

                        float(answer.relevance_score)

                        if answer.relevance_score is not None

                        else None

                    ),



                    feedback=answer.feedback,

                    strengths=answer.strengths,

                    improvements=answer.improvements,

                )

            )



        difficulty_progression = [

            question.difficulty

            for answer, question in answers

        ]



        if not difficulty_progression:

            difficulty_progression = [

                interview.starting_difficulty

            ]



        return InterviewResultResponse(

            session_id=interview.id,

            user_id=interview.user_id,

            topic_id=interview.topic_id,



            starting_difficulty=(

                interview.starting_difficulty

            ),



            final_difficulty=(

                interview.current_difficulty

            ),



            status=interview.status,



            total_questions=(

                interview.total_questions

            ),



            current_question_number=(

                interview.current_question_number

            ),



            overall_score=(

                interview.overall_score

            ),



            created_at=interview.created_at,

            updated_at=interview.updated_at,



            difficulty_progression=(

                difficulty_progression

            ),



            final_summary=(

                interview.final_summary

            ),



            final_strengths=(

                interview.final_strengths

            ),



            final_weaknesses=(

                interview.final_weaknesses

            ),



            technical_assessment=(

                interview.technical_assessment

            ),



            communication_assessment=(

                interview.communication_assessment

            ),



            problem_solving_assessment=(

                interview.problem_solving_assessment

            ),



            final_recommendations=(

                interview.final_recommendations

            ),



            answers=result_answers,

        )



    # =========================================================

    # GENERATE FINAL AI REPORT

    # =========================================================



    def generate_final_report(

        self,

        interview: InterviewSession,

    ) -> InterviewSession:

        """

        Generate and save the final AI-powered interview report.



        This should only be called after the interview has been

        marked as COMPLETED and the final overall score exists.

        """



        if interview.status != InterviewStatus.COMPLETED:

            raise ValueError(

                "Final report can only be generated "

                "for a completed interview."

            )



        if interview.overall_score is None:

            raise ValueError(

                "Overall interview score is required "

                "before generating the final report."

            )



        # -----------------------------------------------------

        # Get topic

        # -----------------------------------------------------



        topic = (

            self.db.query(Topic)

            .filter(

                Topic.id == interview.topic_id

            )

            .first()

        )



        if not topic:

            raise ValueError(

                "Interview topic not found."

            )



        # -----------------------------------------------------

        # Get evaluated answers

        # -----------------------------------------------------



        answers = (

            self.db.query(

                InterviewAnswer,

                Question,

            )

            .join(

                Question,

                InterviewAnswer.question_id == Question.id,

            )

            .filter(

                InterviewAnswer.session_id == interview.id,

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



        # -----------------------------------------------------

        # Difficulty progression

        # -----------------------------------------------------



        difficulty_progression_values = [

            question.difficulty.value

            for answer, question in answers

        ]



        difficulty_progression = " → ".join(

            difficulty_progression_values

        )



        # -----------------------------------------------------

        # Build answer information for Gemini

        # -----------------------------------------------------



        answers_text_parts = []



        for index, (answer, question) in enumerate(

            answers,

            start=1,

        ):



            answers_text_parts.append(

                f"""

Question {index}

\--------------



Difficulty:

{question.difficulty.value}



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



        answers_text = "\n".join(

            answers_text_parts

        )



        # -----------------------------------------------------

        # Generate final report using Gemini

        # -----------------------------------------------------



        report = self.gemini.generate_final_report(

            topic=topic.name,

            starting_difficulty=(

                interview.starting_difficulty.value

            ),

            final_difficulty=(

                interview.current_difficulty.value

            ),

            overall_score=float(

                interview.overall_score

            ),

            difficulty_progression=(

                difficulty_progression

            ),

            answers_text=answers_text,

        )



        # -----------------------------------------------------

        # Save difficulty progression

        # -----------------------------------------------------



        interview.difficulty_progression = (

            difficulty_progression_values

        )



        # -----------------------------------------------------

        # Save final AI report

        # -----------------------------------------------------



        interview.final_summary = (

            report.final_summary

        )



        interview.final_strengths = (

            report.final_strengths

        )



        interview.final_weaknesses = (

            report.final_weaknesses

        )



        interview.technical_assessment = (

            report.technical_assessment

        )



        interview.communication_assessment = (

            report.communication_assessment

        )



        interview.problem_solving_assessment = (

            report.problem_solving_assessment

        )



        interview.final_recommendations = (

            report.final_recommendations

        )



        self.db.flush()



        return interview



    # =========================================================

    # UPDATE INTERVIEW

    # =========================================================



    def update_interview(

        self,

        session_id: int,

        user_id: int,

        interview_data: InterviewUpdate,

    ) -> InterviewSession:



        interview = self.get_interview_by_id(session_id)



        if not interview:

            raise ValueError("Interview not found.")



        if interview.user_id != user_id:

            raise PermissionError(

                "You do not own this interview."

            )



        if interview_data.status is not None:

            interview.status = interview_data.status



        self.db.commit()

        self.db.refresh(interview)



        return interview



    # =========================================================

    # COMPLETE INTERVIEW

    # =========================================================



    def complete_interview(

        self,

        session_id: int,

        user_id: int,

    ) -> InterviewSession:

        """

        Complete an interview safely.



        This method is idempotent:

        if the interview has already been completed, it simply

        returns the completed interview instead of throwing an

        error or attempting to complete it again.

        """



        interview = self.get_interview_by_id(session_id)



        if not interview:

            raise ValueError("Interview not found.")



        if interview.user_id != user_id:

            raise PermissionError(

                "You do not own this interview."

            )



        # -----------------------------------------------------

        # IMPORTANT:

        # If the final answer already completed the interview,

        # do NOT try to complete it again.

        # -----------------------------------------------------



        if interview.status == InterviewStatus.COMPLETED:



            # The interview is already safely completed.

            # Return it without another completion operation.

            return interview



        if interview.status != InterviewStatus.IN_PROGRESS:

            raise ValueError(

                "Only an in-progress interview "

                "can be completed."

            )



        # -----------------------------------------------------

        # Prevent completion while a question is unanswered.

        # -----------------------------------------------------



        if interview.current_question_id is not None:

            raise ValueError(

                "You must answer the current interview question "

                "before completing the interview."

            )



        # -----------------------------------------------------

        # Calculate overall score.

        # -----------------------------------------------------



        overall_score = self._calculate_overall_score(

            interview.id

        )



        if overall_score is None:

            raise ValueError(

                "At least one evaluated answer is required "

                "to complete the interview."

            )



        interview.overall_score = overall_score



        # -----------------------------------------------------

        # Mark completed BEFORE generating Gemini report.

        #

        # This is important because the final report is an

        # additional operation and should not determine whether

        # the interview itself is completed.

        # -----------------------------------------------------



        interview.status = InterviewStatus.COMPLETED



        interview.current_question_id = None



        interview.poor_streak = 0

        interview.strong_streak = 0



        # -----------------------------------------------------

        # Commit the completed interview first.

        # -----------------------------------------------------



        self.db.commit()

        self.db.refresh(interview)



        # -----------------------------------------------------

        # Generate final AI report.

        #

        # If Gemini fails, the interview remains COMPLETED.

        # The result page can retry report generation separately.

        # -----------------------------------------------------



        try:

            self.generate_final_report(interview)



            self.db.commit()

            self.db.refresh(interview)



        except Exception:

            # Do NOT roll back the completed interview state.

            #

            # The overall score and status were already committed.

            # The final report can be generated again later.

            self.db.rollback()



            interview = self.get_interview_by_id(

                session_id

            )



            if not interview:

                raise ValueError(

                    "Interview could not be reloaded "

                    "after completion."

                )



        return interview



    # =========================================================

    # ABANDON INTERVIEW

    # =========================================================



    def abandon_interview(

        self,

        session_id: int,

        user_id: int,

    ) -> InterviewSession:



        interview = self.get_interview_by_id(session_id)



        if not interview:

            raise ValueError("Interview not found.")



        if interview.user_id != user_id:

            raise PermissionError(

                "You do not own this interview."

            )



        # Never change an already completed interview

        # into ABANDONED.

        if interview.status == InterviewStatus.COMPLETED:

            return interview



        if interview.status != InterviewStatus.IN_PROGRESS:

            raise ValueError(

                "Only an in-progress interview "

                "can be abandoned."

            )



        interview.status = InterviewStatus.ABANDONED

        interview.current_question_id = None



        self.db.commit()

        self.db.refresh(interview)



        return interview



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

            Decimal(str(answer.overall_score))

            for answer in answers

        )



        average_score = (

            total_score / Decimal(len(answers))

        )



        return average_score.quantize(

            Decimal("0.01")

        )