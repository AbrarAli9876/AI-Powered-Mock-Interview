import logging
import os
from typing import Any

from google import genai
from google.genai import types

from app.ai.final_report_generator import FinalReportGenerator
from app.ai.final_report_prompts import build_final_report_prompt
from app.ai.prompts import build_evaluation_prompt
from app.config import settings
from app.schemas.evaluation import InterviewEvaluation
from app.schemas.final_report import FinalInterviewReport


logger = logging.getLogger(__name__)


class _FailoverModels:
    """
    Proxy the Google GenAI models API through the failover client.

    This allows FinalReportGenerator to use automatic API key
    failover without changing its existing interface.
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

    API keys are tried in the following order:
        1. GEMINI_EVALUATION_API_KEY from application settings
        2. GEMINI_EVALUATION_API_KEY_2
        3. GEMINI_EVALUATION_API_KEY_3
        4. Additional keys from GEMINI_EVALUATION_API_KEYS

    The next configured key is tried when a request fails with
    a retryable API, network, or temporary provider error.

    API keys are never written to application logs.
    """

    RETRYABLE_STATUSES = {
        401,  # Unauthorized or invalid key
        403,  # Permission or quota-related rejection
        408,  # Request timeout
        429,  # Rate limit or quota exhaustion
        500,  # Internal server error
        502,  # Bad gateway
        503,  # Service unavailable
        504,  # Gateway timeout
    }

    RETRYABLE_PHRASES = (
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
        "connecterror",
        "connection error",
        "connection failed",
        "connection refused",
        "connection reset",
        "getaddrinfo failed",
        "name or service not known",
        "temporary failure in name resolution",
        "failed to resolve",
        "network is unreachable",
        "network error",
    )

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

        # Support additional comma-separated API keys.
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

        # Remove empty keys and duplicates while preserving order.
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

        # Preserve the existing interface expected by the
        # final report generator.
        self.client = _FailoverClient(self)

        logger.info(
            "Gemini evaluation client initialized with "
            "%s configured API key slot(s).",
            len(self.clients),
        )

    @classmethod
    def _is_retryable_error(cls, exc: Exception) -> bool:
        """
        Determine whether another API key should be attempted.

        Handles HTTP status codes, Gemini API errors, and common
        transient network errors.

        Note:
        Trying another key cannot fix persistent DNS or network
        connectivity problems.
        """

        # Check structured status attributes first.
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

        # Normalize numeric strings and integer-like status codes.
        try:
            status_code = int(status_code)
        except (TypeError, ValueError, OverflowError):
            status_code = None

        if status_code in cls.RETRYABLE_STATUSES:
            return True

        message = str(exc).lower()

        # Some SDK/network exceptions wrap their original error.
        if any(
            phrase in message
            for phrase in cls.RETRYABLE_PHRASES
        ):
            return True

        # Check common HTTP status codes in the exception message.
        # Match status-code boundaries to avoid accidental matches
        # inside unrelated numbers.
        import re

        return bool(
            re.search(
                r"(?<!\d)(401|403|408|429|500|502|503|504)(?!\d)",
                message,
            )
        )

    def _generate_content_with_failover(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Execute a Gemini request using configured keys in order.

        Retryable errors cause the next configured key to be tried.
        Non-retryable errors are raised immediately.
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
                        "Gemini request failed using key slot %s. "
                        "Trying fallback key slot %s. "
                        "Error type: %s",
                        key_number,
                        key_number + 1,
                        type(exc).__name__,
                    )
                else:
                    logger.error(
                        "Gemini request failed with a retryable "
                        "error using all %s configured API key "
                        "slot(s). Last error type: %s",
                        len(self.clients),
                        type(exc).__name__,
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
        Evaluate one candidate answer using Gemini.

        Returns a validated InterviewEvaluation instance.
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

        # Prefer the SDK's parsed structured response.
        if response.parsed is not None:
            if isinstance(
                response.parsed,
                InterviewEvaluation,
            ):
                return response.parsed

            return InterviewEvaluation.model_validate(
                response.parsed
            )

        # Fall back to validating the JSON response text.
        response_text = response.text

        if not response_text or not response_text.strip():
            raise ValueError(
                "Gemini returned an empty answer evaluation."
            )

        return InterviewEvaluation.model_validate_json(
            response_text
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
        Generate the final interview report using Gemini
        with automatic API key failover.
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