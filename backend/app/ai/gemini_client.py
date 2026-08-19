from google import genai
from google.genai import types

from app.ai.final_report_prompts import (
    build_final_report_prompt,
)
from app.ai.prompts import build_evaluation_prompt
from app.config import settings
from app.schemas.evaluation import InterviewEvaluation
from app.schemas.final_report import FinalInterviewReport


class GeminiEvaluationClient:
    """
    Client responsible for evaluating interview answers
    and generating final interview reports using Gemini.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_EVALUATION_API_KEY,
        )

        self.model = settings.GEMINI_EVALUATION_MODEL

    def evaluate_answer(
        self,
        question: str,
        expected_answer: str,
        candidate_answer: str,
    ) -> InterviewEvaluation:
        """
        Evaluate one candidate answer.
        """

        prompt = build_evaluation_prompt(
            question=question,
            expected_answer=expected_answer,
            candidate_answer=candidate_answer,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=InterviewEvaluation,
                temperature=0.2,
            ),
        )

        if response.parsed is not None:
            return response.parsed

        return InterviewEvaluation.model_validate_json(
            response.text
        )

    def generate_final_report(
        self,
        topic: str,
        starting_difficulty: str,
        final_difficulty: str,
        overall_score: float,
        difficulty_progression: str,
        answers_text: str,
    ) -> FinalInterviewReport:
        """
        Generate the final AI-powered interview report.
        """

        prompt = build_final_report_prompt(
            topic=topic,
            starting_difficulty=starting_difficulty,
            final_difficulty=final_difficulty,
            overall_score=overall_score,
            difficulty_progression=difficulty_progression,
            answers_text=answers_text,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=FinalInterviewReport,
                temperature=0.2,
            ),
        )

        if response.parsed is not None:
            return response.parsed

        return FinalInterviewReport.model_validate_json(
            response.text
        )