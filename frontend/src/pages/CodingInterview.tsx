import {
  useEffect,
  useMemo,
  useState,
} from "react";
import Editor from "@monaco-editor/react";
import {
  useLocation,
  useNavigate,
} from "react-router-dom";

import {
  abandonCodingInterview,
  getCodingInterview,
  getCodingInterviewResult,
  getCurrentCodingQuestion,
  getNextCodingQuestion,
  skipCodingQuestion,
  runCode,
  submitCodingAnswer,
  type CodingInterview,
  type CodingInterviewQuestionResponse,
  type CodingInterviewResult,
  type CodingLanguage,
  type CodingQuestion,
  type CodeExecutionResponse,
  type Difficulty,
} from "../lib/api";
import {
  getInterviewCameraStream,
  getInterviewDisplayStream,
  stopInterviewSetupMedia,
} from "../lib/interviewMedia";

interface CodingInterviewState {
  sessionId?: number;
  language: CodingLanguage;
  difficulty: Difficulty;
  questionCount?: number;

  questions?: CodingQuestion[];
}

const LANGUAGE_LABELS: Record<
  CodingLanguage,
  string
> = {
  python: "Python",
  javascript: "JavaScript",
  java: "Java",
  cpp: "C++",
};

const DIFFICULTY_LABELS: Record<
  Difficulty,
  string
> = {
  easy: "Easy",
  medium: "Medium",
  hard: "Hard",
};

function formatExamples(
  examples: string,
): {
  input: string;
  output: string;
}[] {
  if (!examples) {
    return [];
  }

  try {
    const parsed = JSON.parse(examples);

    if (Array.isArray(parsed)) {
      return parsed.map(
        (example) => ({
          input: String(
            example.input ??
            example.Input ??
            "",
          ),

          output: String(
            example.output ??
            example.Output ??
            "",
          ),
        }),
      );
    }

    return [
      {
        input: String(
          parsed.input ??
          parsed.Input ??
          "",
        ),

        output: String(
          parsed.output ??
          parsed.Output ??
          "",
        ),
      },
    ];
  } catch {
    return [
      {
        input: examples,
        output: "",
      },
    ];
  }
}

export default function CodingInterview() {
  const navigate = useNavigate();

  const location = useLocation();

  const interviewState =
    location.state as
      | CodingInterviewState
      | null;

  const initialSessionId =
    interviewState?.sessionId;

  const [
    sessionId,
    setSessionId,
  ] = useState<number | null>(
    initialSessionId ?? null,
  );

  const [
    interview,
    setInterview,
  ] = useState<CodingInterview | null>(
    null,
  );

  const [
    currentQuestionData,
    setCurrentQuestionData,
  ] = useState<
    CodingInterviewQuestionResponse | null
  >(null);

  const currentQuestion =
    currentQuestionData?.question ?? null;

  const [
    code,
    setCode,
  ] = useState("");

  const [
    isRunning,
    setIsRunning,
  ] = useState(false);

  const [
    executionResult,
    setExecutionResult,
  ] = useState<
    CodeExecutionResponse | null
  >(null);

  const allTestsPassed =
    executionResult !== null &&
    executionResult.success &&
    executionResult.total_test_cases > 0 &&
    executionResult.passed_test_cases ===
      executionResult.total_test_cases;

  const [
    isSubmitting,
    setIsSubmitting,
  ] = useState(false);

  const [
    isSubmitted,
    setIsSubmitted,
  ] = useState(false);

  const [
    submitResult,
    setSubmitResult,
  ] = useState<{
    success: boolean;
    passed: number;
    total: number;
    score?: number;
    isLastQuestion: boolean;
  } | null>(null);

  const [
    isLoading,
    setIsLoading,
  ] = useState(true);

  const [
    isLoadingNext,
    setIsLoadingNext,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState<string | null>(null);

  const [
    showExitConfirmation,
    setShowExitConfirmation,
  ] = useState(false);

  const [
    isLoadingResult,
    setIsLoadingResult,
  ] = useState(false);

  const examples = useMemo(
    () =>
      currentQuestion
        ? formatExamples(
            currentQuestion.examples,
          )
        : [],
    [currentQuestion],
  );

  useEffect(() => {
    if (!interviewState) {
      navigate(
        "/coding-interview/setup",
        {
          replace: true,
        },
      );

      return;
    }

    if (!initialSessionId) {
      setError(
        "Coding interview session was not found. Please start a new interview.",
      );

      setIsLoading(false);
    }
  }, [
    interviewState,
    initialSessionId,
    navigate,
  ]);

  useEffect(() => {
    if (sessionId === null) {
      return;
    }

    const id = sessionId;

    let cancelled = false;

    async function loadInterview() {
      try {
        setIsLoading(true);
        setError(null);

        const [
          interviewData,
          questionData,
        ] = await Promise.all([
          getCodingInterview(
            id,
          ),

          getCurrentCodingQuestion(
            id,
          ),
        ]);

        if (cancelled) {
          return;
        }

        setInterview(
          interviewData,
        );

        setCurrentQuestionData(
          questionData,
        );

        setCode(
          questionData.question
            .starter_code || "",
        );

        setExecutionResult(
          null,
        );

        setSubmitResult(
          null,
        );

        setIsSubmitted(false);
      } catch (err) {
        if (cancelled) {
          return;
        }

        setError(
          err instanceof Error
            ? err.message
            : "Unable to load the coding interview.",
        );
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void loadInterview();

    return () => {
      cancelled = true;
    };
  }, [sessionId]);

  useEffect(() => {
    if (!currentQuestion) {
      return;
    }

    setCode(
      currentQuestion.starter_code ||
      "",
    );

    setExecutionResult(
      null,
    );

    setSubmitResult(
      null,
    );

    setIsSubmitted(false);

    setError(null);
  }, [
    currentQuestion?.id,
  ]);

  async function handleRunCode() {
    if (!currentQuestion) {
      return;
    }

    if (!code.trim()) {
      setError(
        "Please write some code before running it.",
      );

      return;
    }

    try {
      setError(null);

      setIsRunning(true);

      setExecutionResult(
        null,
      );

      const result =
        await runCode(
          currentQuestion.id,
          code,
        );

      setExecutionResult(
        result,
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to execute the code.",
      );
    } finally {
      setIsRunning(false);
    }
  }

  async function handleSubmit() {
    if (!sessionId) {
      setError(
        "Interview session not found.",
      );

      return;
    }

    if (!currentQuestion) {
      return;
    }

    if (!code.trim()) {
      setError(
        "Please write some code before submitting.",
      );

      return;
    }

    if (!allTestsPassed) {
      setError(
        "Please run your code and pass all test cases before submitting.",
      );

      return;
    }

    if (isSubmitted) {
      return;
    }

    try {
      setError(null);

      setIsSubmitting(true);

      const result =
        await submitCodingAnswer(
          sessionId,
          code,
        );

      setSubmitResult({
        success:
          result.success,

        passed:
          result.passed_test_cases,

        total:
          result.total_test_cases,

        score:
          result.score,

        isLastQuestion:
          result.is_last_question,
      });

      setIsSubmitted(true);

      setInterview(
        (previous) =>
          previous
            ? {
                ...previous,

                current_question_number:
                  result.question_number,
              }
            : previous,
      );

      if (result.is_last_question) {
        setIsLoadingResult(true);

        const finalResult =
          await getCodingInterviewResult(
            sessionId,
          );

        navigate(
          `/coding-interview/results/${encodeURIComponent(String(sessionId))}`,
          {
            state: {
              result: finalResult,
              sessionId,
            },
          },
        );

        return;
      }
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to submit your solution.",
      );
    } finally {
      setIsSubmitting(false);

      setIsLoadingResult(false);
    }
  }

  async function handleNextQuestion() {
    if (!sessionId) {
      setError(
        "Interview session not found.",
      );

      return;
    }

    if (!isSubmitted) {
      setError(
        "Please submit your solution before moving to the next question.",
      );

      return;
    }

    if (
      submitResult?.isLastQuestion
    ) {
      return;
    }

    try {
      setError(null);

      setIsLoadingNext(true);

      const nextQuestion =
        await getNextCodingQuestion(
          sessionId,
        );

      setCurrentQuestionData(
        nextQuestion,
      );

      setCode(
        nextQuestion.question
          .starter_code || "",
      );

      setExecutionResult(
        null,
      );

      setSubmitResult(
        null,
      );

      setIsSubmitted(false);

      const updatedInterview =
        await getCodingInterview(
          sessionId,
        );

      setInterview(
        updatedInterview,
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load the next question.",
      );
    } finally {
      setIsLoadingNext(false);
    }
  }

  /**
   * Release the interview camera and screen share and leave fullscreen.
   * Called only when the candidate finishes or voluntarily exits the interview.
   */
  async function releaseInterviewMedia() {
    const camera = getInterviewCameraStream();
    const display = getInterviewDisplayStream();

    try {
      camera?.getTracks().forEach((track) => track.stop());
      display?.getTracks().forEach((track) => track.stop());
    } finally {
      stopInterviewSetupMedia();

      try {
        if (document.fullscreenElement) {
          await document.exitFullscreen();
        }
      } catch {
        // The browser may already have exited fullscreen.
      }
    }
  }

  async function handleSkipQuestion() {
    if (!sessionId || !currentQuestion) {
      setError("Interview session not found.");
      return;
    }

    if (isSubmitted || isSubmitting || isLoadingNext || isRunning) {
      return;
    }

    try {
      setError(null);
      setIsLoadingNext(true);
      const response = await skipCodingQuestion(sessionId);

      if (response.is_last_question || !response.next_question) {
        const finalResult = await getCodingInterviewResult(sessionId);
        await releaseInterviewMedia();
        navigate(
          `/coding-interview/results/${encodeURIComponent(String(sessionId))}`,
          { state: { result: finalResult, sessionId } },
        );
        return;
      }

      const nextQuestion = response.next_question;
      setCurrentQuestionData(nextQuestion);
      setCode(nextQuestion.question.starter_code || "");
      setExecutionResult(null);
      setSubmitResult(null);
      setIsSubmitted(false);
      const updatedInterview = await getCodingInterview(sessionId);
      setInterview(updatedInterview);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to skip this question.");
    } finally {
      setIsLoadingNext(false);
    }
  }

  useEffect(() => {
    function handleKeyboard(
      event: KeyboardEvent,
    ) {
      if (
        (event.ctrlKey ||
          event.metaKey) &&
        event.key === "Enter"
      ) {
        event.preventDefault();

        void handleRunCode();
      }
    }

    window.addEventListener(
      "keydown",
      handleKeyboard,
    );

    return () =>
      window.removeEventListener(
        "keydown",
        handleKeyboard,
      );
  }, [
    code,
    currentQuestion,
  ]);

  async function handleExit() {
    if (!sessionId) {
      await releaseInterviewMedia();
      navigate("/home");
      return;
    }

    try {
      await abandonCodingInterview(sessionId);
      let finalResult: CodingInterviewResult | null = null;

      try {
        finalResult = await getCodingInterviewResult(sessionId);
      } catch {
        // If the report cannot be loaded, still allow the candidate to leave.
      }

      await releaseInterviewMedia();

      if (finalResult) {
        navigate(
          `/coding-interview/results/${encodeURIComponent(String(sessionId))}`,
          { state: { result: finalResult, sessionId } },
        );
      } else {
        navigate("/home");
      }
      return;
    } catch {
      // Still release media and allow the candidate to leave if saving fails.
    }

    await releaseInterviewMedia();
    navigate("/home");
  }

  if (
    isLoading ||
    !interviewState
  ) {
    return (
      <div className="app-background min-h-screen flex items-center justify-center">
        <div className="text-center">

          <div className="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-2 border-white/10 border-t-violet-400" />

          <p className="text-sm text-slate-400">
            Preparing coding interview...
          </p>

        </div>
      </div>
    );
  }

  if (
    !sessionId ||
    !currentQuestion
  ) {
    return (
      <div className="app-background min-h-screen flex items-center justify-center px-6">

        <div className="max-w-md text-center">

          <p className="font-mono text-[9px] uppercase tracking-[0.2em] text-rose-400">
            Coding Interview
          </p>

          <h1 className="mt-3 text-xl font-semibold text-white">
            Unable to load interview
          </h1>

          <p className="mt-3 text-sm leading-6 text-slate-400">
            {error ||
              "The coding interview session could not be loaded."}
          </p>

          <button
            type="button"
            onClick={() =>
              navigate(
                "/coding-interview/setup",
              )
            }
            className="mt-6 rounded-lg bg-violet-500 px-5 py-2.5 text-xs font-semibold text-white hover:bg-violet-400"
          >
            Start New Interview
          </button>

        </div>

      </div>
    );
  }

  const questionNumber =
    currentQuestionData
      ?.question_number ??
    interview?.current_question_number ??
    1;

  const totalQuestions =
    currentQuestionData
      ?.total_questions ??
    interview?.total_questions ??
    interviewState.questionCount ??
    0;

  return (
    <div className="app-background min-h-screen text-white">

      <div className="app-grid" />

      <header className="relative z-20 border-b border-white/[0.06] bg-black/20 backdrop-blur-xl">

        <div className="mx-auto flex max-w-[1600px] items-center justify-between px-5 py-4">

          <div className="flex items-center gap-4">

            <button
              type="button"
              onClick={() =>
                setShowExitConfirmation(
                  true,
                )
              }
              className="rounded-lg border border-white/10 px-3 py-2 text-xs text-slate-400 hover:text-white"
            >
              ← Exit
            </button>

            <div>

              <p className="font-mono text-[9px] uppercase tracking-[0.2em] text-slate-600">
                Coding Interview
              </p>

              <p className="mt-1 text-sm font-medium text-slate-200">

                Question{" "}
                {questionNumber}

                {" "}of{" "}

                {totalQuestions}

              </p>

            </div>

          </div>

          <div className="flex items-center gap-3">

            <span className="rounded-full border border-cyan-400/20 bg-cyan-400/[0.06] px-3 py-1 text-xs text-cyan-300">

              {
                LANGUAGE_LABELS[
                  interviewState.language
                ]
              }

            </span>

            <span className="rounded-full border border-violet-400/20 bg-violet-400/[0.06] px-3 py-1 text-xs text-violet-300">

              {
                DIFFICULTY_LABELS[
                  interviewState.difficulty
                ]
              }

            </span>

          </div>

        </div>

      </header>

      {error && (

        <div className="relative z-20 border-b border-rose-400/20 bg-rose-400/[0.05] px-5 py-3">

          <div className="mx-auto max-w-[1600px] text-sm text-rose-300">
            {error}
          </div>

        </div>

      )}

      <main className="relative z-10 mx-auto max-w-[1600px] px-4 py-5 lg:px-6">

        <div className="grid min-h-[calc(100vh-130px)] gap-5 lg:grid-cols-2">

          <section className="glass-panel flex min-h-[650px] flex-col overflow-hidden rounded-2xl">

            <div className="border-b border-white/[0.06] px-6 py-5">

              <p className="font-mono text-[9px] uppercase tracking-[0.2em] text-slate-600">
                Problem
              </p>

              <h1 className="mt-2 text-2xl font-semibold text-white">
                {currentQuestion.title}
              </h1>

            </div>

            <div className="flex-1 overflow-y-auto px-6 py-6">

              <h2 className="mb-3 text-sm font-semibold text-white">
                Problem Statement
              </h2>

              <div className="whitespace-pre-wrap text-sm leading-7 text-slate-300">
                {
                  currentQuestion.problem_statement
                }
              </div>

              <div className="mt-8">

                <h2 className="mb-3 text-sm font-semibold text-white">
                  💡 Hints
                </h2>

                <div className="space-y-3">

                  <div className="rounded-xl border border-amber-400/10 bg-amber-400/[0.04] p-4">

                    <p className="mb-2 font-mono text-[9px] uppercase tracking-[0.15em] text-amber-400/70">
                      Hint 1
                    </p>

                    <p className="text-sm leading-6 text-slate-300">
                      {currentQuestion.hint_1}
                    </p>

                  </div>

                  <div className="rounded-xl border border-amber-400/10 bg-amber-400/[0.04] p-4">

                    <p className="mb-2 font-mono text-[9px] uppercase tracking-[0.15em] text-amber-400/70">
                      Hint 2
                    </p>

                    <p className="text-sm leading-6 text-slate-300">
                      {currentQuestion.hint_2}
                    </p>

                  </div>

                </div>

              </div>

              <div className="mt-8">

                <h2 className="mb-3 text-sm font-semibold text-white">
                  Input Format
                </h2>

                <div className="whitespace-pre-wrap rounded-xl border border-white/[0.06] bg-black/20 p-4 font-mono text-xs leading-6 text-slate-400">
                  {
                    currentQuestion.input_format
                  }
                </div>

              </div>

              <div className="mt-6">

                <h2 className="mb-3 text-sm font-semibold text-white">
                  Output Format
                </h2>

                <div className="whitespace-pre-wrap rounded-xl border border-white/[0.06] bg-black/20 p-4 font-mono text-xs leading-6 text-slate-400">
                  {
                    currentQuestion.output_format
                  }
                </div>

              </div>

              <div className="mt-6">

                <h2 className="mb-3 text-sm font-semibold text-white">
                  Constraints
                </h2>

                <div className="whitespace-pre-wrap rounded-xl border border-white/[0.06] bg-black/20 p-4 font-mono text-xs leading-6 text-slate-400">
                  {
                    currentQuestion.constraints
                  }
                </div>

              </div>

              <div className="mt-6">

                <h2 className="mb-3 text-sm font-semibold text-white">
                  Examples
                </h2>

                {examples.length === 0 ? (

                  <p className="text-sm text-slate-500">
                    No examples available.
                  </p>

                ) : (

                  <div className="space-y-4">

                    {examples.map(
                      (
                        example,
                        index,
                      ) => (

                        <div
                          key={index}
                          className="rounded-xl border border-white/[0.06] bg-black/20 p-4"
                        >

                          <p className="mb-3 font-mono text-[9px] uppercase tracking-[0.15em] text-slate-600">
                            Example{" "}
                            {index + 1}
                          </p>

                          <div className="grid gap-4 md:grid-cols-2">

                            <div>

                              <p className="mb-2 text-xs text-slate-600">
                                Input
                              </p>

                              <pre className="whitespace-pre-wrap font-mono text-xs text-slate-400">
                                {example.input}
                              </pre>

                            </div>

                            <div>

                              <p className="mb-2 text-xs text-slate-600">
                                Output
                              </p>

                              <pre className="whitespace-pre-wrap font-mono text-xs text-slate-400">
                                {example.output}
                              </pre>

                            </div>

                          </div>

                        </div>

                      ),
                    )}

                  </div>

                )}

              </div>

            </div>

          </section>

          <section className="flex min-h-[650px] flex-col overflow-hidden rounded-2xl border border-white/[0.07] bg-[#0a0a0f]">

            <div className="flex items-center justify-between border-b border-white/[0.06] bg-white/[0.02] px-4 py-3">

              <div className="flex items-center gap-3">

                <div className="flex gap-1.5">

                  <span className="h-2.5 w-2.5 rounded-full bg-red-400/60" />

                  <span className="h-2.5 w-2.5 rounded-full bg-yellow-400/60" />

                  <span className="h-2.5 w-2.5 rounded-full bg-green-400/60" />

                </div>

                <span className="font-mono text-xs text-slate-500">

                  {
                    interviewState.language ===
                    "python"
                      ? "solution.py"
                      : interviewState.language ===
                        "javascript"
                        ? "solution.js"
                        : interviewState.language ===
                          "java"
                          ? "Solution.java"
                          : "solution.cpp"
                  }

                </span>

              </div>

              <span className="text-xs text-slate-600">
                Ctrl + Enter to run
              </span>

            </div>

            <div className="relative min-h-[350px] flex-1">

              <Editor
                height="100%"
                language={
                  interviewState.language === "javascript"
                    ? "javascript"
                    : interviewState.language === "python"
                      ? "python"
                      : interviewState.language === "java"
                        ? "java"
                        : "cpp"
                }
                theme="vs-dark"
                value={code}
                onChange={(value) => {
                  setCode(value ?? "");

                  setExecutionResult(null);
                  setSubmitResult(null);
                  setIsSubmitted(false);
                }}
                options={{
                  readOnly: isSubmitted,
                  automaticLayout: true,
                  minimap: { enabled: false },
                  fontSize: 14,
                  lineHeight: 24,
                  fontFamily: "Consolas, 'Courier New', monospace",
                  tabSize: interviewState.language === "python" ? 4 : 2,
                  insertSpaces: true,
                  detectIndentation: false,
                  autoIndent: "full",
                  formatOnPaste: true,
                  formatOnType: true,
                  wordWrap: "on",
                  scrollBeyondLastLine: false,
                  padding: {
                    top: 18,
                    bottom: 18,
                  },
                  suggestOnTriggerCharacters: true,
                  quickSuggestions: true,
                  scrollbar: {
                    verticalScrollbarSize: 10,
                    horizontalScrollbarSize: 10,
                  },
                }}
                loading={
                  <div className="p-5 font-mono text-sm text-slate-500">
                    Loading code editor...
                  </div>
                }
              />

            </div>

            <div className="border-t border-white/[0.06]">

              <div className="border-b border-white/[0.05] px-4 py-3">

                <div className="flex items-center justify-between">

                  <div>

                    <p className="font-mono text-[9px] uppercase tracking-[0.18em] text-slate-600">
                      Test Results
                    </p>

                    {executionResult && (

                      <p className="mt-1 text-xs text-slate-400">

                        {
                          executionResult.passed_test_cases
                        }

                        /

                        {
                          executionResult.total_test_cases
                        }

                        {" "}
                        test cases passed

                      </p>

                    )}

                  </div>

                  {executionResult && (

                    <span
                      className={`rounded-full px-3 py-1 text-[10px] font-semibold ${
                        executionResult.success
                          ? "bg-emerald-400/10 text-emerald-300"
                          : "bg-rose-400/10 text-rose-300"
                      }`}
                    >
                      {
                        executionResult.success
                          ? "All Tests Passed"
                          : "Some Tests Failed"
                      }
                    </span>

                  )}

                </div>

              </div>

              <div className="max-h-64 overflow-y-auto px-4 py-4">

                {!executionResult ? (

                  <div className="rounded-lg border border-white/[0.05] bg-white/[0.015] px-4 py-4 text-xs text-slate-600">
                    Run your code to validate all test cases. Submission
                    will be enabled only when every test case passes.
                  </div>

                ) : (

                  <div className="space-y-3">

                    {executionResult.results.map(
                      (result) => (

                        <div
                          key={
                            result.test_case_number
                          }
                          className={`rounded-xl border p-4 ${
                            result.passed
                              ? "border-emerald-400/20 bg-emerald-400/[0.04]"
                              : "border-rose-400/20 bg-rose-400/[0.04]"
                          }`}
                        >

                          <div className="flex items-center justify-between">

                            <span className="text-xs font-medium text-slate-300">
                              Test Case{" "}
                              {
                                result.test_case_number
                              }
                            </span>

                            <span
                              className={`text-[10px] font-semibold uppercase tracking-[0.1em] ${
                                result.passed
                                  ? "text-emerald-300"
                                  : "text-rose-300"
                              }`}
                            >
                              {
                                result.passed
                                  ? "Passed"
                                  : "Failed"
                              }
                            </span>

                          </div>

                          <div className="mt-3 grid gap-4 md:grid-cols-3">

                            <div>

                              <p className="mb-1 text-[10px] uppercase tracking-wider text-slate-600">
                                Input
                              </p>

                              <pre className="whitespace-pre-wrap font-mono text-xs text-slate-400">
                                {
                                  result.input_data
                                }
                              </pre>

                            </div>

                            <div>

                              <p className="mb-1 text-[10px] uppercase tracking-wider text-slate-600">
                                Expected
                              </p>

                              <pre className="whitespace-pre-wrap font-mono text-xs text-slate-400">
                                {
                                  result.expected_output
                                }
                              </pre>

                            </div>

                            <div>

                              <p className="mb-1 text-[10px] uppercase tracking-wider text-slate-600">
                                Actual
                              </p>

                              <pre className="whitespace-pre-wrap font-mono text-xs text-slate-400">
                                {
                                  result.actual_output ||
                                  "—"
                                }
                              </pre>

                            </div>

                          </div>

                          {result.error && (

                            <div className="mt-3 rounded-lg bg-rose-400/[0.05] p-3">

                              <p className="mb-1 text-[10px] uppercase tracking-wider text-rose-400">
                                Error
                              </p>

                              <pre className="whitespace-pre-wrap font-mono text-xs leading-5 text-rose-300">
                                {
                                  result.error
                                }
                              </pre>

                            </div>

                          )}

                          {result.execution_time_ms !==
                            null && (

                            <p className="mt-3 font-mono text-[10px] text-slate-600">

                              Execution time:{" "}
                              {
                                result.execution_time_ms.toFixed(
                                  2,
                                )
                              }
                              ms

                            </p>

                          )}

                        </div>

                      ),
                    )}

                  </div>

                )}

              </div>

            </div>

            {submitResult && (

              <div className="border-t border-white/[0.06] px-4 py-4">

                <div
                  className={`rounded-xl border p-4 ${
                    submitResult.success
                      ? "border-emerald-400/20 bg-emerald-400/[0.04]"
                      : "border-rose-400/20 bg-rose-400/[0.04]"
                  }`}
                >

                  <div className="flex items-center justify-between">

                    <div>

                      <p className="text-sm font-semibold text-white">
                        {
                          submitResult.success
                            ? "Solution Accepted"
                            : "Solution Submitted"
                        }
                      </p>

                      <p className="mt-1 text-xs text-slate-400">
                        {
                          submitResult.passed
                        }
                        /
                        {
                          submitResult.total
                        }
                        {" "}
                        test cases passed
                      </p>

                    </div>

                    {submitResult.score !==
                      undefined && (

                      <span className="text-lg font-semibold text-violet-300">
                        {
                          submitResult.score
                        }%
                      </span>

                    )}

                  </div>

                </div>

              </div>

            )}

            <div className="flex items-center justify-between border-t border-white/[0.06] bg-white/[0.015] px-4 py-4">

              <div>

                {isSubmitted && (
                  <span className="text-[10px] uppercase tracking-wider text-emerald-300">
                    ✓ Submitted
                  </span>
                )}

              </div>

              <div className="flex gap-3">

                {!isSubmitted && (
                  <button
                    type="button"
                    onClick={handleSkipQuestion}
                    disabled={isRunning || isSubmitting || isLoadingNext}
                    className="rounded-lg border border-white/10 bg-white/[0.03] px-4 py-2.5 text-xs font-semibold text-slate-300 transition hover:bg-white/[0.06] hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {isLoadingNext ? "Moving..." : "Skip Question →"}
                  </button>
                )}

                <button
                  type="button"
                  onClick={
                    handleRunCode
                  }
                  disabled={
                    isRunning ||
                    isSubmitting ||
                    isSubmitted
                  }
                  className="rounded-lg border border-white/10 bg-white/[0.03] px-5 py-2.5 text-xs font-semibold text-slate-300 hover:bg-white/[0.06] hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {isRunning
                    ? "Running..."
                    : "▶ Run Code"}
                </button>

                {!isSubmitted && (

                  <button
                    type="button"
                    onClick={
                      handleSubmit
                    }
                    disabled={
                      isRunning ||
                      isSubmitting ||
                      !allTestsPassed
                    }
                    className={`rounded-lg px-5 py-2.5 text-xs font-semibold text-white shadow-lg disabled:cursor-not-allowed disabled:opacity-50 ${
                      allTestsPassed
                        ? "bg-emerald-500 shadow-emerald-500/20 hover:bg-emerald-400"
                        : "bg-slate-700/60 shadow-none"
                    }`}
                  >
                    {isSubmitting
                      ? "Submitting..."
                      : allTestsPassed
                        ? "✓ Submit Solution"
                        : "✓ Pass All Tests to Submit"}
                  </button>

                )}

                {isSubmitted &&
                  !submitResult?.isLastQuestion && (

                  <button
                    type="button"
                    onClick={
                      handleNextQuestion
                    }
                    disabled={
                      isLoadingNext
                    }
                    className="rounded-lg bg-violet-500 px-5 py-2.5 text-xs font-semibold text-white shadow-lg shadow-violet-500/20 hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {isLoadingNext
                      ? "Loading..."
                      : "Next Question →"}
                  </button>

                )}

                {isSubmitted &&
                  submitResult?.isLastQuestion && (

                  <button
                    type="button"
                    onClick={async () => {
                      if (!sessionId) {
                        return;
                      }

                      try {
                        setIsLoadingResult(
                          true,
                        );

                        const result =
                          await getCodingInterviewResult(
                            sessionId,
                          );

                        await releaseInterviewMedia();

                        navigate(
                          `/coding-interview/results/${encodeURIComponent(String(sessionId))}`,
                          {
                            state: {
                              result,
                              sessionId,
                            },
                          },
                        );
                      } catch (err) {
                        setError(
                          err instanceof Error
                            ? err.message
                            : "Unable to load the final result.",
                        );
                      } finally {
                        setIsLoadingResult(
                          false,
                        );
                      }
                    }}
                    disabled={
                      isLoadingResult
                    }
                    className="rounded-lg bg-violet-500 px-5 py-2.5 text-xs font-semibold text-white shadow-lg shadow-violet-500/20 hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {isLoadingResult
                      ? "Loading Result..."
                      : "View Final Result →"}
                  </button>

                )}

              </div>

            </div>

          </section>

        </div>

      </main>

      {showExitConfirmation && (

        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-6 backdrop-blur-sm">

          <div className="w-full max-w-md rounded-2xl border border-white/10 bg-[#111116] p-7 shadow-2xl">

            <p className="font-mono text-[9px] uppercase tracking-[0.2em] text-rose-400">
              Leave Interview
            </p>

            <h2 className="mt-3 text-xl font-semibold text-white">
              End coding interview?
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-400">
              Your current code will not be submitted.
              Ending now will save your progress and open your coding interview result.
            </p>

            <div className="mt-7 flex justify-end gap-3">

              <button
                type="button"
                onClick={() =>
                  setShowExitConfirmation(
                    false,
                  )
                }
                className="rounded-lg border border-white/10 px-4 py-2.5 text-xs text-slate-400 hover:text-white"
              >
                Continue
              </button>

              <button
                type="button"
                onClick={
                  handleExit
                }
                className="rounded-lg bg-rose-500 px-4 py-2.5 text-xs font-semibold text-white hover:bg-rose-400"
              >
                End Interview
              </button>

            </div>

          </div>

        </div>

      )}

    </div>
  );
}