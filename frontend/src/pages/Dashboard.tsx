import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getInterviews,
  getTopics,
  type Difficulty,
  type Interview,
  type Topic,
} from "../lib/api";

const DASHBOARD_CACHE_KEY = "technicalInterviewDashboardCache";

type DashboardCache = {
  interviews: Interview[];
  topics: Topic[];
  cachedAt: number;
};

function readDashboardCache(): DashboardCache | null {
  try {
    const raw = sessionStorage.getItem(DASHBOARD_CACHE_KEY);
    if (!raw) return null;

    const cache: DashboardCache = JSON.parse(raw);

    if (
      !Array.isArray(cache.interviews) ||
      !Array.isArray(cache.topics)
    ) {
      return null;
    }

    return cache;
  } catch {
    return null;
  }
}

function writeDashboardCache(
  interviews: Interview[],
  topics: Topic[],
): void {
  try {
    const cache: DashboardCache = {
      interviews,
      topics,
      cachedAt: Date.now(),
    };

    sessionStorage.setItem(
      DASHBOARD_CACHE_KEY,
      JSON.stringify(cache),
    );
  } catch {
    // The dashboard must continue working if storage is unavailable.
  }
}

/**
 * Call this after an interview is completed or its result is updated.
 * The next dashboard visit will fetch fresh data from the backend.
 */


function sortInterviews(interviews: Interview[]): Interview[] {
  return [...interviews].sort(
    (a, b) =>
      new Date(b.created_at).getTime() -
      new Date(a.created_at).getTime(),
  );
}

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function formatDateTime(dateString: string): string {
  return new Date(dateString).toLocaleString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function capitalize(value: string): string {
  if (!value) return value;
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function getDifficultyLabel(difficulty: Difficulty): string {
  return capitalize(difficulty);
}

function getStatusLabel(status: Interview["status"]): string {
  if (status === "in_progress") return "In Progress";
  if (status === "completed") return "Completed";
  return "Abandoned";
}

function getStatusClass(status: Interview["status"]): string {
  if (status === "completed") {
    return "dashboard-status dashboard-status-success";
  }

  if (status === "in_progress") {
    return "dashboard-status dashboard-status-warning";
  }

  return "dashboard-status dashboard-status-danger";
}

function getScoreClass(score: number | null): string {
  if (score === null) {
    return "dashboard-score dashboard-score-muted";
  }

  if (score >= 80) {
    return "dashboard-score dashboard-score-good";
  }

  if (score >= 60) {
    return "dashboard-score dashboard-score-average";
  }

  return "dashboard-score dashboard-score-low";
}

/**
 * API responses can contain scores as numbers or numeric strings.
 * Normalize them before calculations or calling number methods.
 */
function toNumericScore(value: unknown): number | null {
  if (value === null || value === undefined || value === "") {
    return null;
  }

  const numericValue =
    typeof value === "number" ? value : Number(value);

  return Number.isFinite(numericValue) ? numericValue : null;
}

export default function Dashboard() {
  const navigate = useNavigate();

  // Read cached data synchronously, before the first render.
  const [initialCache] = useState<DashboardCache | null>(
    () => readDashboardCache(),
  );

  const [interviews, setInterviews] = useState<Interview[]>(
    () => initialCache?.interviews ?? [],
  );

  const [topics, setTopics] = useState<Topic[]>(
    () => initialCache?.topics ?? [],
  );

  const [loading, setLoading] = useState(!initialCache);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const loadDashboard = useCallback(
    async (showLoading: boolean) => {
      if (showLoading) {
        setLoading(true);
      } else {
        setRefreshing(true);
      }

      setError(null);

      try {
        const [interviewData, topicData] = await Promise.all([
          getInterviews(),
          getTopics(),
        ]);

        const sortedInterviews = sortInterviews(interviewData);

        setInterviews(sortedInterviews);
        setTopics(topicData);

        writeDashboardCache(sortedInterviews, topicData);
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : "Failed to load dashboard.";

        // Keep cached content visible if a background refresh fails.
        if (showLoading) {
          setError(message);
        } else {
          console.error("Dashboard background refresh failed:", err);
        }
      } finally {
        setLoading(false);
        setRefreshing(false);
      }
    },
    [],
  );

  useEffect(() => {
    let isMounted = true;

    async function refresh() {
      try {
        const [interviewData, topicData] = await Promise.all([
          getInterviews(),
          getTopics(),
        ]);

        if (!isMounted) return;

        const sortedInterviews = sortInterviews(interviewData);

        setInterviews(sortedInterviews);
        setTopics(topicData);
        setError(null);

        writeDashboardCache(sortedInterviews, topicData);
      } catch (err) {
        if (!isMounted) return;

        if (!initialCache) {
          setError(
            err instanceof Error
              ? err.message
              : "Failed to load dashboard.",
          );
        } else {
          // Existing cached data remains visible.
          console.error("Dashboard background refresh failed:", err);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
          setRefreshing(false);
        }
      }
    }

    void refresh();

    return () => {
      isMounted = false;
    };
  }, [initialCache]);

  const topicMap = useMemo(() => {
    const map = new Map<number, string>();

    topics.forEach((topic) => {
      map.set(topic.id, topic.name);
    });

    return map;
  }, [topics]);

  const completedInterviews = useMemo(
    () =>
      interviews.filter(
        (interview) => interview.status === "completed",
      ),
    [interviews],
  );

  const scores = useMemo(
    () =>
      completedInterviews
        .map((interview) => toNumericScore(interview.overall_score))
        .filter((score): score is number => score !== null),
    [completedInterviews],
  );

  const averageScore =
    scores.length > 0
      ? scores.reduce((sum, score) => sum + score, 0) /
        scores.length
      : null;

  const bestScore = scores.length > 0 ? Math.max(...scores) : null;

  // Interviews are sorted newest-first, so scores follow that order.
  const latestScore = scores.length > 0 ? scores[0] : null;
  const previousScore = scores.length > 1 ? scores[1] : null;

  const improvement =
    latestScore !== null && previousScore !== null
      ? latestScore - previousScore
      : null;

  const performanceInterviews = useMemo(
    () =>
      [...completedInterviews]
        .reverse()
        .filter((interview) => interview.overall_score !== null),
    [completedInterviews],
  );

  const handleInterviewClick = (interview: Interview) => {
    if (interview.status === "completed") {
      navigate(`/interviews/${interview.id}/result`);
      return;
    }

    if (interview.status === "in_progress") {
      navigate(`/interviews/${interview.id}`);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-container">
          <div className="dashboard-loading">
            Loading your performance dashboard...
          </div>
        </div>
      </div>
    );
  }

  if (error && interviews.length === 0 && topics.length === 0) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-container">
          <div className="dashboard-error">
            <h2>Unable to load dashboard</h2>
            <p>{error}</p>

            <button
              className="dashboard-button"
              onClick={() => void loadDashboard(true)}
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div className="dashboard-container">
        {/* HEADER */}
        <header className="dashboard-header">
          <div>
            <div className="dashboard-eyebrow">
              PERFORMANCE CENTER
            </div>

            <h1>Your Interview Performance</h1>

            <p>
              Track your progress, review previous interviews, and
              understand where you can improve.
            </p>

            {refreshing && (
              <p className="text-xs text-slate-500" aria-live="polite">
                Updating your dashboard...
              </p>
            )}
          </div>

          <button
            className="dashboard-primary-button"
            onClick={() => navigate("/interviews/new")}
          >
            Start New Interview
            <span>→</span>
          </button>
        </header>

        {error && (
          <div className="dashboard-error" role="status">
            Could not refresh the latest data. Showing the last
            available dashboard data.
          </div>
        )}

        {/* OVERVIEW */}
        <section className="dashboard-overview">
          <div className="dashboard-stat-card">
            <span className="dashboard-stat-label">
              TOTAL INTERVIEWS
            </span>
            <strong>{interviews.length}</strong>
            <span className="dashboard-stat-description">
              All interview sessions
            </span>
          </div>

          <div className="dashboard-stat-card">
            <span className="dashboard-stat-label">COMPLETED</span>
            <strong>{completedInterviews.length}</strong>
            <span className="dashboard-stat-description">
              Successfully completed
            </span>
          </div>

          <div className="dashboard-stat-card">
            <span className="dashboard-stat-label">
              AVERAGE SCORE
            </span>
            <strong>
              {averageScore !== null
                ? averageScore.toFixed(0)
                : "—"}
            </strong>
            <span className="dashboard-stat-description">
              Across completed interviews
            </span>
          </div>

          <div className="dashboard-stat-card">
            <span className="dashboard-stat-label">BEST SCORE</span>
            <strong>
              {bestScore !== null ? bestScore.toFixed(0) : "—"}
            </strong>
            <span className="dashboard-stat-description">
              Your highest performance
            </span>
          </div>
        </section>

        {/* PERFORMANCE TREND */}
        {performanceInterviews.length > 0 && (
          <section className="dashboard-section">
            <div className="dashboard-section-header">
              <div>
                <div className="dashboard-eyebrow">PROGRESS</div>
                <h2>Performance over time</h2>
                <p>
                  Your interview scores across completed sessions.
                </p>
              </div>

              {improvement !== null && (
                <div
                  className={
                    improvement >= 0
                      ? "dashboard-improvement dashboard-improvement-positive"
                      : "dashboard-improvement dashboard-improvement-negative"
                  }
                >
                  {improvement >= 0 ? "↑" : "↓"}{" "}
                  {Math.abs(improvement).toFixed(0)} points vs previous
                </div>
              )}
            </div>

            <div className="dashboard-chart">
              {performanceInterviews.map((interview, index) => {
                const score = toNumericScore(interview.overall_score) ?? 0;

                return (
                  <div
                    className="dashboard-chart-item"
                    key={interview.id}
                  >
                    <div className="dashboard-chart-value">
                      {score.toFixed(0)}
                    </div>

                    <div className="dashboard-chart-track">
                      <div
                        className="dashboard-chart-bar"
                        style={{
                          height: `${Math.max(
                            0,
                            Math.min(score, 100),
                          )}%`,
                        }}
                      />
                    </div>

                    <div className="dashboard-chart-label">
                      #{index + 1}
                    </div>

                    <div className="dashboard-chart-date">
                      {formatDate(interview.created_at)}
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        )}

        {/* INTERVIEW HISTORY */}
        <section className="dashboard-section">
          <div className="dashboard-section-header">
            <div>
              <div className="dashboard-eyebrow">
                INTERVIEW HISTORY
              </div>

              <h2>Your interviews</h2>

              <p>
                Review every interview in chronological order.
              </p>
            </div>

            <span className="dashboard-count">
              {interviews.length}{" "}
              {interviews.length === 1 ? "interview" : "interviews"}
            </span>
          </div>

          {interviews.length === 0 ? (
            <div className="dashboard-empty">
              <div className="dashboard-empty-icon">+</div>

              <h3>No interviews yet</h3>

              <p>
                Start your first mock interview to begin building
                your performance history.
              </p>

              <button
                className="dashboard-primary-button"
                onClick={() => navigate("/interviews/new")}
              >
                Start Your First Interview
                <span>→</span>
              </button>
            </div>
          ) : (
            <div className="dashboard-interview-list">
              {interviews.map((interview, index) => {
                const topicName =
                  topicMap.get(interview.topic_id) ??
                  `Topic #${interview.topic_id}`;

                const score = toNumericScore(interview.overall_score);

                return (
                  <article
                    className="dashboard-interview-card"
                    key={interview.id}
                  >
                    <div className="dashboard-interview-number">
                      #{interviews.length - index}
                    </div>

                    <div className="dashboard-interview-main">
                      <div className="dashboard-interview-top">
                        <div>
                          <h3>{topicName} Interview</h3>

                          <p>
                            {formatDateTime(interview.created_at)}
                          </p>
                        </div>

                        <span
                          className={getStatusClass(interview.status)}
                        >
                          {getStatusLabel(interview.status)}
                        </span>
                      </div>

                      <div className="dashboard-interview-meta">
                        <div>
                          <span>STARTING</span>
                          <strong>
                            {getDifficultyLabel(
                              interview.starting_difficulty,
                            )}
                          </strong>
                        </div>

                        <div>
                          <span>FINAL</span>
                          <strong>
                            {getDifficultyLabel(
                              interview.current_difficulty,
                            )}
                          </strong>
                        </div>

                        <div>
                          <span>QUESTIONS</span>
                          <strong>{interview.total_questions}</strong>
                        </div>

                        <div>
                          <span>PROGRESS</span>
                          <strong>
                            {interview.current_question_number}/
                            {interview.total_questions}
                          </strong>
                        </div>
                      </div>
                    </div>

                    <div className="dashboard-interview-score">
                      <span>SCORE</span>

                      <strong className={getScoreClass(score)}>
                        {score !== null ? score.toFixed(0) : "—"}
                      </strong>

                      {interview.status === "completed" && (
                        <button
                          className="dashboard-view-button"
                          onClick={() =>
                            handleInterviewClick(interview)
                          }
                        >
                          View Full Report
                          <span>→</span>
                        </button>
                      )}

                      {interview.status === "in_progress" && (
                        <button
                          className="dashboard-view-button"
                          onClick={() =>
                            handleInterviewClick(interview)
                          }
                        >
                          Continue Interview
                          <span>→</span>
                        </button>
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