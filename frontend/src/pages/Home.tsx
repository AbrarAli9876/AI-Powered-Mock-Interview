
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getInterviews, getTopics } from "../lib/api";
import type { Interview, Topic } from "../lib/api";

interface CurrentUser {
  id: number;
  full_name: string;
  email: string;
  role: "user" | "admin" | "candidate";
  is_active: boolean;
}

function toNumber(value: number | string | null | undefined): number | null {
  if (value === null || value === undefined || value === "") return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

/**
 * Interpret timezone-naive backend timestamps as UTC.
 * Then display the converted date in the user's local timezone.
 *
 * Example: 2026-10-09T12:40:00 (UTC)
 * displays as 6:10 PM in India.
 */
function parseBackendDate(value: string): Date {
  const hasTimezone = /(?:Z|[+-]\d{2}:?\d{2})$/i.test(value.trim());
  const normalized = hasTimezone ? value : `${value}Z`;
  return new Date(normalized);
}

function formatDateTime(value: string): string {
  if (!value) return "Date unavailable";

  const date = parseBackendDate(value);

  if (Number.isNaN(date.getTime())) return "Date unavailable";

  return date.toLocaleString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function formatDate(value: string): string {
  if (!value) return "Date unavailable";

  const date = parseBackendDate(value);

  if (Number.isNaN(date.getTime())) return "Date unavailable";

  return date.toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function capitalize(value: string | null | undefined): string {
  if (!value) return "Unknown";

  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function getStatusClass(status: Interview["status"]): string {
  switch (status) {
    case "completed":
      return "border-emerald-400/20 bg-emerald-400/[0.06] text-emerald-300";
    case "in_progress":
      return "border-amber-400/20 bg-amber-400/[0.06] text-amber-300";
    default:
      return "border-white/[0.08] bg-white/[0.03] text-slate-400";
  }
}

function getScoreClass(value: number | string | null | undefined): string {
  const score = toNumber(value);

  if (score === null) return "text-slate-500";
  if (score >= 80) return "text-emerald-300";
  if (score >= 60) return "text-amber-300";
  return "text-rose-300";
}

function formatScore(value: number | string | null | undefined): string {
  const score = toNumber(value);
  return score === null ? "—" : score.toFixed(0);
}

export default function Home() {
  const navigate = useNavigate();

  const [user, setUser] = useState<CurrentUser | null>(null);
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [historyError, setHistoryError] = useState<string | null>(null);

  // Authenticate the user.
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const storedUser = localStorage.getItem("user");

    if (!token || !storedUser) {
      navigate("/login", { replace: true });
      return;
    }

    try {
      const parsedUser = JSON.parse(storedUser) as CurrentUser;

      if (parsedUser.role === "admin") {
        navigate("/admin", { replace: true });
        return;
      }

      setUser(parsedUser);
      setIsLoading(false);
    } catch {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      navigate("/login", { replace: true });
    }
  }, [navigate]);

  // Load interviews and topics.
  useEffect(() => {
    if (!user) return;

    let cancelled = false;

    async function loadHistory() {
      setHistoryLoading(true);
      setHistoryError(null);

      try {
        const [interviewData, topicData] = await Promise.all([
          getInterviews(),
          getTopics().catch((error: unknown) => {
            console.error("Could not load topics:", error);
            return [] as Topic[];
          }),
        ]);

        if (cancelled) return;

        const sorted = [...interviewData].sort((a, b) => {
          const dateA = parseBackendDate(a.created_at).getTime();
          const dateB = parseBackendDate(b.created_at).getTime();

          if (
            Number.isFinite(dateA) &&
            Number.isFinite(dateB) &&
            dateA !== dateB
          ) {
            return dateB - dateA;
          }

          return b.id - a.id;
        });

        setInterviews(sorted);
        setTopics(topicData);
      } catch (error) {
        if (cancelled) return;

        console.error("Could not load interview history:", error);
        setHistoryError(
          error instanceof Error
            ? error.message
            : "Unable to load interview history.",
        );
      } finally {
        if (!cancelled) setHistoryLoading(false);
      }
    }

    void loadHistory();

    return () => {
      cancelled = true;
    };
  }, [user]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    navigate("/login", { replace: true });
  };

  const firstName = user?.full_name?.trim().split(/\s+/)[0] || "there";

  const topicMap = useMemo(() => {
    const map = new Map<number, string>();
    topics.forEach((topic) => map.set(topic.id, topic.name));
    return map;
  }, [topics]);

  const recentInterviews = interviews.slice(0, 3);

  const completedInterviews = interviews.filter(
    (interview) => interview.status === "completed",
  );

  const inProgressCount = interviews.filter(
    (interview) => interview.status === "in_progress",
  ).length;

  const averageScore = useMemo(() => {
    const scores = completedInterviews
      .map((interview) => toNumber(interview.overall_score))
      .filter((score): score is number => score !== null);

    if (scores.length === 0) return null;

    return scores.reduce((sum, score) => sum + score, 0) / scores.length;
  }, [completedInterviews]);

  if (isLoading) {
    return (
      <div className="app-background flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-10 w-10 animate-spin rounded-full border-2 border-white/10 border-t-violet-400" />
          <p className="mt-4 font-mono text-[10px] uppercase tracking-[0.18em] text-slate-600">
            Loading workspace
          </p>
        </div>
      </div>
    );
  }

  if (!user) return null;

  return (
    <div className="app-background min-h-screen">
      <div className="app-grid" />
      <div className="glow-orb glow-orb-violet left-[-150px] top-[180px] animate-pulse-slow" />
      <div className="glow-orb glow-orb-cyan right-[-120px] top-[320px] animate-pulse-slow" />

      {/* Navigation */}
      <header className="relative z-20 border-b border-white/[0.06] bg-black/10">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5 lg:px-10">
          <button
            type="button"
            onClick={() => navigate("/home")}
            className="flex items-center gap-3 text-left"
            aria-label="Go to home"
          >
            <div className="relative flex h-10 w-10 items-center justify-center overflow-hidden rounded-xl border border-violet-400/30 bg-violet-500/10 shadow-glow">
              <div className="absolute inset-0 bg-gradient-to-br from-violet-500/20 to-cyan-400/10" />
              <span className="relative font-display text-sm font-bold text-violet-300">
                AI
              </span>
            </div>

            <div>
              <div className="font-display text-sm font-semibold tracking-wide text-white">
                MOCK INTERVIEW
              </div>
              <div className="font-mono text-[9px] uppercase tracking-[0.2em] text-slate-600">
                Candidate workspace
              </div>
            </div>
          </button>

          <div className="flex items-center gap-4">
            <div className="hidden text-right sm:block">
              <div className="text-sm font-medium text-slate-200">
                {user.full_name}
              </div>
              <div className="font-mono text-[9px] uppercase tracking-[0.16em] text-slate-600">
                Candidate
              </div>
            </div>

            <div className="hidden h-9 w-px bg-white/[0.08] sm:block" />

            <button
              type="button"
              onClick={handleLogout}
              className="rounded-lg border border-white/10 bg-white/[0.025] px-4 py-2 text-sm font-medium text-slate-400 transition hover:border-red-400/20 hover:bg-red-400/[0.04] hover:text-red-300"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="relative z-10 mx-auto max-w-7xl px-6 py-10 lg:px-10 lg:py-14">
        {/* Greeting */}
        <section className="mb-10">
          <div className="font-mono text-[10px] uppercase tracking-[0.2em] text-violet-400">
            Candidate workspace
          </div>

          <div className="mt-3 flex flex-col justify-between gap-5 lg:flex-row lg:items-end">
            <div>
              <h1 className="font-display text-4xl font-semibold leading-tight tracking-[-0.035em] text-white sm:text-5xl">
                Good to see you,{" "}
                <span className="bg-gradient-to-r from-violet-300 to-cyan-300 bg-clip-text text-transparent">
                  {firstName}.
                </span>
              </h1>

              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-500">
                Ready for your next challenge? Practice under realistic
                interview conditions and turn your answers into measurable
                progress.
              </p>
            </div>

            <div className="flex w-fit items-center gap-2 rounded-full border border-emerald-400/10 bg-emerald-400/[0.035] px-3 py-2">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-[0_0_10px_rgba(52,211,153,0.8)]" />
              <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-emerald-400/80">
                Interview engine ready
              </span>
            </div>
          </div>
        </section>

        {/* Technical interview and performance */}
        <section className="grid gap-5 lg:grid-cols-[1.4fr_1fr]">
          <div className="group relative overflow-hidden rounded-3xl border border-violet-400/15 bg-gradient-to-br from-violet-500/[0.13] via-white/[0.035] to-cyan-400/[0.04] p-8 shadow-glow transition-all duration-500 hover:border-violet-400/25">
            <div className="absolute right-[-100px] top-[-100px] h-72 w-72 rounded-full bg-violet-500/[0.08] blur-3xl transition-transform duration-700 group-hover:scale-125" />

            <div className="relative">
              <div className="inline-flex items-center gap-2 rounded-full border border-white/[0.08] bg-black/10 px-3 py-1.5">
                <span className="h-1.5 w-1.5 rounded-full bg-violet-400" />
                <span className="font-mono text-[9px] uppercase tracking-[0.16em] text-violet-300/80">
                  New session
                </span>
              </div>

              <h2 className="mt-7 max-w-xl font-display text-3xl font-semibold leading-tight tracking-tight text-white sm:text-4xl">
                Put your technical skills under pressure.
              </h2>

              <p className="mt-4 max-w-lg text-sm leading-6 text-slate-400">
                Choose a topic and starting difficulty. The AI interviewer
                adapts the conversation based on your performance.
              </p>

              <button
                type="button"
                onClick={() => navigate("/interviews/new")}
                className="group/button mt-8 inline-flex items-center gap-3 rounded-xl bg-white px-6 py-3.5 font-display text-sm font-semibold text-slate-950 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-[0_15px_45px_rgba(139,92,246,0.25)] active:translate-y-0"
              >
                Start technical interview
                <span className="transition-transform duration-300 group-hover/button:translate-x-1">
                  →
                </span>
              </button>

              <div className="mt-8 flex flex-wrap gap-x-7 gap-y-3 border-t border-white/[0.06] pt-6">
                <div>
                  <div className="font-mono text-[9px] uppercase tracking-[0.15em] text-slate-600">
                    Difficulty
                  </div>
                  <div className="mt-1 text-xs text-slate-300">Adaptive</div>
                </div>
                <div>
                  <div className="font-mono text-[9px] uppercase tracking-[0.15em] text-slate-600">
                    Evaluation
                  </div>
                  <div className="mt-1 text-xs text-slate-300">AI-powered</div>
                </div>
                <div>
                  <div className="font-mono text-[9px] uppercase tracking-[0.15em] text-slate-600">
                    Feedback
                  </div>
                  <div className="mt-1 text-xs text-slate-300">Detailed report</div>
                </div>
              </div>
            </div>
          </div>

          {/* Performance metrics */}
          <div className="glass-panel rounded-3xl p-7">
            <div className="font-mono text-[10px] uppercase tracking-[0.18em] text-slate-600">
              Your performance
            </div>

            <div className="mt-7">
              <div className="font-display text-5xl font-semibold tracking-tight text-white">
                {averageScore === null ? "—" : averageScore.toFixed(0)}
              </div>
              <div className="mt-2 text-sm text-slate-500">
                Average score across completed interviews
              </div>
            </div>

            <div className="mt-8 grid grid-cols-2 gap-3">
              <div className="rounded-2xl border border-white/[0.06] bg-white/[0.025] p-5">
                <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-slate-600">
                  Completed
                </div>
                <div className="mt-3 font-display text-3xl font-semibold text-white">
                  {completedInterviews.length}
                </div>
                <div className="mt-1 text-xs text-slate-600">
                  Finished sessions
                </div>
              </div>

              <div className="rounded-2xl border border-white/[0.06] bg-white/[0.025] p-5">
                <div className="font-mono text-[10px] uppercase tracking-[0.16em] text-slate-600">
                  In progress
                </div>
                <div className="mt-3 font-display text-3xl font-semibold text-white">
                  {inProgressCount}
                </div>
                <div className="mt-1 text-xs text-slate-600">
                  Active sessions
                </div>
              </div>
            </div>

            <div className="mt-4 rounded-xl border border-white/[0.06] bg-white/[0.02] p-4">
              <div className="font-mono text-[9px] uppercase tracking-[0.15em] text-slate-600">
                Total sessions
              </div>
              <div className="mt-2 font-display text-2xl font-semibold text-white">
                {interviews.length}
              </div>
            </div>
          </div>
        </section>

        {/* Quick actions — including Coding Interview */}
        <section className="mt-8">
          <div className="mb-4 font-mono text-[10px] uppercase tracking-[0.18em] text-slate-600">
            Quick actions
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <button
              type="button"
              onClick={() => navigate("/dashboard")}
              className="group rounded-2xl border border-white/[0.06] bg-white/[0.02] p-5 text-left transition-all duration-300 hover:-translate-y-0.5 hover:border-violet-400/20 hover:bg-white/[0.035]"
            >
              <div className="flex items-center justify-between">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-violet-400/10 bg-violet-500/[0.06]">
                  <span className="font-mono text-xs text-violet-300">↗</span>
                </div>
                <span className="text-slate-700 transition-transform group-hover:translate-x-1">→</span>
              </div>
              <h3 className="mt-5 font-display text-base font-semibold text-white">
                Performance dashboard
              </h3>
              <p className="mt-2 text-xs leading-5 text-slate-600">
                Review scores, progress, and interview history.
              </p>
            </button>

            <button
              type="button"
              onClick={() => navigate("/coding-interview/new")}
              className="group rounded-2xl border border-white/[0.06] bg-white/[0.02] p-5 text-left transition-all duration-300 hover:-translate-y-0.5 hover:border-cyan-400/20 hover:bg-white/[0.035]"
            >
              <div className="flex items-center justify-between">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-400/10 bg-cyan-400/[0.05]">
                  <span className="font-mono text-xs text-cyan-300">{"</>"}</span>
                </div>
                <span className="text-slate-700 transition-transform group-hover:translate-x-1">→</span>
              </div>
              <h3 className="mt-5 font-display text-base font-semibold text-white">
                Coding interview
              </h3>
              <p className="mt-2 text-xs leading-5 text-slate-600">
                Solve coding problems, run your code, and test your solutions.
              </p>
            </button>

            <button
              type="button"
              onClick={() => navigate("/profile")}
              className="group rounded-2xl border border-white/[0.06] bg-white/[0.02] p-5 text-left transition-all duration-300 hover:-translate-y-0.5 hover:border-cyan-400/20 hover:bg-white/[0.035]"
            >
              <div className="flex items-center justify-between">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-400/10 bg-cyan-400/[0.05]">
                  <span className="font-mono text-xs text-cyan-300">ID</span>
                </div>
                <span className="text-slate-700 transition-transform group-hover:translate-x-1">→</span>
              </div>
              <h3 className="mt-5 font-display text-base font-semibold text-white">
                Your profile
              </h3>
              <p className="mt-2 text-xs leading-5 text-slate-600">
                Manage your account information and preferences.
              </p>
            </button>
          </div>
        </section>

        {/* Recent interview history */}
        <section className="mt-8">
          <div className="glass-panel overflow-hidden rounded-3xl">
            <div className="flex flex-col gap-4 border-b border-white/[0.06] p-7 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <div className="font-mono text-[10px] uppercase tracking-[0.18em] text-violet-400">
                  Interview history
                </div>
                <h2 className="mt-2 font-display text-xl font-semibold text-white">
                  Recent interviews
                </h2>
                <p className="mt-2 text-xs text-slate-500">
                  Showing your three most recent sessions.
                </p>
              </div>

              <div className="font-mono text-[10px] uppercase tracking-[0.15em] text-slate-500">
                {interviews.length}{" "}
                {interviews.length === 1 ? "session" : "sessions"}
              </div>
            </div>

            <div className="p-7">
              {historyLoading ? (
                <div className="py-12 text-center text-sm text-slate-500">
                  Loading interview history...
                </div>
              ) : historyError ? (
                <div
                  role="alert"
                  className="rounded-2xl border border-red-400/20 bg-red-400/[0.04] p-6 text-sm text-red-300"
                >
                  <p className="font-semibold">
                    Could not load interview history.
                  </p>
                  <p className="mt-2 break-words text-xs">{historyError}</p>
                  <button
                    type="button"
                    onClick={() => window.location.reload()}
                    className="mt-4 rounded-lg border border-white/10 px-4 py-2 text-xs text-white hover:bg-white/[0.05]"
                  >
                    Retry
                  </button>
                </div>
              ) : recentInterviews.length === 0 ? (
                <div className="flex min-h-56 items-center justify-center rounded-2xl border border-dashed border-white/[0.08] bg-white/[0.012]">
                  <div className="max-w-sm px-5 text-center">
                    <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-white/[0.07] bg-white/[0.025]">
                      <span className="font-mono text-xs tracking-widest text-slate-600">
                        01
                      </span>
                    </div>
                    <h3 className="mt-5 font-display text-base font-semibold text-slate-300">
                      Your interview history is empty.
                    </h3>
                    <p className="mt-2 text-xs leading-5 text-slate-600">
                      Complete your first interview to start tracking your
                      technical performance and growth.
                    </p>
                    <button
                      type="button"
                      onClick={() => navigate("/interviews/new")}
                      className="mt-5 rounded-lg border border-violet-400/20 bg-violet-500/[0.07] px-4 py-2.5 font-mono text-[10px] uppercase tracking-[0.12em] text-violet-300 transition hover:bg-violet-500/[0.12]"
                    >
                      Start your first interview
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  {recentInterviews.map((interview, index) => {
                    const topicName =
                      topicMap.get(interview.topic_id) ??
                      `Topic #${interview.topic_id}`;

                    return (
                      <article
                        key={interview.id}
                        className="group rounded-2xl border border-white/[0.06] bg-white/[0.02] p-5 transition-all duration-300 hover:border-violet-400/20 hover:bg-white/[0.035]"
                      >
                        <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
                          <div className="flex min-w-0 items-start gap-4">
                            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-violet-400/10 bg-violet-500/[0.06] font-mono text-xs text-violet-300">
                              {String(index + 1).padStart(2, "0")}
                            </div>

                            <div className="min-w-0">
                              <h3 className="truncate font-display text-base font-semibold text-white">
                                {topicName} Interview
                              </h3>
                              <p className="mt-1 text-xs text-slate-500">
                                {formatDateTime(interview.created_at)}
                              </p>

                              <div className="mt-3 flex flex-wrap items-center gap-2">
                                <span className={`rounded-full border px-2.5 py-1 text-[10px] ${getStatusClass(interview.status)}`}>
                                  {capitalize(interview.status)}
                                </span>
                                <span className="rounded-full border border-white/[0.07] bg-white/[0.02] px-2.5 py-1 text-[10px] text-slate-400">
                                  {capitalize(interview.current_difficulty)}
                                </span>
                                <span className="rounded-full border border-white/[0.07] bg-white/[0.02] px-2.5 py-1 text-[10px] text-slate-400">
                                  {interview.current_question_number}/{interview.total_questions} questions
                                </span>
                              </div>
                            </div>
                          </div>

                          <div className="flex shrink-0 items-center justify-between gap-5 border-t border-white/[0.06] pt-4 sm:flex-col sm:items-end sm:border-t-0 sm:pt-0">
                            <div className="sm:text-right">
                              <div className="font-mono text-[9px] uppercase tracking-[0.15em] text-slate-600">
                                Score
                              </div>
                              <div className={`mt-1 font-display text-2xl font-semibold ${getScoreClass(interview.overall_score)}`}>
                                {formatScore(interview.overall_score)}
                                {toNumber(interview.overall_score) !== null && (
                                  <span className="ml-1 text-xs text-slate-600">/ 100</span>
                                )}
                              </div>
                            </div>

                            <button
                              type="button"
                              disabled={interview.status === "abandoned"}
                              onClick={() => {
                                if (interview.status === "completed") {
                                  navigate(`/interviews/${interview.id}/result`);
                                } else if (interview.status === "in_progress") {
                                  navigate(`/interviews/${interview.id}`);
                                }
                              }}
                              className="inline-flex items-center gap-2 rounded-lg border border-violet-400/20 bg-violet-500/[0.06] px-3 py-2 text-xs font-medium text-violet-300 transition hover:bg-violet-500/[0.12] disabled:cursor-not-allowed disabled:opacity-40"
                            >
                              {interview.status === "completed"
                                ? "View report"
                                : interview.status === "in_progress"
                                  ? "Continue"
                                  : "Abandoned"}
                              {interview.status !== "abandoned" && " →"}
                            </button>
                          </div>
                        </div>
                      </article>
                    );
                  })}

                  {interviews.length > 3 && (
                    <div className="flex flex-col items-center justify-center gap-3 border-t border-white/[0.06] pt-6 text-center">
                      <p className="text-xs text-slate-500">
                        Showing 3 of {interviews.length} interview sessions.
                      </p>
                      <button
                        type="button"
                        onClick={() => navigate("/dashboard")}
                        className="rounded-lg border border-white/[0.08] bg-white/[0.025] px-5 py-2.5 font-mono text-[10px] uppercase tracking-[0.12em] text-slate-300 transition hover:border-violet-400/20 hover:bg-violet-500/[0.05] hover:text-violet-300"
                      >
                        View all interviews →
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="mt-12 border-t border-white/[0.05] py-7">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div className="font-mono text-[9px] uppercase tracking-[0.15em] text-slate-700">
              © 2026 AI Mock Interview
            </div>
            <div className="font-mono text-[9px] uppercase tracking-[0.15em] text-slate-700">
              Intelligent practice · Better interviews
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}
