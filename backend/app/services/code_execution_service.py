from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from app.enums.coding_language import CodingLanguage
from app.models.coding_question import CodingQuestion
from app.schemas.code_execution import CodeExecutionResponse, TestCaseResult


class CodeExecutionService:
    """
    Local coding-question runner.

    Supported:
      - Python: current Python interpreter
      - JavaScript: Node.js
      - Java: javac + java (source must define Main)
      - C++: g++ (source must define main)
      - SQL: SQLite in-memory database; each test case's input_data is SQL setup
             SQL and the submitted code is the query to execute.

    SECURITY:
      This uses subprocess without OS/container sandboxing. Do not expose it to
      untrusted public submissions in production without strong isolation,
      resource limits, and network/filesystem restrictions.
    """

    TIMEOUT_SECONDS = 5
    COMPILE_TIMEOUT_SECONDS = 10
    MAX_OUTPUT_LENGTH = 10_000

    # Enum keys are used where available; normalized strings are also supported.
    LANGUAGE_CONFIG = {
        "python": {"filename": "main.py", "kind": "script", "command": [sys.executable]},
        "javascript": {"filename": "main.js", "kind": "script", "command": ["node"]},
        "java": {"filename": "Main.java", "kind": "java", "command": ["java"]},
        "cpp": {"filename": "main.cpp", "kind": "cpp", "command": ["g++"]},
        "c++": {"filename": "main.cpp", "kind": "cpp", "command": ["g++"]},
        "sql": {"filename": "", "kind": "sql", "command": []},
    }

    @staticmethod
    def _language_name(language: Any) -> str:
        value = getattr(language, "value", language)
        value = str(value).strip().lower()
        aliases = {
            "py": "python",
            "js": "javascript",
            "node": "javascript",
            "cxx": "cpp",
            "c plus plus": "cpp",
            "sqlite": "sql",
        }
        return aliases.get(value, value)

    def execute(self, question: CodingQuestion, code: str) -> CodeExecutionResponse:
        language = self._language_name(question.language)
        config = self.LANGUAGE_CONFIG.get(language)

        if config is None:
            raise ValueError(
                f"Code execution for {language} is not available. "
                "Supported: Python, JavaScript, Java, C++, SQL."
            )
        if not code or not code.strip():
            raise ValueError("Code cannot be empty.")
        if not question.test_cases:
            raise ValueError("No test cases are configured for this coding question.")

        if config["kind"] == "sql":
            return self._execute_sql(question, code, language)

        results: list[TestCaseResult] = []
        with tempfile.TemporaryDirectory(prefix="ai_mock_interview_") as temp_dir:
            workdir = Path(temp_dir)
            source_file = workdir / config["filename"]
            source_file.write_text(code, encoding="utf-8")

            command_prefix = self._prepare_command(config, source_file, workdir)
            # Compilation is done once per submission, then run for each test case.
            if config["kind"] in {"java", "cpp"}:
                compile_command = self._compile_command(config, source_file, workdir)
                compiler = self._resolve_executable(compile_command[0])
                if compiler is None:
                    raise RuntimeError(self._compiler_not_found_message(compile_command[0]))
                compile_start = time.perf_counter()
                try:
                    compiled = subprocess.run(
                        [compiler, *compile_command[1:]],
                        text=True,
                        capture_output=True,
                        timeout=self.COMPILE_TIMEOUT_SECONDS,
                        cwd=str(workdir),
                        env=self._build_environment(),
                        check=False,
                    )
                except subprocess.TimeoutExpired:
                    return self._compile_failure_response(
                        language, question.test_cases, "Compilation timed out."
                    )
                compile_ms = (time.perf_counter() - compile_start) * 1000
                if compiled.returncode != 0:
                    error = self._limit_output((compiled.stderr or compiled.stdout or "Compilation failed.").strip())
                    return self._compile_failure_response(language, question.test_cases, error, compile_ms)

            for index, test_case in enumerate(question.test_cases, start=1):
                result = self._run_test_case(
                    command=command_prefix,
                    input_data=test_case.input_data or "",
                    expected_output=test_case.expected_output or "",
                    index=index,
                    working_directory=workdir,
                )
                results.append(result)

        passed = sum(item.passed for item in results)
        total = len(results)
        return CodeExecutionResponse(
            success=total > 0 and passed == total,
            language=language,
            total_test_cases=total,
            passed_test_cases=passed,
            failed_test_cases=total - passed,
            results=results,
        )

    @staticmethod
    def _resolve_executable(name: str) -> str | None:
        """
        Resolve an executable using PATH, JAVA_HOME, and common Windows JDK
        installation locations. This also handles a backend started before
        Windows environment-variable changes were picked up.
        """
        executable_names = [name]
        if os.name == "nt" and not name.lower().endswith(".exe"):
            executable_names.insert(0, f"{name}.exe")

        # First use the current process PATH.
        for executable_name in executable_names:
            resolved = shutil.which(executable_name)
            if resolved:
                return str(Path(resolved))

        # Next, check JAVA_HOME, which may be configured even if PATH is stale.
        java_home = os.environ.get("JAVA_HOME")
        if java_home:
            for executable_name in executable_names:
                candidate = Path(java_home) / "bin" / executable_name
                if candidate.is_file():
                    return str(candidate)

        # On Windows, check the standard per-user Eclipse Temurin location.
        if os.name == "nt":
            local_app_data = os.environ.get("LOCALAPPDATA")
            if local_app_data:
                adoptium_dir = Path(local_app_data) / "Programs" / "Eclipse Adoptium"
                if adoptium_dir.is_dir():
                    for candidate_dir in sorted(adoptium_dir.glob("jdk*"), reverse=True):
                        for executable_name in executable_names:
                            candidate = candidate_dir / "bin" / executable_name
                            if candidate.is_file():
                                return str(candidate)

        return None

    @staticmethod
    def _compiler_not_found_message(executable: str) -> str:
        if executable.lower() in {"javac", "javac.exe", "java", "java.exe"}:
            return (
                f"Required Java executable '{executable}' could not be resolved. "
                "Set JAVA_HOME to your JDK folder and ensure its bin folder is on PATH, "
                "then restart the backend."
            )
        return (
            f"Required compiler '{executable}' was not found on PATH. "
            "Install the appropriate C++ compiler and restart the backend."
        )

    def _prepare_command(self, config: dict, source_file: Path, workdir: Path) -> list[str]:
        kind = config["kind"]
        if kind == "java":
            if "class Main" not in source_file.read_text(encoding="utf-8"):
                raise ValueError("Java solution must define a class named Main.")
            java_executable = self._resolve_executable("java")
            if java_executable is None:
                raise RuntimeError(self._compiler_not_found_message("java"))
            return [java_executable, "-Dfile.encoding=UTF-8", "-cp", str(workdir), "Main"]
        if kind == "cpp":
            return [str(workdir / "main_program.exe" if os.name == "nt" else workdir / "main_program")]
        return [*config["command"], str(source_file)]

    def _compile_command(self, config: dict, source_file: Path, workdir: Path) -> list[str]:
        if config["kind"] == "java":
            return ["javac", "-encoding", "UTF-8", str(source_file)]
        if config["kind"] == "cpp":
            output = workdir / ("main_program.exe" if os.name == "nt" else "main_program")
            return ["g++", "-std=c++17", "-O2", "-pipe", str(source_file), "-o", str(output)]
        raise ValueError("Unsupported compilation language.")

    def _run_test_case(
        self, command: list[str], input_data: str, expected_output: str,
        index: int, working_directory: Path,
    ) -> TestCaseResult:
        start = time.perf_counter()
        try:
            process = subprocess.run(
                command,
                input=input_data,
                text=True,
                capture_output=True,
                timeout=self.TIMEOUT_SECONDS,
                cwd=str(working_directory),
                env=self._build_environment(),
                check=False,
            )
            elapsed = (time.perf_counter() - start) * 1000
            actual = (process.stdout or "").strip()
            expected = (expected_output or "").strip()
            stderr = (process.stderr or "").strip()
            if process.returncode != 0:
                return TestCaseResult(
                    test_case_number=index, passed=False, input_data=input_data,
                    expected_output=expected, actual_output=self._limit_output(actual),
                    error=self._limit_output(stderr or f"Program exited with code {process.returncode}."),
                    execution_time_ms=elapsed,
                )
            passed = self._normalize_output(actual) == self._normalize_output(expected)
            return TestCaseResult(
                test_case_number=index, passed=passed, input_data=input_data,
                expected_output=expected, actual_output=self._limit_output(actual),
                error=None if passed else "Output does not match expected output.",
                execution_time_ms=elapsed,
            )
        except subprocess.TimeoutExpired:
            elapsed = (time.perf_counter() - start) * 1000
            return TestCaseResult(
                test_case_number=index, passed=False, input_data=input_data,
                expected_output=(expected_output or "").strip(), actual_output="",
                error=f"Execution timed out after {self.TIMEOUT_SECONDS} seconds.",
                execution_time_ms=elapsed,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"Required runtime '{command[0]}' was not found. Install it and ensure it is on PATH."
            ) from exc
        except OSError as exc:
            raise RuntimeError(f"Unable to execute candidate code: {exc}") from exc

    def _execute_sql(self, question: CodingQuestion, code: str, language: str) -> CodeExecutionResponse:
        results: list[TestCaseResult] = []
        for index, test_case in enumerate(question.test_cases, start=1):
            start = time.perf_counter()
            actual = ""
            error = None
            passed = False
            try:
                # Each test case gets a fresh in-memory SQLite database.
                connection = sqlite3.connect(":memory:")
                try:
                    connection.executescript(test_case.input_data or "")
                    cursor = connection.execute(code)
                    rows = cursor.fetchall() if cursor.description else []
                    actual = "\n".join(" ".join("" if value is None else str(value) for value in row) for row in rows)
                    expected = (test_case.expected_output or "").strip()
                    passed = self._normalize_output(actual) == self._normalize_output(expected)
                    if not passed:
                        error = "Query output does not match expected output."
                finally:
                    connection.close()
            except sqlite3.Error as exc:
                error = self._limit_output(str(exc))
                expected = (test_case.expected_output or "").strip()
            results.append(TestCaseResult(
                test_case_number=index,
                passed=passed,
                input_data=test_case.input_data or "",
                expected_output=expected,
                actual_output=self._limit_output(actual),
                error=error,
                execution_time_ms=(time.perf_counter() - start) * 1000,
            ))
        passed_count = sum(item.passed for item in results)
        total = len(results)
        return CodeExecutionResponse(
            success=total > 0 and passed_count == total,
            language=language,
            total_test_cases=total,
            passed_test_cases=passed_count,
            failed_test_cases=total - passed_count,
            results=results,
        )

    def _compile_failure_response(
        self, language: str, test_cases: list, error: str, compile_ms: float = 0,
    ) -> CodeExecutionResponse:
        results = [
            TestCaseResult(
                test_case_number=index,
                passed=False,
                input_data=case.input_data or "",
                expected_output=(case.expected_output or "").strip(),
                actual_output="",
                error=self._limit_output(error),
                execution_time_ms=compile_ms,
            )
            for index, case in enumerate(test_cases, start=1)
        ]
        return CodeExecutionResponse(
            success=False, language=language, total_test_cases=len(results),
            passed_test_cases=0, failed_test_cases=len(results), results=results,
        )

    @staticmethod
    def _normalize_output(value: str) -> str:
        # Ignore insignificant whitespace differences, including line wrapping.
        return " ".join((value or "").strip().split())

    @classmethod
    def _build_environment(cls) -> dict[str, str]:
        # Preserve the parent PATH and prepend the JDK bin directory when found.
        path_entries = [entry for entry in os.environ.get("PATH", "").split(os.pathsep) if entry]
        java_executable = cls._resolve_executable("java")
        javac_executable = cls._resolve_executable("javac")
        for executable in (java_executable, javac_executable):
            if executable:
                bin_dir = str(Path(executable).parent)
                if bin_dir not in path_entries:
                    path_entries.insert(0, bin_dir)

        java_home = os.environ.get("JAVA_HOME")
        if java_home:
            java_bin = str(Path(java_home) / "bin")
            if java_bin not in path_entries:
                path_entries.insert(0, java_bin)

        env = {
            "PATH": os.pathsep.join(path_entries),
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        # Keep required Windows variables if present.
        for variable in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP", "USERPROFILE"):
            value = os.environ.get(variable)
            if value:
                env[variable] = value
        return env

    def _limit_output(self, output: str) -> str:
        if len(output) <= self.MAX_OUTPUT_LENGTH:
            return output
        return output[:self.MAX_OUTPUT_LENGTH] + "\n\n[Output truncated.]"
