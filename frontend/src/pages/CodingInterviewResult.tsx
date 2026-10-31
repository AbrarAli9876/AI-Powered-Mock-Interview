import { useEffect, useMemo, useState } from "react";
import {
  useLocation,
  useNavigate,
  useParams,
  useSearchParams,
} from "react-router-dom";
import { invalidateCodingInterviewCache } from "../lib/dataCache";
import {
  getCodingInterviewResult,
  type CodingInterviewResult,
  type CodingInterviewResultAnswer,
} from "../lib/api";

type ResultLocationState = {
  result?: CodingInterviewResult;
  sessionId?: number;
};

const LANGUAGE_NAMES: Record<string, string> = {
  python: "Python",
  javascript: "JavaScript",
  java: "Java",
  cpp: "C++",
  sql: "SQL",
};

function displayLanguage(language?: string) {
  if (!language) return "—";
  return LANGUAGE_NAMES[language.toLowerCase()] ?? language.toUpperCase();
}

function formatPercent(value: number | null | undefined) {
  const safeValue = Number.isFinite(value) ? Number(value) : 0;
  return `${Math.round(safeValue)}%`;
}

function StatCard({
  label,
  value,
  detail,
}: {
  label: string;
  value: string | number;
  detail?: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5">
      <p className="text-sm text-slate-400">{label}</p>
      <p className="mt-2 text-3xl font-semibold text-white">{value}</p>
      {detail && <p className="mt-1 text-xs text-slate-500">{detail}</p>}
    </div>
  );
}

function QuestionReview({
  answer,
  expanded,
  onToggle,
}: {
  answer: CodingInterviewResultAnswer;
  expanded: boolean;
  onToggle: () => void;
}) {
  const passed = Number(answer.passed_test_cases ?? 0);
  const total = Number(answer.total_test_cases ?? 0);
  const score = Number(answer.score ?? 0);

  return (
    <article className="overflow-hidden rounded-2xl border border-white/10 bg-slate-950/50">
      <button
        type="button"
        onClick={onToggle}
        className="flex w-full flex-col gap-4 p-5 text-left transition hover:bg-white/[0.03] sm:flex-row sm:items-center sm:justify-between"
        aria-expanded={expanded}
      >
        <div className="flex min-w-0 items-start gap-4">
          <div
            className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-sm font-bold ${
              answer.success
                ? "bg-emerald-400/15 text-emerald-300"
                : "bg-amber-400/15 text-amber-300"
            }`}
          >
            {answer.question_number}
          </div>

          <div className="min-w-0">
            <h3 className="break-words font-semibold text-white">
              {answer.title || `Question ${answer.question_number}`}
            </h3>

            <p className="mt-1 text-sm text-slate-400">
              {answer.difficulty ? `${answer.difficulty} · ` : ""}
              {passed}/{total} test cases passed
            </p>
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-3 pl-14 sm:pl-0">
          <span
            className={`rounded-full px-3 py-1 text-xs font-semibold ${
              answer.success
                ? "bg-emerald-400/10 text-emerald-300"
                : "bg-amber-400/10 text-amber-300"
            }`}
          >
            {answer.success ? "Passed" : "Needs review"}
          </span>

          <span className="text-sm font-semibold text-white">
            {formatPercent(score)}
          </span>

          <span className="text-slate-400">
            {expanded ? "−" : "+"}
          </span>
        </div>
      </button>

      {expanded && (
        <div className="space-y-5 border-t border-white/10 p-5">
          <div className="grid gap-3 sm:grid-cols-3">
            <div className="rounded-xl bg-white/[0.04] p-3">
              <p className="text-xs text-slate-500">Score</p>
              <p className="mt-1 font-semibold text-white">
                {formatPercent(score)}
              </p>
            </div>

            <div className="rounded-xl bg-white/[0.04] p-3">
              <p className="text-xs text-slate-500">Passed tests</p>
              <p className="mt-1 font-semibold text-emerald-300">
                {passed}
              </p>
            </div>

            <div className="rounded-xl bg-white/[0.04] p-3">
              <p className="text-xs text-slate-500">Failed tests</p>
              <p className="mt-1 font-semibold text-rose-300">
                {Number(
                  answer.failed_test_cases ??
                    Math.max(total - passed, 0),
                )}
              </p>
            </div>
          </div>

          <div>
            <div className="mb-2 flex items-center justify-between gap-3">
              <h4 className="text-sm font-semibold text-slate-200">
                Your submitted code
              </h4>

              <span className="text-xs text-slate-500">
                {displayLanguage(answer.language)}
              </span>
            </div>

            <pre className="max-h-[28rem] overflow-auto whitespace-pre-wrap break-words rounded-xl border border-white/10 bg-black/40 p-4 text-sm leading-6 text-slate-200">
              <code>
                {answer.code?.trim()
                  ? answer.code
                  : "No submitted code was saved for this question."}
              </code>
            </pre>
          </div>

          {answer.feedback && (
            <div className="rounded-xl border border-violet-400/20 bg-violet-400/[0.06] p-4">
              <h4 className="mb-2 text-sm font-semibold text-violet-200">
                Feedback
              </h4>

              <p className="whitespace-pre-wrap text-sm leading-6 text-slate-300">
                {answer.feedback}
              </p>
            </div>
          )}
        </div>
      )}
    </article>
  );
}

export default function CodingInterviewResult() {
  const navigate = useNavigate();
  const location = useLocation();
  const [searchParams] = useSearchParams();

  const locationState = (location.state ?? {}) as ResultLocationState;

  const { id: routeSessionId } = useParams<{ id: string }>();

  const parsedRouteSessionId = Number(routeSessionId);
  const querySessionId = Number(searchParams.get("sessionId"));

  const stateSessionId =
    locationState.sessionId !== undefined && locationState.sessionId !== null
      ? Number(locationState.sessionId)
      : undefined;

  // Supports navigation from history, direct URL navigation,
  // older query-string links, and navigation state.
  const sessionId =
    (Number.isFinite(stateSessionId) && (stateSessionId as number) > 0 ? (stateSessionId as number) : undefined) ??
    (Number.isFinite(parsedRouteSessionId) && parsedRouteSessionId > 0
      ? parsedRouteSessionId
      : Number.isFinite(querySessionId) && querySessionId > 0
        ? querySessionId
        : undefined);

  const [result, setResult] = useState<CodingInterviewResult | null>(
    locationState.result ?? null,
  );

  const [isLoading, setIsLoading] = useState(
    !locationState.result,
  );

  const [error, setError] = useState<string | null>(null);

  const [expandedQuestions, setExpandedQuestions] = useState<number[]>([]);

  useEffect(() => {
    sessionStorage.removeItem("codingInterviewViewingResults");
    invalidateCodingInterviewCache();

    if (locationState.result) {
      setResult(locationState.result);
      setError(null);
      setIsLoading(false);
      return;
    }

    if (!sessionId) {
      setError(
        "No interview result was provided. Open this page from a completed coding interview.",
      );
      setIsLoading(false);
      return;
    }

    let cancelled = false;

    setIsLoading(true);
    setError(null);

    getCodingInterviewResult(sessionId)
      .then((data) => {
        if (!cancelled) {
          setResult(data);
          setError(null);
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Unable to load the coding interview result.",
          );
        }
      })
      .finally(() => {
        if (!cancelled) {
          setIsLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [locationState.result, sessionId]);

  const answers = useMemo(
    () =>
      [...(result?.answers ?? [])].sort(
        (a, b) => a.question_number - b.question_number,
      ),
    [result?.answers],
  );

  if (isLoading) {
    return (
      <main className="app-background flex min-h-screen items-center justify-center px-4">
        <div className="text-center">
          <div className="mx-auto mb-4 h-9 w-9 animate-spin rounded-full border-2 border-white/10 border-t-violet-400" />

          <p className="text-sm text-slate-300">
            Loading your coding interview result…
          </p>
        </div>
      </main>
    );
  }

  if (error || !result) {
    return (
      <main className="app-background flex min-h-screen items-center justify-center px-4 py-12">
        <section className="w-full max-w-xl rounded-3xl border border-rose-400/20 bg-slate-950/70 p-8 text-center">
          <h1 className="text-2xl font-semibold text-white">
            Result unavailable
          </h1>

          <p className="mt-3 break-words text-sm leading-6 text-rose-200">
            {error ?? "The result could not be loaded."}
          </p>

          <div className="mt-6 flex flex-wrap justify-center gap-3">
            {sessionId && (
              <button
                onClick={() => {
                  setError(null);
                  setIsLoading(true);

                  getCodingInterviewResult(sessionId)
                    .then((data) => {
                      setResult(data);
                      setError(null);
                    })
                    .catch((err: unknown) => {
                      setError(
                        err instanceof Error
                          ? err.message
                          : "Unable to load result.",
                      );
                    })
                    .finally(() => setIsLoading(false));
                }}
                className="rounded-xl border border-white/15 px-5 py-3 text-sm font-semibold text-white hover:bg-white/5"
              >
                Try again
              </button>
            )}

            <button
              onClick={() => navigate("/home")}
              className="rounded-xl bg-violet-500 px-5 py-3 text-sm font-semibold text-white hover:bg-violet-400"
            >
              Back to home
            </button>
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className="app-background min-h-screen px-4 py-10 text-white sm:px-6 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <header className="mb-8">
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.35em] text-violet-300">
            Coding interview · Results
          </p>

          <div className="flex flex-col gap-5 md:flex-row md:items-end md:justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight sm:text-5xl">
                Your coding interview report
              </h1>

              <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400 sm:text-base">
                Review your performance, test-case results, submitted
                solutions, and feedback for every question.
              </p>
            </div>

            <button
              onClick={() => navigate("/home")}
              className="w-fit rounded-xl border border-white/15 px-5 py-3 text-sm font-semibold text-white transition hover:bg-white/5"
            >
              Back to home
            </button>
          </div>
        </header>

        <section className="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard
            label="Questions answered"
            value={`${Number(
              (
                result as CodingInterviewResult & {
                  solved_questions?: number;
                }
              ).solved_questions ?? result.attempted_questions,
            )}/${result.total_questions}`}
            detail={`${answers.length} submitted answer records`}
          />

          <StatCard
            label="Questions skipped"
            value={Number(
              (
                result as CodingInterviewResult & {
                  skipped_questions?: number;
                }
              ).skipped_questions ?? 0,
            )}
            detail="Explicitly skipped during the interview"
          />

          <StatCard
            label="Questions unanswered"
            value={
              result.unanswered_questions ??
              Math.max(
                result.total_questions - result.attempted_questions,
                0,
              )
            }
            detail="Questions not solved successfully"
          />

          <StatCard
            label="Test cases passed"
            value={`${result.passed_test_cases}/${result.total_test_cases}`}
            detail={`${result.failed_test_cases} failed`}
          />
        </section>

        <section className="mb-8 flex flex-wrap items-center gap-x-8 gap-y-3 rounded-2xl border border-white/10 bg-white/[0.035] px-5 py-4">
          <div>
            <p className="text-xs uppercase tracking-[0.18em] text-slate-500">
              Language
            </p>

            <p className="mt-1 font-semibold text-slate-100">
              {displayLanguage(result.language)}
            </p>
          </div>

          <div>
            <p className="text-xs uppercase tracking-[0.18em] text-slate-500">
              Difficulty
            </p>

            <p className="mt-1 font-semibold capitalize text-slate-100">
              {result.difficulty || "—"}
            </p>
          </div>
        </section>

        <section>
          <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="text-2xl font-bold">
                Question review
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Expand a question to inspect your code, score, and feedback.
              </p>
            </div>

            {answers.length > 0 && (
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() =>
                    setExpandedQuestions(
                      answers.map((answer) => answer.question_number),
                    )
                  }
                  className="rounded-lg border border-white/10 px-4 py-2 text-sm font-medium text-slate-300 transition hover:border-violet-400/40 hover:bg-white/5 hover:text-white"
                >
                  Expand all
                </button>

                <button
                  type="button"
                  onClick={() => setExpandedQuestions([])}
                  className="rounded-lg border border-white/10 px-4 py-2 text-sm font-medium text-slate-300 transition hover:border-violet-400/40 hover:bg-white/5 hover:text-white"
                >
                  Collapse all
                </button>
              </div>
            )}
          </div>

          {answers.length === 0 ? (
            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-8 text-center">
              <h3 className="font-semibold text-white">
                No submitted answers found
              </h3>

              <p className="mt-2 text-sm text-slate-400">
                The interview result was returned, but it contains no answer
                records to review.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {answers.map((answer) => (
                <QuestionReview
                  key={`${answer.question_number}-${answer.coding_question_id}`}
                  answer={answer}
                  expanded={expandedQuestions.includes(
                    answer.question_number,
                  )}
                  onToggle={() =>
                    setExpandedQuestions((current) =>
                      current.includes(answer.question_number)
                        ? current.filter(
                            (number) =>
                              number !== answer.question_number,
                          )
                        : [...current, answer.question_number],
                    )
                  }
                />
              ))}
            </div>
          )}
        </section>

        <footer className="mt-10 flex flex-col justify-between gap-4 border-t border-white/10 pt-6 sm:flex-row sm:items-center">
          <p className="text-xs text-slate-500">
            Your result is based on the answers and test-case data returned by
            the server.
          </p>

          <button
            onClick={() => navigate("/coding-interview/new")}
            className="rounded-xl bg-violet-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-violet-400"
          >
            Start another interview
          </button>
        </footer>
      </div>
    </main>
  );
}