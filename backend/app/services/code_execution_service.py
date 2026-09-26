from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from app.enums.coding_language import CodingLanguage
from app.models.coding_question import CodingQuestion
from app.schemas.code_execution import (
    CodeExecutionResponse,
    TestCaseResult,
)


class CodeExecutionService:
    """
    Executes candidate coding solutions locally using subprocess.

    Docker is intentionally not used.

    The candidate code is written to a temporary file and executed
    using the Python interpreter from the currently active environment.
    """

    TIMEOUT_SECONDS = 5

    MAX_OUTPUT_LENGTH = 10000

    LANGUAGE_CONFIG = {
        CodingLanguage.PYTHON: {
            "filename": "main.py",
            "command": [sys.executable],
        },
    }

    def execute(
        self,
        question: CodingQuestion,
        code: str,
    ) -> CodeExecutionResponse:
        """
        Execute candidate code against all configured test cases.
        """

        language = question.language

        if language not in self.LANGUAGE_CONFIG:
            raise ValueError(
                f"Code execution for "
                f"{language.value} is not available yet."
            )

        config = self.LANGUAGE_CONFIG[language]

        if not code or not code.strip():
            raise ValueError(
                "Code cannot be empty."
            )

        if not question.test_cases:
            raise ValueError(
                "No test cases are configured "
                "for this coding question."
            )

        results: list[TestCaseResult] = []

        passed_count = 0

        with tempfile.TemporaryDirectory(
            prefix="ai_mock_interview_"
        ) as temp_dir:

            temp_path = Path(temp_dir)

            source_file = (
                temp_path / config["filename"]
            )

            try:
                source_file.write_text(
                    code,
                    encoding="utf-8",
                )

            except OSError as exc:
                raise RuntimeError(
                    "Unable to create the temporary "
                    f"source file: {exc}"
                ) from exc

            for index, test_case in enumerate(
                question.test_cases,
                start=1,
            ):
                result = self._run_test_case(
                    source_file=source_file,
                    input_data=test_case.input_data,
                    expected_output=(
                        test_case.expected_output
                    ),
                    index=index,
                    config=config,
                    working_directory=temp_path,
                )

                results.append(result)

                if result.passed:
                    passed_count += 1

        total = len(results)

        return CodeExecutionResponse(
            success=(
                total > 0
                and passed_count == total
            ),
            language=language.value,
            total_test_cases=total,
            passed_test_cases=passed_count,
            failed_test_cases=(
                total - passed_count
            ),
            results=results,
        )

    def _run_test_case(
        self,
        source_file: Path,
        input_data: str,
        expected_output: str,
        index: int,
        config: dict,
        working_directory: Path,
    ) -> TestCaseResult:
        """
        Execute one test case using a local subprocess.
        """

        command = [
            *config["command"],
            str(source_file),
        ]

        start_time = time.perf_counter()

        environment = self._build_environment()

        try:
            process = subprocess.run(
                command,
                input=input_data,
                text=True,
                capture_output=True,
                timeout=self.TIMEOUT_SECONDS,
                cwd=str(working_directory),
                env=environment,
                check=False,
            )

            execution_time_ms = (
                time.perf_counter()
                - start_time
            ) * 1000

            actual_output = (
                process.stdout or ""
            ).strip()

            expected = (
                expected_output or ""
            ).strip()

            stderr_output = (
                process.stderr or ""
            ).strip()

            if process.returncode != 0:
                error = (
                    stderr_output
                    or "Code execution failed."
                )

                return TestCaseResult(
                    test_case_number=index,
                    passed=False,
                    input_data=input_data,
                    expected_output=expected,
                    actual_output=actual_output,
                    error=(
                        self._limit_output(error)
                    ),
                    execution_time_ms=(
                        execution_time_ms
                    ),
                )

            passed = (
                actual_output == expected
            )

            return TestCaseResult(
                test_case_number=index,
                passed=passed,
                input_data=input_data,
                expected_output=expected,
                actual_output=(
                    self._limit_output(
                        actual_output
                    )
                ),
                error=(
                    None
                    if passed
                    else (
                        "Output does not match "
                        "expected output."
                    )
                ),
                execution_time_ms=(
                    execution_time_ms
                ),
            )

        except subprocess.TimeoutExpired:
            execution_time_ms = (
                time.perf_counter()
                - start_time
            ) * 1000

            return TestCaseResult(
                test_case_number=index,
                passed=False,
                input_data=input_data,
                expected_output=(
                    expected_output.strip()
                    if expected_output
                    else ""
                ),
                actual_output="",
                error=(
                    f"Execution timed out after "
                    f"{self.TIMEOUT_SECONDS} seconds."
                ),
                execution_time_ms=(
                    execution_time_ms
                ),
            )

        except FileNotFoundError as exc:
            raise RuntimeError(
                "Python executable could not be found."
            ) from exc

        except PermissionError as exc:
            raise RuntimeError(
                "Permission denied while "
                "executing the candidate code."
            ) from exc

        except OSError as exc:
            raise RuntimeError(
                f"Unable to execute candidate code: {exc}"
            ) from exc

    @staticmethod
    def _build_environment() -> dict[str, str]:
        """
        Build a controlled environment for candidate execution.

        The candidate program receives a minimal environment instead
        of inheriting the complete backend environment.
        """

        environment = {
            "PATH": os.environ.get(
                "PATH",
                "",
            ),
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        }

        return environment

    def _limit_output(
        self,
        output: str,
    ) -> str:
        """
        Prevent extremely large program output from
        being returned to the frontend.
        """

        if len(output) <= self.MAX_OUTPUT_LENGTH:
            return output

        return (
            output[: self.MAX_OUTPUT_LENGTH]
            + "\n\n[Output truncated.]"
        )