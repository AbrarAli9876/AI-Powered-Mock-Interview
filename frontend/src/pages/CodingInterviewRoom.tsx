import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  useLocation,
  useNavigate,
} from "react-router-dom";

import {
  CodingLanguage,
  CodingQuestion,
  Difficulty,
  getCodingQuestions,
} from "../lib/api";


interface LocationState {
  topicId?: number;
  language?: CodingLanguage;
  difficulty?: Difficulty;
  questionCount?: number;
  questions?: CodingQuestion[];
}


interface TestCaseResult {
  test_case_number: number;
  passed: boolean;
  input_data: string;
  expected_output: string;
  actual_output: string;
  error: string | null;
  execution_time_ms: number | null;
}


interface CodeExecutionResponse {
  success: boolean;
  language: string;
  total_test_cases: number;
  passed_test_cases: number;
  failed_test_cases: number;
  results: TestCaseResult[];
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


function CodingInterviewRoom() {
  const navigate = useNavigate();

  const location =
    useLocation();

  const locationState =
    (location.state as LocationState | null) ??
    null;


  const [questions, setQuestions] =
    useState<CodingQuestion[]>(
      locationState?.questions ?? [],
    );

  const [currentIndex, setCurrentIndex] =
    useState(0);

  const [code, setCode] =
    useState("");

  const [loading, setLoading] =
    useState(
      locationState?.questions
        ? false
        : true,
    );

  const [running, setRunning] =
    useState(false);

  const [submitting, setSubmitting] =
    useState(false);

  const [executionResult, setExecutionResult] =
    useState<CodeExecutionResponse | null>(
      null,
    );

  const [error, setError] =
    useState<string | null>(null);

  const [showProblem, setShowProblem] =
    useState(true);


  const currentQuestion =
    questions[currentIndex];


  const language =
    currentQuestion?.language ??
    locationState?.language ??
    "python";


  const questionNumber =
    currentIndex + 1;


  const totalQuestions =
    questions.length;


  const progressPercentage =
    totalQuestions > 0
      ? (questionNumber / totalQuestions) * 100
      : 0;


  const isLastQuestion =
    currentIndex ===
    totalQuestions - 1;


  const canSubmit =
    executionResult !== null &&
    executionResult.success;


  const languageLabel =
    LANGUAGE_LABELS[language];


  const formattedExamples =
    useMemo(() => {
      if (!currentQuestion?.examples) {
        return [];
      }

      return currentQuestion.examples
        .split(/\n\s*\n/)
        .filter(
          (example) =>
            example.trim().length > 0,
        );
    }, [currentQuestion]);


  useEffect(() => {
    async function loadQuestions() {
      if (locationState?.questions?.length) {
        return;
      }

      if (
        locationState?.topicId === undefined ||
        !locationState.language ||
        !locationState.difficulty
      ) {
        setError(
          "Coding interview configuration is missing.",
        );

        setLoading(false);

        return;
      }


      try {
        setLoading(true);
        setError(null);

        const data =
          await getCodingQuestions(
            locationState.topicId,
            locationState.language,
            locationState.difficulty,
          );


        if (data.length === 0) {
          setError(
            "No coding questions are available for this interview.",
          );

          return;
        }


        const requestedCount =
          locationState.questionCount ??
          data.length;


        setQuestions(
          data.slice(
            0,
            requestedCount,
          ),
        );
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load coding questions.",
        );
      } finally {
        setLoading(false);
      }
    }


    loadQuestions();
  }, [
    locationState,
  ]);


  useEffect(() => {
    if (currentQuestion) {
      setCode(
        currentQuestion.starter_code,
      );

      setExecutionResult(null);
      setError(null);
    }
  }, [
    currentQuestion,
  ]);


  async function executeCode() {
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
      setRunning(true);
      setError(null);
      setExecutionResult(null);


      const token =
        localStorage.getItem(
          "access_token",
        );


      const API_BASE_URL =
        import.meta.env.VITE_API_BASE_URL ||
        "http://127.0.0.1:8000";


      const response =
        await fetch(
          `${API_BASE_URL}/code-execution/run`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",

              ...(token
                ? {
                    Authorization:
                      `Bearer ${token}`,
                  }
                : {}),
            },

            body: JSON.stringify({
              coding_question_id:
                currentQuestion.id,

              code,
            }),
          },
        );


      if (!response.ok) {
        let message =
          "Code execution failed.";


        try {
          const data =
            await response.json();

          message =
            data.detail ||
            message;
        } catch {
          // Keep default message.
        }


        throw new Error(message);
      }


      const result =
        (await response.json()) as CodeExecutionResponse;


      setExecutionResult(result);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to execute code.",
      );
    } finally {
      setRunning(false);
    }
  }


  async function submitSolution() {
    if (!currentQuestion) {
      return;
    }


    if (!executionResult?.success) {
      setError(
        "Your solution must pass all test cases before submission.",
      );

      return;
    }


    try {
      setSubmitting(true);
      setError(null);


      /*
       * For now, successful submission moves
       * to the next coding problem.
       *
       * Coding-answer persistence and AI
       * evaluation will be connected in the
       * next development step.
       */


      if (isLastQuestion) {
        navigate(
          "/dashboard",
          {
            replace: true,
          },
        );

        return;
      }


      setCurrentIndex(
        (previous) =>
          previous + 1,
      );
    } finally {
      setSubmitting(false);
    }
  }


  function handleBack() {
    const confirmed =
      window.confirm(
        "Are you sure you want to leave this coding interview? Your current progress may be lost.",
      );


    if (confirmed) {
      navigate("/home");
    }
  }


  if (loading) {
    return (
      <div className="app-background flex min-h-screen items-center justify-center">
        <div className="app-grid" />

        <div className="glass-panel relative z-10 rounded-2xl px-8 py-10 text-center">
          <div className="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-2 border-violet-400 border-t-transparent" />

          <p className="text-sm text-slate-400">
            Preparing your coding interview...
          </p>
        </div>
      </div>
    );
  }


  if (error && !currentQuestion) {
    return (
      <div className="app-background flex min-h-screen items-center justify-center px-6">
        <div className="app-grid" />

        <div className="glass-panel relative z-10 w-full max-w-lg rounded-2xl p-8 text-center">

          <div className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-full bg-rose-500/10 text-rose-400">
            !
          </div>

          <h1 className="text-2xl font-semibold text-white">
            Unable to start interview
          </h1>

          <p className="mt-3 text-sm leading-6 text-slate-400">
            {error}
          </p>

          <button
            type="button"
            onClick={() =>
              navigate("/coding-interview/new")
            }
            className="mt-7 rounded-xl bg-violet-500 px-6 py-3 text-sm font-semibold text-white hover:bg-violet-400"
          >
            Back to setup
          </button>

        </div>
      </div>
    );
  }


  if (!currentQuestion) {
    return null;
  }


  return (
    <div className="app-background min-h-screen">
      <div className="app-grid" />

      <main className="relative z-10 flex min-h-screen flex-col">

        {/* =================================================
            TOP BAR
        ================================================== */}

        <header className="border-b border-white/10 bg-black/20 backdrop-blur-xl">

          <div className="mx-auto flex max-w-[1600px] items-center justify-between gap-6 px-5 py-4">

            <div className="flex items-center gap-5">

              <button
                type="button"
                onClick={handleBack}
                className="text-sm text-slate-400 hover:text-white"
              >
                ← Exit
              </button>

              <div className="hidden h-6 w-px bg-white/10 sm:block" />

              <div>
                <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-slate-500">
                  Coding Interview
                </p>

                <p className="mt-1 text-sm font-medium text-white">
                  {languageLabel}
                  {" · "}
                  {currentQuestion.difficulty}
                </p>
              </div>

            </div>


            <div className="flex items-center gap-4">

              <div className="hidden text-right sm:block">
                <p className="text-xs text-slate-500">
                  Question
                </p>

                <p className="text-sm font-semibold text-white">
                  {questionNumber}
                  {" / "}
                  {totalQuestions}
                </p>
              </div>

              <div className="h-2 w-24 overflow-hidden rounded-full bg-white/10 sm:w-32">
                <div
                  className="h-full rounded-full bg-violet-400 transition-all duration-300"
                  style={{
                    width:
                      `${progressPercentage}%`,
                  }}
                />
              </div>

            </div>

          </div>

        </header>


        {/* =================================================
            MOBILE PROBLEM TOGGLE
        ================================================== */}

        <div className="border-b border-white/10 bg-black/10 px-5 py-3 lg:hidden">

          <button
            type="button"
            onClick={() =>
              setShowProblem(
                (previous) =>
                  !previous,
              )
            }
            className="text-sm font-medium text-violet-300"
          >
            {showProblem
              ? "Hide problem"
              : "Show problem"}
          </button>

        </div>


        {/* =================================================
            MAIN INTERVIEW AREA
        ================================================== */}

        <div className="mx-auto flex w-full max-w-[1600px] flex-1 flex-col gap-0 lg:grid lg:grid-cols-[minmax(320px,0.85fr)_minmax(500px,1.4fr)]">

          {/* =================================================
              PROBLEM PANEL
          ================================================== */}

          <section
            className={`border-b border-white/10 lg:border-b-0 lg:border-r ${
              showProblem
                ? "block"
                : "hidden lg:block"
            }`}
          >

            <div className="h-full overflow-y-auto p-6 md:p-8 lg:max-h-[calc(100vh-81px)]">

              <div className="mb-8">

                <div className="mb-4 flex flex-wrap items-center gap-2">

                  <span className="rounded-full border border-violet-400/20 bg-violet-400/10 px-3 py-1 font-mono text-[10px] uppercase tracking-wider text-violet-300">
                    {currentQuestion.difficulty}
                  </span>

                  <span className="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 font-mono text-[10px] uppercase tracking-wider text-cyan-300">
                    {languageLabel}
                  </span>

                </div>


                <h1 className="text-3xl font-semibold tracking-tight text-white">
                  {currentQuestion.title}
                </h1>

              </div>


              <div className="space-y-8">

                {/* Problem */}
                <div>
                  <h2 className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                    Problem
                  </h2>

                  <p className="whitespace-pre-wrap text-sm leading-7 text-slate-300">
                    {currentQuestion.problem_statement}
                  </p>
                </div>


                {/* Input */}
                <div>
                  <h2 className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                    Input
                  </h2>

                  <div className="rounded-xl border border-white/10 bg-black/20 p-4">
                    <p className="whitespace-pre-wrap text-sm leading-6 text-slate-400">
                      {currentQuestion.input_format}
                    </p>
                  </div>
                </div>


                {/* Output */}
                <div>
                  <h2 className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                    Output
                  </h2>

                  <div className="rounded-xl border border-white/10 bg-black/20 p-4">
                    <p className="whitespace-pre-wrap text-sm leading-6 text-slate-400">
                      {currentQuestion.output_format}
                    </p>
                  </div>
                </div>


                {/* Constraints */}
                <div>
                  <h2 className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                    Constraints
                  </h2>

                  <div className="rounded-xl border border-white/10 bg-black/20 p-4">
                    <p className="whitespace-pre-wrap font-mono text-xs leading-6 text-slate-400">
                      {currentQuestion.constraints}
                    </p>
                  </div>
                </div>


                {/* Examples */}
                <div>
                  <h2 className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                    Examples
                  </h2>

                  <div className="space-y-3">

                    {formattedExamples.length > 0 ? (
                      formattedExamples.map(
                        (
                          example,
                          index,
                        ) => (
                          <pre
                            key={index}
                            className="overflow-x-auto rounded-xl border border-white/10 bg-black/30 p-4 font-mono text-xs leading-6 text-slate-300"
                          >
                            {example}
                          </pre>
                        ),
                      )
                    ) : (
                      <pre className="overflow-x-auto rounded-xl border border-white/10 bg-black/30 p-4 font-mono text-xs leading-6 text-slate-300">
                        {currentQuestion.examples}
                      </pre>
                    )}

                  </div>
                </div>

              </div>

            </div>

          </section>


          {/* =================================================
              CODE PANEL
          ================================================== */}

          <section className="flex min-h-[650px] flex-1 flex-col">

            {/* Editor Header */}
            <div className="flex items-center justify-between border-b border-white/10 bg-black/20 px-5 py-3">

              <div className="flex items-center gap-3">

                <div className="flex gap-1.5">
                  <div className="h-2.5 w-2.5 rounded-full bg-rose-400/70" />
                  <div className="h-2.5 w-2.5 rounded-full bg-amber-400/70" />
                  <div className="h-2.5 w-2.5 rounded-full bg-emerald-400/70" />
                </div>

                <span className="font-mono text-xs text-slate-500">
                  solution
                </span>

              </div>


              <span className="rounded-md border border-white/10 bg-white/[0.03] px-3 py-1 font-mono text-xs text-slate-400">
                {languageLabel}
              </span>

            </div>


            {/* Editor */}
            <div className="relative flex-1 bg-[#080b12]">

              <textarea
                value={code}
                onChange={(event) => {
                  setCode(
                    event.target.value,
                  );

                  setExecutionResult(
                    null,
                  );

                  setError(null);
                }}
                spellCheck={false}
                className="h-full min-h-[420px] w-full resize-none border-0 bg-transparent p-6 font-mono text-sm leading-7 text-slate-200 outline-none"
                placeholder="Write your solution here..."
              />

            </div>


            {/* Error */}
            {error && (
              <div className="border-t border-rose-500/20 bg-rose-500/5 px-5 py-3">
                <p className="text-sm text-rose-300">
                  {error}
                </p>
              </div>
            )}


            {/* =================================================
                TEST RESULTS
            ================================================== */}

            <div className="max-h-[280px] overflow-y-auto border-t border-white/10 bg-black/20">

              <div className="px-5 py-4">

                <div className="mb-4 flex items-center justify-between">

                  <h2 className="text-sm font-semibold text-white">
                    Test Results
                  </h2>

                  {executionResult && (
                    <span
                      className={`text-xs font-medium ${
                        executionResult.success
                          ? "text-emerald-400"
                          : "text-amber-400"
                      }`}
                    >
                      {
                        executionResult.passed_test_cases
                      }
                      {" / "}
                      {
                        executionResult.total_test_cases
                      }
                      {" passed"}
                    </span>
                  )}

                </div>


                {!executionResult ? (
                  <div className="rounded-xl border border-dashed border-white/10 px-5 py-7 text-center">
                    <p className="text-sm text-slate-500">
                      Run your code to see the
                      test results.
                    </p>
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
                              ? "border-emerald-400/20 bg-emerald-400/5"
                              : "border-rose-400/20 bg-rose-400/5"
                          }`}
                        >

                          <div className="flex items-center justify-between">

                            <div className="flex items-center gap-3">

                              <span
                                className={`flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold ${
                                  result.passed
                                    ? "bg-emerald-400/10 text-emerald-400"
                                    : "bg-rose-400/10 text-rose-400"
                                }`}
                              >
                                {result.passed
                                  ? "✓"
                                  : "×"}
                              </span>

                              <span className="text-sm font-medium text-white">
                                Test Case{" "}
                                {
                                  result.test_case_number
                                }
                              </span>

                            </div>


                            {result.execution_time_ms !==
                              null && (
                              <span className="font-mono text-[10px] text-slate-500">
                                {
                                  result.execution_time_ms.toFixed(
                                    0,
                                  )
                                }
                                {" ms"}
                              </span>
                            )}

                          </div>


                          {!result.passed && (
                            <div className="mt-4 space-y-3">

                              <div>
                                <p className="mb-1 text-[10px] uppercase tracking-wider text-slate-500">
                                  Expected
                                </p>

                                <pre className="overflow-x-auto rounded-lg bg-black/20 p-3 font-mono text-xs text-slate-300">
                                  {result.expected_output}
                                </pre>
                              </div>


                              <div>
                                <p className="mb-1 text-[10px] uppercase tracking-wider text-slate-500">
                                  Actual
                                </p>

                                <pre className="overflow-x-auto rounded-lg bg-black/20 p-3 font-mono text-xs text-slate-300">
                                  {result.actual_output ||
                                    "No output"}
                                </pre>
                              </div>


                              {result.error && (
                                <div>
                                  <p className="mb-1 text-[10px] uppercase tracking-wider text-rose-400">
                                    Error
                                  </p>

                                  <pre className="overflow-x-auto rounded-lg bg-black/20 p-3 font-mono text-xs text-rose-300">
                                    {result.error}
                                  </pre>
                                </div>
                              )}

                            </div>
                          )}

                        </div>
                      ),
                    )}

                  </div>
                )}

              </div>

            </div>


            {/* =================================================
                ACTION BAR
            ================================================== */}

            <div className="flex flex-col gap-3 border-t border-white/10 bg-black/30 p-4 sm:flex-row sm:items-center sm:justify-between">

              <div className="text-xs text-slate-500">

                {executionResult?.success
                  ? "All test cases passed."
                  : "Run your code before submitting."}

              </div>


              <div className="flex gap-3">

                <button
                  type="button"
                  onClick={executeCode}
                  disabled={running}
                  className="rounded-xl border border-white/10 bg-white/[0.04] px-5 py-3 text-sm font-semibold text-white hover:bg-white/[0.08] disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {running
                    ? "Running..."
                    : "▶ Run Code"}
                </button>


                <button
                  type="button"
                  onClick={submitSolution}
                  disabled={
                    submitting ||
                    !canSubmit
                  }
                  className="rounded-xl bg-violet-500 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  {submitting
                    ? "Submitting..."
                    : isLastQuestion
                      ? "Submit & Finish"
                      : "Submit & Next →"}
                </button>

              </div>

            </div>

          </section>

        </div>

      </main>
    </div>
  );
}


export default CodingInterviewRoom;