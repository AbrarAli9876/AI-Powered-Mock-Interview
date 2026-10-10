"""Robust Gemini final-report generation.

The answer evaluator uses structured Gemini output successfully, but final
reports are larger and contain more free-form text.  This module deliberately
uses JSON mode first instead of relying on Gemini's structured-output schema.
That makes final-report generation more tolerant of model/SDK differences.
"""

import json
import re
from typing import Any

from google import genai
from google.genai import types

from app.schemas.final_report import FinalInterviewReport


class FinalReportGenerator:
    """Generate and validate a final technical-interview report."""

    REQUIRED_FIELDS = (
        "final_summary",
        "final_strengths",
        "final_weaknesses",
        "technical_assessment",
        "communication_assessment",
        "problem_solving_assessment",
        "final_recommendations",
    )

    def __init__(self, client: genai.Client, model: str):
        self.client = client
        self.model = model

    def generate(self, prompt: str) -> FinalInterviewReport:
        """Generate a report with a JSON-first strategy and a safe fallback."""
        errors: list[str] = []

        # Attempt 1: JSON mode without response_schema.  This avoids failures
        # caused by structured-output schema support on a particular model.
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                    max_output_tokens=4096,
                ),
            )
            report = self._parse_response(response)
            if report:
                return report
            errors.append("Gemini returned an empty or invalid JSON report.")
        except Exception as exc:
            errors.append(f"JSON-mode generation failed: {exc}")

        # Attempt 2: plain text generation with an even stricter JSON-only
        # instruction.  This is useful when a model rejects JSON MIME mode.
        fallback_prompt = (
            prompt
            + "\n\nFINAL OUTPUT REQUIREMENT:\n"
            "Return ONLY one valid JSON object. Do not use markdown fences. "
            "Do not add commentary before or after the JSON. "
            "Every required field must contain a non-empty string."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=fallback_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=4096,
                ),
            )
            report = self._parse_response(response)
            if report:
                return report
            errors.append("Fallback generation returned invalid JSON.")
        except Exception as exc:
            errors.append(f"Fallback generation failed: {exc}")

        raise RuntimeError(
            "Gemini could not generate a valid final interview report. "
            + " | ".join(errors)
        )

    def _parse_response(self, response: Any) -> FinalInterviewReport | None:
        parsed = getattr(response, "parsed", None)
        if isinstance(parsed, FinalInterviewReport):
            return parsed

        text = getattr(response, "text", None)
        if not text or not text.strip():
            return None

        data = self._extract_json(text)
        if not isinstance(data, dict):
            return None

        # Reject incomplete reports instead of silently saving partial data.
        if any(
            not isinstance(data.get(field), str)
            or not data[field].strip()
            for field in self.REQUIRED_FIELDS
        ):
            return None

        return FinalInterviewReport.model_validate(data)

    @staticmethod
    def _extract_json(text: str) -> dict[str, Any] | None:
        cleaned = text.strip()

        # Handle accidental markdown code fences.
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = cleaned.strip()

        try:
            value = json.loads(cleaned)
            return value if isinstance(value, dict) else None
        except json.JSONDecodeError:
            pass

        # Last-resort extraction if the model added a sentence around JSON.
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start < 0 or end <= start:
            return None

        try:
            value = json.loads(cleaned[start : end + 1])
            return value if isinstance(value, dict) else None
        except json.JSONDecodeError:
            return None
