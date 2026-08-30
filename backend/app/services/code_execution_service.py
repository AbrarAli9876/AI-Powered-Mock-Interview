from __future__ import annotations

import subprocess
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
    Executes candidate code inside an isolated Docker container.
    """

    TIMEOUT_SECONDS = 5

    MEMORY_LIMIT = "128m"

    CPU_LIMIT = "0.5"

    LANGUAGE_CONFIG = {
        CodingLanguage.PYTHON: {
            "image": "python:3.12-slim",
            "filename": "main.py",
            "command": [
                "python",
                "/code/main.py",
            ],
        },
    }

    def execute(
        self,
        question: CodingQuestion,
        code: str,
    ) -> CodeExecutionResponse:
        """
        Execute candidate code against all test cases.
        """

        language = question.language

        if language not in self.LANGUAGE_CONFIG:
            raise ValueError(
                f"Code execution for "
                f"{language.value} is not available yet."
            )

        config = self.LANGUAGE_CONFIG[language]

        if not question.test_cases:
            raise ValueError(
                "No test cases are configured "
                "for this coding question."
            )

        results: list[TestCaseResult] = []

        passed_count = 0

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_path = Path(temp_dir)

            source_file = (
                temp_path /
                config["filename"]
            )

            source_file.write_text(
                code,
                encoding="utf-8",
            )

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
                )

                results.append(result)

                if result.passed:
                    passed_count += 1

        total = len(results)

        return CodeExecutionResponse(
            success=passed_count == total,
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
    ) -> TestCaseResult:
        """
        Run one test case inside Docker.
        """

        command = [
            "docker",
            "run",
            "--rm",

            "--network",
            "none",

            "--memory",
            self.MEMORY_LIMIT,

            "--cpus",
            self.CPU_LIMIT,

            "--pids-limit",
            "64",

            "--read-only",

            "--tmpfs",
            "/tmp:rw,noexec,nosuid,size=16m",

            "-v",
            f"{source_file.parent}:/code:ro",

            config["image"],
        ]

        command.extend(
            config["command"]
        )

        start_time = time.perf_counter()

        try:
            process = subprocess.run(
                command,
                input=input_data,
                text=True,
                capture_output=True,
                timeout=self.TIMEOUT_SECONDS,
                check=False,
            )

            execution_time_ms = (
                time.perf_counter()
                - start_time
            ) * 1000

            actual_output = (
                process.stdout.strip()
            )

            expected = (
                expected_output.strip()
            )

            if process.returncode != 0:
                error = (
                    process.stderr.strip()
                    or "Code execution failed."
                )

                return TestCaseResult(
                    test_case_number=index,
                    passed=False,
                    input_data=input_data,
                    expected_output=expected,
                    actual_output=actual_output,
                    error=error,
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
                actual_output=actual_output,
                error=(
                    None
                    if passed
                    else "Output does not match expected output."
                ),
                execution_time_ms=(
                    execution_time_ms
                ),
            )

        except subprocess.TimeoutExpired:

            return TestCaseResult(
                test_case_number=index,
                passed=False,
                input_data=input_data,
                expected_output=(
                    expected_output.strip()
                ),
                actual_output="",
                error=(
                    "Execution timed out."
                ),
                execution_time_ms=(
                    self.TIMEOUT_SECONDS * 1000
                ),
            )

        except FileNotFoundError:

            raise RuntimeError(
                "Docker is not installed or "
                "is not available in PATH."
            )