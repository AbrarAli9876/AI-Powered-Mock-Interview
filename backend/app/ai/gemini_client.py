
import logging
import os
from typing import Any

from google import genai
from google.genai import types

from app.ai.final_report_generator import FinalReportGenerator
from app.ai.final_report_prompts import (
    build_final_report_prompt,
)
from app.ai.prompts import build_evaluation_prompt
from app.config import settings
from app.schemas.evaluation import InterviewEvaluation
from app.schemas.final_report import FinalInterviewReport


logger = logging.getLogger(__name__)


class _FailoverModels:
    """
    Proxy the Google GenAI models API through the failover client.

    This also allows FinalReportGenerator to use automatic key
    rotation without needing to change its existing interface.
    """

    def __init__(self, owner: "GeminiEvaluationClient"):
        self._owner = owner

    def generate_content(self, **kwargs: Any) -> Any:
        return self._owner._generate_content_with_failover(
            **kwargs
        )


class _FailoverClient:
    """
    Minimal client adapter used by FinalReportGenerator.
    """

    def __init__(self, owner: "GeminiEvaluationClient"):
        self.models = _FailoverModels(owner)


class GeminiEvaluationClient:
    """
    Evaluates interview answers and generates final reports.

    API keys are tried in order:
        1. GEMINI_EVALUATION_API_KEY
        2. GEMINI_EVALUATION_API_KEY_2
        3. GEMINI_EVALUATION_API_KEY_3

    On a retryable Gemini API error, the same request is
    immediately attempted with the next configured key.
    """

    def __init__(self):
        primary_key = getattr(
            settings,
            "GEMINI_EVALUATION_API_KEY",
            None,
        )

        configured_keys = [
            primary_key,
            os.getenv("GEMINI_EVALUATION_API_KEY_2"),
            os.getenv("GEMINI_EVALUATION_API_KEY_3"),
        ]

        # Also support an optional comma-separated environment
        # variable for deployments that prefer a single setting.
        extra_keys = os.getenv(
            "GEMINI_EVALUATION_API_KEYS",
            "",
        )

        if extra_keys:
            configured_keys.extend(
                key.strip()
                for key in extra_keys.split(",")
                if key.strip()
            )

        # Remove empty values and duplicate keys while preserving
        # the configured order.
        self.api_keys = list(
            dict.fromkeys(
                key.strip()
                for key in configured_keys
                if isinstance(key, str) and key.strip()
            )
        )

        if not self.api_keys:
            raise RuntimeError(
                "No Gemini evaluation API keys are configured. "
                "Set GEMINI_EVALUATION_API_KEY in the backend "
                "environment."
            )

        self.clients = [
            genai.Client(api_key=key)
            for key in self.api_keys
        ]

        self.model = settings.GEMINI_EVALUATION_MODEL

        # Preserve the existing client.models interface.
        self.client = _FailoverClient(self)

    @staticmethod
    def _is_retryable_error(exc: Exception) -> bool:
        """
        Return True when trying another API key may help.

        Quota exhaustion, rate limiting, authentication errors,
        and temporary provider errors are eligible for failover.
        """

        message = str(exc).lower()

        retryable_statuses = {
            401,  # Invalid or unauthorized key
            403,  # Permission/quota-related rejection
            408,  # Request timeout
            429,  # Rate limit or quota exhausted
            500,  # Internal provider error
            502,  # Bad gateway
            503,  # Service unavailable
            504,  # Gateway timeout
        }

        status_code = getattr(
            exc,
            "status_code",
            None,
        )

        if status_code is None:
            status_code = getattr(
                exc,
                "code",
                None,
            )

        if status_code in retryable_statuses:
            return True

        retryable_phrases = (
            "resource_exhausted",
            "quota exceeded",
            "quota has been exceeded",
            "rate limit",
            "rate_limit",
            "too many requests",
            "api key not valid",
            "invalid api key",
            "permission denied",
            "unauthorized",
            "service unavailable",
            "temporarily unavailable",
            "internal server error",
            "deadline exceeded",
            "timed out",
            "timeout",
            "503",
            "502",
            "504",
            "429",
            "401",
            "403",
        )

        return any(
            phrase in message
            for phrase in retryable_phrases
        )

    def _generate_content_with_failover(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Run one Gemini request and switch keys on retryable errors.

        No API key values are included in logs or exceptions.
        """

        last_error = None

        for index, client in enumerate(self.clients):
            key_number = index + 1

            try:
                response = client.models.generate_content(
                    **kwargs
                )

                if index > 0:
                    logger.info(
                        "Gemini request succeeded using "
                        "fallback API key slot %s.",
                        key_number,
                    )

                return response

            except Exception as exc:
                last_error = exc

                if not self._is_retryable_error(exc):
                    logger.exception(
                        "Gemini request failed with a "
                        "non-retryable error using key slot %s.",
                        key_number,
                    )
                    raise

                if index + 1 < len(self.clients):
                    logger.warning(
                        "Gemini request failed with a retryable "
                        "error using key slot %s. Switching to "
                        "key slot %s.",
                        key_number,
                        key_number + 1,
                    )
                else:
                    logger.error(
                        "Gemini request failed with a "
                        "retryable error using all %s configured "
                        "API key slots.",
                        len(self.clients),
                    )

        if last_error is not None:
            raise last_error

        raise RuntimeError(
            "Gemini request failed because no API keys "
            "were available."
        )

    def evaluate_answer(
        self,
        question: str,
        expected_answer: str,
        candidate_answer: str,
    ) -> InterviewEvaluation:
        """
        Evaluate one candidate answer with automatic key failover.
        """

        prompt = build_evaluation_prompt(
            question=question,
            expected_answer=expected_answer,
            candidate_answer=candidate_answer,
        )

        response = self._generate_content_with_failover(
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

        if not response.text:
            raise ValueError(
                "Gemini returned an empty answer evaluation."
            )

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
        Generate the final AI interview report with automatic
        API key failover.
        """

        prompt = build_final_report_prompt(
            topic=topic,
            starting_difficulty=starting_difficulty,
            final_difficulty=final_difficulty,
            overall_score=overall_score,
            difficulty_progression=difficulty_progression,
            answers_text=answers_text,
        )

        generator = FinalReportGenerator(
            client=self.client,
            model=self.model,
        )

        return generator.generate(prompt)
