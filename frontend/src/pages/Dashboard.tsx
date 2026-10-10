import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getInterviews,
  getTopics,
  type Difficulty,
  type Interview,
  type Topic,
} from "../lib/api";

function toNumber(
  value: number | string | null | undefined,
): number | null {
  if (value === null || value === undefined || value === "") {
    return null;
  }

  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function formatScore(
  value: number | string | null | undefined,
): string {
  const score = toNumber(value);
  return score === null ? "—" : score.toFixed(0);
}

function formatDate(dateString: string): string {
  const date = new Date(dateString);

  if (Number.isNaN(date.getTime())) {
    return "Date unavailable";
  }

  return date.toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function formatDateTime(dateString: string): string {
  const date = new Date(dateString);

  if (Number.isNaN(date.getTime())) {
    return "Date unavailable";
  }

  return date.toLocaleString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function capitalize(value: string): string {
  if (!value) return "Unknown";

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

export default function Dashboard() {
  const navigate = useNavigate();

  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadDashboard() {
      try {
        setLoading(true);
        setError(null);

        const [interviewData, topicData] = await Promise.all([
          getInterviews(),
          getTopics(),
        ]);

        if (!isMounted) return;

        const sortedInterviews = [...interviewData].sort(
          (a, b) =>
            new Date(b.created_at).getTime() -
            new Date(a.created_at).getTime(),
        );

        setInterviews(sortedInterviews);
        setTopics(topicData);
      } catch (err) {
        if (!isMounted) return;

        setError(
          err instanceof Error
            ? err.message
            : "Failed to load dashboard.",
        );
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    void loadDashboard();

    return () => {
      isMounted = false;
    };
  }, []);

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

  // Convert API scores to numbers before performing calculations.
  const scoredInterviews = useMemo(
    () =>
      completedInterviews
        .map((interview) => ({
          interview,
          score: toNumber(interview.overall_score),
        }))
        .filter(
          (
            item,
          ): item is {
            interview: Interview;
            score: number;
          } => item.score !== null,
        ),
    [completedInterviews],
  );

  const scores = useMemo(
    () => scoredInterviews.map((item) => item.score),
    [scoredInterviews],
  );

  const averageScore =
    scores.length > 0
      ? scores.reduce((sum, score) => sum + score, 0) /
        scores.length
      : null;

  const bestScore =
    scores.length > 0 ? Math.max(...scores) : null;

  const latestScore =
    scoredInterviews.length > 0
      ? scoredInterviews[0].score
      : null;

  const previousScore =
    scoredInterviews.length > 1
      ? scoredInterviews[1].score
      : null;

  const improvement =
    latestScore !== null && previousScore !== null
      ? latestScore - previousScore
      : null;

  const performanceInterviews = useMemo(
    () => [...scoredInterviews].reverse(),
    [scoredInterviews],
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

  if (error) {
    return (
      <div className="dashboard-page">
        <div className="dashboard-container">
          <div className="dashboard-error">
            <h2>Unable to load dashboard</h2>
            <p>{error}</p>

            <button
              className="dashboard-button"
              onClick={() => window.location.reload()}
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
          </div>

          <button
            className="dashboard-primary-button"
            onClick={() => navigate("/interviews/new")}
          >
            Start New Interview
            <span>→</span>
          </button>
        </header>

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
            <span className="dashboard-stat-label">
              COMPLETED
            </span>

            <strong>{completedInterviews.length}</strong>

            <span className="dashboard-stat-description">
              Successfully completed
            </span>
          </div>

          <div className="dashboard-stat-card">
            <span className="dashboard-stat-label">
              AVERAGE SCORE
            </span>

            <strong>{formatScore(averageScore)}</strong>

            <span className="dashboard-stat-description">
              Across completed interviews
            </span>
          </div>

          <div className="dashboard-stat-card">
            <span className="dashboard-stat-label">
              BEST SCORE
            </span>

            <strong>{formatScore(bestScore)}</strong>

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
                <div className="dashboard-eyebrow">
                  PROGRESS
                </div>

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
                  {formatScore(Math.abs(improvement))} points vs
                  previous
                </div>
              )}
            </div>

            <div className="dashboard-chart">
              {performanceInterviews.map(
                ({ interview, score }, index) => (
                  <div
                    className="dashboard-chart-item"
                    key={interview.id}
                  >
                    <div className="dashboard-chart-value">
                      {formatScore(score)}
                    </div>

                    <div className="dashboard-chart-track">
                      <div
                        className="dashboard-chart-bar"
                        style={{
                          height: `${Math.max(
                            0,
                            Math.min(score, 100),
                          )}%`,
                          minHeight: "5%",
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
                ),
              )}
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
                  topicMap.get(interview.topic_id) ||
                  `Topic #${interview.topic_id}`;

                const score = toNumber(interview.overall_score);

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
                        {formatScore(score)}
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