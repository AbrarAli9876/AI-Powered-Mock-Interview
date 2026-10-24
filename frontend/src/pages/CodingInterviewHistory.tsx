import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getCodingInterviews,
  type CodingInterview,
} from "../lib/api";

function formatDateTime(value: string): string {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "Date unavailable";
  }

  return date.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function statusLabel(status: CodingInterview["status"]): string {
  if (status === "completed") return "Completed";
  if (status === "abandoned") return "Abandoned";
  return "In Progress";
}

function statusClass(status: CodingInterview["status"]): string {
  if (status === "completed") {
    return "dashboard-status dashboard-status-success";
  }

  if (status === "in_progress") {
    return "dashboard-status dashboard-status-warning";
  }

  return "dashboard-status dashboard-status-danger";
}

function languageLabel(language: string): string {
  const labels: Record<string, string> = {
    python: "Python",
    javascript: "JavaScript",
    java: "Java",
    cpp: "C++",
    "c++": "C++",
  };

  return labels[language.toLowerCase()] ?? language;
}

function safeNumber(value: unknown): number {
  const number = typeof value === "number" ? value : Number(value);

  return Number.isFinite(number) && number >= 0 ? number : 0;
}

export default function CodingInterviewHistory() {
  const navigate = useNavigate();

  const [interviews, setInterviews] = useState<CodingInterview[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadInterviews() {
      try {
        setLoading(true);
        setError(null);

        const items = await getCodingInterviews();

        if (cancelled) return;

        const sorted = [...items].sort(
          (a, b) =>
            new Date(b.created_at).getTime() -
            new Date(a.created_at).getTime(),
        );

        setInterviews(sorted);
      } catch (err: unknown) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Unable to load coding interview history.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadInterviews();

    return () => {
      cancelled = true;
    };
  }, []);

  function openResults(interviewId: number | string) {
    navigate(`/coding-interview/results/${encodeURIComponent(String(interviewId))}`);
  }

  return (
    <div className="dashboard-page">
      <div className="dashboard-container">
        <header className="dashboard-header">
          <div>
            <div className="dashboard-eyebrow">
              CODING INTERVIEW HISTORY
            </div>

            <h1>Your coding interviews</h1>

            <p>
              Review your coding sessions, submitted solutions, and
              test-case feedback. Coding results remain separate from
              technical interview reports.
            </p>
          </div>

          <div className="dashboard-header-actions">
            <button
              type="button"
              className="dashboard-primary-button"
              onClick={() => navigate("/home")}
            >
              <span aria-hidden="true">←</span>
              Back to Home
            </button>
          </div>
        </header>

        <section className="dashboard-section">
          <div className="dashboard-section-header">
            <div>
              <div className="dashboard-eyebrow">
                INTERVIEW HISTORY
              </div>

              <h2>Your coding sessions</h2>

              <p>Most recent interviews appear first.</p>
            </div>

            {!loading && !error && (
              <span className="dashboard-count">
                {interviews.length}{" "}
                {interviews.length === 1
                  ? "interview"
                  : "interviews"}
              </span>
            )}
          </div>

          {loading && (
            <div className="dashboard-loading" role="status">
              Loading your coding interview history...
            </div>
          )}

          {!loading && error && (
            <div className="dashboard-error" role="alert">
              <h2>Unable to load coding interviews</h2>
              <p>{error}</p>

              <button
                type="button"
                className="dashboard-button"
                onClick={() => window.location.reload()}
              >
                Try Again
              </button>
            </div>
          )}

          {!loading && !error && interviews.length === 0 && (
            <div className="dashboard-empty">
              <div
                className="dashboard-empty-icon"
                aria-hidden="true"
              >
                &lt;/&gt;
              </div>

              <h3>No coding interviews yet</h3>

              <p>
                Start a coding interview to practice problems and
                see your saved results here.
              </p>

              <button
                type="button"
                className="dashboard-primary-button"
                onClick={() => navigate("/coding-interview/new")}
              >
                Start Coding Interview
                <span aria-hidden="true">→</span>
              </button>
            </div>
          )}

          {!loading && !error && interviews.length > 0 && (
            <div className="dashboard-interview-list">
              {interviews.map((interview, index) => {
                const canViewResult =
                  interview.status !== "in_progress";

                const totalQuestions = safeNumber(
                  interview.total_questions,
                );

                const currentQuestion = Math.min(
                  safeNumber(interview.current_question_number),
                  totalQuestions,
                );

                return (
                  <article
                    className="dashboard-interview-card coding-history-card"
                    key={interview.id}
                  >
                    <div className="dashboard-interview-number">
                      #{interviews.length - index}
                    </div>

                    <div className="dashboard-interview-main">
                      <div className="dashboard-interview-top">
                        <div>
                          <h3>Coding Interview</h3>

                          <p>
                            {formatDateTime(interview.created_at)}
                          </p>
                        </div>

                        <span
                          className={statusClass(interview.status)}
                        >
                          {statusLabel(interview.status)}
                        </span>
                      </div>

                      <div className="dashboard-interview-meta coding-history-meta">
                        <div>
                          <span>LANGUAGE</span>
                          <strong>
                            {languageLabel(interview.language)}
                          </strong>
                        </div>

                        <div>
                          <span>DIFFICULTY</span>
                          <strong className="capitalize">
                            {interview.difficulty}
                          </strong>
                        </div>

                        <div>
                          <span>QUESTIONS</span>
                          <strong>{totalQuestions}</strong>
                        </div>

                        <div>
                          <span>PROGRESS</span>
                          <strong>
                            {currentQuestion}/{totalQuestions}
                          </strong>
                        </div>
                      </div>
                    </div>

                    <div className="dashboard-interview-score coding-history-report">
                      {canViewResult ? (
                        <button
                          type="button"
                          className="dashboard-view-button"
                          onClick={() => openResults(interview.id)}
                        >
                          View Results
                          <span aria-hidden="true">→</span>
                        </button>
                      ) : (
                        <span className="coding-history-in-progress">
                          In Progress
                        </span>
                      )}
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
