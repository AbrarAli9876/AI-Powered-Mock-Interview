import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { invalidateTechnicalInterviewCache } from "../lib/dataCache";
import {
  getInterviewResult,
  getTopics,
  type InterviewResult,
  type Topic,
} from "../lib/api";

function formatDateTime(dateString: string): string {
  if (!dateString) {
    return "Date unavailable";
  }

  // If the backend returns a timestamp without a timezone,
  // interpret it as UTC. This assumes naive backend timestamps
  // are stored in UTC.
  const hasTimezone = /(?:Z|[+-]\d{2}:\d{2})$/i.test(dateString);

  const normalizedDate = hasTimezone
    ? dateString
    : `${dateString}Z`;

  const date = new Date(normalizedDate);

  if (Number.isNaN(date.getTime())) {
    return "Date unavailable";
  }

  return date.toLocaleString(undefined, {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function capitalize(value: string | null | undefined): string {
  if (!value) return "Unknown";

  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

/**
 * API responses may contain numeric values as strings.
 * Always convert and validate before formatting.
 */
function formatScore(
  value: number | string | null | undefined,
): string {
  if (value === null || value === undefined || value === "") {
    return "—";
  }

  const numericValue = Number(value);

  return Number.isFinite(numericValue)
    ? numericValue.toFixed(0)
    : "—";
}

function toScore(
  value: number | string | null | undefined,
): number | null {
  if (value === null || value === undefined || value === "") {
    return null;
  }

  const numericValue = Number(value);

  return Number.isFinite(numericValue) ? numericValue : null;
}

function average(
  values: Array<number | string | null | undefined>,
): number | null {
  const validValues = values
    .map(toScore)
    .filter((value): value is number => value !== null);

  if (validValues.length === 0) {
    return null;
  }

  return (
    validValues.reduce((sum, value) => sum + value, 0) /
    validValues.length
  );
}

function ScoreCard({
  label,
  score,
}: {
  label: string;
  score: number | string | null | undefined;
}) {
  return (
    <div className="result-score-card">
      <span>{label}</span>
      <strong>{formatScore(score)}</strong>
      <small>/ 100</small>
    </div>
  );
}

function ReportSection({
  label,
  title,
  content,
}: {
  label: string;
  title: string;
  content: string | null | undefined;
}) {
  return (
    <section className="result-report-section">
      <div className="result-eyebrow">{label}</div>
      <h2>{title}</h2>
      <p>{content?.trim() || "No information was generated for this section."}</p>
    </section>
  );
}

const REPORT_RETRY_COUNT = 3;
const REPORT_RETRY_DELAY = 2000;

export default function InterviewResult() {
  const navigate = useNavigate();
  const { sessionId } = useParams<{ sessionId: string }>();

  const [result, setResult] = useState<InterviewResult | null>(null);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [retrying, setRetrying] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    sessionStorage.removeItem("technicalInterviewViewingResults");
    invalidateTechnicalInterviewCache();
    let cancelled = false;
    let retryTimer: ReturnType<typeof setTimeout> | undefined;

    const wait = () =>
      new Promise<void>((resolve) => {
        retryTimer = setTimeout(resolve, REPORT_RETRY_DELAY);
      });

    async function loadPage() {
      setLoading(true);
      setError(null);

      if (!sessionId || !/^\d+$/.test(sessionId)) {
        setError("The interview session ID is invalid.");
        setLoading(false);
        return;
      }

      const numericSessionId = Number(sessionId);

      if (!Number.isSafeInteger(numericSessionId) || numericSessionId <= 0) {
        setError("The interview session ID is invalid.");
        setLoading(false);
        return;
      }

      // Topics are supplementary. A topic endpoint failure should not
      // prevent a valid interview result from being displayed.
      try {
        const topicData = await getTopics();

        if (!cancelled) {
          setTopics(Array.isArray(topicData) ? topicData : []);
        }
      } catch (topicError) {
        console.error("Unable to load interview topics:", topicError);
      }

      let lastError: unknown = null;

      for (let attempt = 0; attempt <= REPORT_RETRY_COUNT; attempt += 1) {
        if (cancelled) return;

        try {
          const data = await getInterviewResult(numericSessionId);

          if (cancelled) return;

          if (!data || typeof data !== "object") {
            throw new Error("The server returned an invalid interview result.");
          }

          setResult(data);
          setError(null);

          const reportReady = Boolean(
            data.final_summary ||
              data.final_strengths ||
              data.final_weaknesses ||
              data.technical_assessment ||
              data.communication_assessment ||
              data.problem_solving_assessment ||
              data.final_recommendations,
          );

          // Show the result even if report generation is still pending.
          if (data.status !== "completed" || reportReady) {
            setRetrying(false);
            setLoading(false);
            return;
          }

          if (attempt < REPORT_RETRY_COUNT) {
            setRetrying(true);
            await wait();
            continue;
          }

          setRetrying(false);
          setLoading(false);
          return;
        } catch (requestError) {
          lastError = requestError;

          if (cancelled) return;

          // A 404 usually means the URL or backend route/resource is wrong.
          // Repeating the same 404 request will not fix it.
          const message =
            requestError instanceof Error
              ? requestError.message
              : String(requestError);

          if (
            /\b404\b|not found/i.test(message) ||
            attempt === REPORT_RETRY_COUNT
          ) {
            break;
          }

          setRetrying(true);
          await wait();
        }
      }

      if (cancelled) return;

      setRetrying(false);
      setLoading(false);

      setError(
        lastError instanceof Error
          ? lastError.message
          : "Unable to load the interview result. Check the backend API.",
      );
    }

    void loadPage();

    return () => {
      cancelled = true;

      if (retryTimer) {
        clearTimeout(retryTimer);
      }
    };
  }, [sessionId]);

  const topic = topics.find((item) => item.id === result?.topic_id);

  if (loading) {
    return (
      <div className="result-page">
        <div className="result-container">
          <div className="result-loading">
            {retrying
              ? "Retrying your interview report..."
              : "Loading your interview report..."}
          </div>
        </div>
      </div>
    );
  }

  if (error && !result) {
    return (
      <div className="result-page">
        <div className="result-container">
          <div className="result-error">
            <h1>Unable to load interview result</h1>
            <p>{error}</p>
            <p>
              Check the browser Network tab and backend logs to find why the
              interview result endpoint returned an error.
            </p>
            <button
              className="result-button"
              onClick={() => navigate("/dashboard")}
            >
              Back to Dashboard
            </button>
            <button
              className="result-primary-button"
              onClick={() => window.location.reload()}
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="result-page">
        <div className="result-container">
          <div className="result-error">
            <h1>Interview result unavailable</h1>
            <p>The server did not return an interview result.</p>
            <button
              className="result-button"
              onClick={() => navigate("/dashboard")}
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  const answers = Array.isArray(result.answers) ? result.answers : [];

  const technicalAverage = average(
    answers.map((answer) => answer.technical_score),
  );

  const communicationAverage = average(
    answers.map((answer) => answer.communication_score),
  );

  const relevanceAverage = average(
    answers.map((answer) => answer.relevance_score),
  );

  const progression = Array.isArray(result.difficulty_progression)
    ? result.difficulty_progression
    : [];

  const reportReady = Boolean(
    result.final_summary ||
      result.final_strengths ||
      result.final_weaknesses ||
      result.technical_assessment ||
      result.communication_assessment ||
      result.problem_solving_assessment ||
      result.final_recommendations,
  );

  return (
    <div className="result-page">
      <div className="result-container">
        <header className="result-header">
          <button
            className="result-back-button"
            onClick={() => navigate("/dashboard")}
          >
            ← Back to Dashboard
          </button>

          <div className="result-eyebrow">INTERVIEW REPORT</div>

          <div className="result-header-row">
            <div>
              <h1>{topic?.name || `Topic #${result.topic_id}`}</h1>
              <p>
                Interview started on {formatDateTime(result.created_at)}
              </p>
            </div>

            <div className="result-final-score">
              <span>FINAL SCORE</span>
              <strong>{formatScore(result.overall_score)}</strong>
              <small>/ 100</small>
            </div>
          </div>
        </header>

        {error && (
          <div className="result-error">
            <p>{error}</p>
          </div>
        )}

        {result.status === "completed" && !reportReady && (
          <div className="result-loading">
            The interview is complete, but the detailed AI report is not
            available yet. Your saved score and answer review are shown below.
            {retrying && <p>Checking for the final report...</p>}
          </div>
        )}

        <section className="result-info-grid">
          <div className="result-info-card">
            <span>STATUS</span>
            <strong>{capitalize(result.status)}</strong>
          </div>

          <div className="result-info-card">
            <span>QUESTIONS ANSWERED</span>
            <strong>{answers.length}</strong>
          </div>

          <div className="result-info-card">
            <span>STARTING DIFFICULTY</span>
            <strong>{capitalize(result.starting_difficulty)}</strong>
          </div>

          <div className="result-info-card">
            <span>FINAL DIFFICULTY</span>
            <strong>{capitalize(result.final_difficulty)}</strong>
          </div>
        </section>

        {progression.length > 0 && (
          <section className="result-progression">
            <div>
              <div className="result-eyebrow">ADAPTIVE INTERVIEW</div>
              <h2>Difficulty progression</h2>
              <p>Your difficulty changed based on your interview performance.</p>
            </div>

            <div className="result-progression-list">
              {progression.map((difficulty, index) => (
                <div
                  className="result-progression-item"
                  key={`${difficulty}-${index}`}
                >
                  <span>{index + 1}</span>
                  <strong>{capitalize(difficulty)}</strong>
                  {index < progression.length - 1 && <b>→</b>}
                </div>
              ))}
            </div>
          </section>
        )}

        <section className="result-section">
          <div className="result-eyebrow">PERFORMANCE</div>
          <h2>Score breakdown</h2>
          <p className="result-section-description">
            Your performance was evaluated across multiple criteria.
          </p>

          <div className="result-score-grid">
            <ScoreCard label="Overall" score={result.overall_score} />
            <ScoreCard label="Technical" score={technicalAverage} />
            <ScoreCard label="Communication" score={communicationAverage} />
            <ScoreCard label="Relevance" score={relevanceAverage} />
          </div>
        </section>

        <section className="result-ai-report">
          <div className="result-ai-heading">
            <div>
              <div className="result-eyebrow">AI FINAL ASSESSMENT</div>
              <h2>Your personalized feedback</h2>
              <p>
                This assessment is based on your answers and performance
                throughout the interview.
              </p>
            </div>
          </div>

          <div className="result-report-grid">
            <ReportSection
              label="SUMMARY"
              title="Overall assessment"
              content={result.final_summary}
            />

            <ReportSection
              label="STRENGTHS"
              title="What you did well"
              content={result.final_strengths}
            />

            <ReportSection
              label="WEAKNESSES"
              title="Areas to improve"
              content={result.final_weaknesses}
            />

            <ReportSection
              label="TECHNICAL"
              title="Technical assessment"
              content={result.technical_assessment}
            />

            <ReportSection
              label="COMMUNICATION"
              title="Communication assessment"
              content={result.communication_assessment}
            />

            <ReportSection
              label="PROBLEM SOLVING"
              title="Problem-solving assessment"
              content={result.problem_solving_assessment}
            />
          </div>

          <div className="result-recommendations">
            <div className="result-eyebrow">RECOMMENDATIONS</div>
            <h2>What you should work on next</h2>
            <p>
              {result.final_recommendations ||
                "No recommendations were generated yet."}
            </p>
          </div>
        </section>

        <section className="result-section">
          <div className="result-eyebrow">DETAILED REVIEW</div>
          <h2>Question-by-question performance</h2>
          <p className="result-section-description">
            Review your answer, score, feedback, strengths, and improvements
            for each question.
          </p>

          {answers.length === 0 ? (
            <p>No answer records were returned for this interview.</p>
          ) : (
            <div className="result-question-list">
              {answers.map((answer, index) => (
                <article
                  className="result-question-card"
                  key={`${answer.question_id}-${index}`}
                >
                  <div className="result-question-header">
                    <div>
                      <span>QUESTION {index + 1}</span>
                      <h3>{answer.question_text}</h3>
                    </div>

                    <div className="result-question-score">
                      <small>SCORE</small>
                      <strong>{formatScore(answer.overall_score)}</strong>
                    </div>
                  </div>

                  <div className="result-question-difficulty">
                    {capitalize(answer.difficulty)}
                  </div>

                  <div className="result-answer-block">
                    <span>YOUR ANSWER</span>
                    <p>{answer.answer_text || "No answer provided."}</p>
                  </div>

                  <div className="result-question-scores">
                    <div>
                      <span>Technical</span>
                      <strong>{formatScore(answer.technical_score)}</strong>
                    </div>

                    <div>
                      <span>Communication</span>
                      <strong>{formatScore(answer.communication_score)}</strong>
                    </div>

                    <div>
                      <span>Relevance</span>
                      <strong>{formatScore(answer.relevance_score)}</strong>
                    </div>
                  </div>

                  <div className="result-feedback-grid">
                    <div>
                      <span>FEEDBACK</span>
                      <p>{answer.feedback || "No feedback available."}</p>
                    </div>

                    <div>
                      <span>STRENGTHS</span>
                      <p>{answer.strengths || "No strengths recorded."}</p>
                    </div>

                    <div>
                      <span>IMPROVEMENTS</span>
                      <p>{answer.improvements || "No improvements recorded."}</p>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        <div className="result-footer-action">
          <button
            className="result-button"
            onClick={() => navigate("/dashboard")}
          >
            ← Back to Performance Dashboard
          </button>

          <button
            className="result-primary-button"
            onClick={() => navigate("/interviews/new")}
          >
            Start Another Interview →
          </button>
        </div>
      </div>
    </div>
  );
}