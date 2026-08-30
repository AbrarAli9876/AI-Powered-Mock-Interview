import { useEffect, useState } from "react";
import {
  useNavigate,
  useParams,
} from "react-router-dom";

import {
  getInterviewResult,
  getTopics,
  type InterviewResult,
  type Topic,
} from "../lib/api";


function formatDateTime(
  dateString: string,
): string {
  return new Date(dateString).toLocaleString(
    undefined,
    {
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
    },
  );
}


function capitalize(
  value: string,
): string {
  return (
    value.charAt(0).toUpperCase() +
    value.slice(1)
  );
}


function ScoreCard({
  label,
  score,
}: {
  label: string;
  score: number | null;
}) {
  return (
    <div className="result-score-card">
      <span>
        {label}
      </span>

      <strong>
        {score !== null
          ? score.toFixed(0)
          : "—"}
      </strong>

      <small>
        / 100
      </small>
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
  content: string | null;
}) {
  return (
    <section className="result-report-section">

      <div className="result-eyebrow">
        {label}
      </div>

      <h2>
        {title}
      </h2>

      <p>
        {content ||
          "No information was generated for this section."}
      </p>

    </section>
  );
}


export default function InterviewResult() {
  const navigate = useNavigate();

  const { sessionId } =
    useParams<{
      sessionId: string;
    }>();

  const [result, setResult] =
    useState<InterviewResult | null>(
      null,
    );

  const [topics, setTopics] =
    useState<Topic[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {
    async function loadResult() {
      if (!sessionId) {
        setError(
          "Interview session was not found.",
        );

        setLoading(false);

        return;
      }

      try {
        setLoading(true);
        setError(null);

        const [
          interviewResult,
          topicData,
        ] = await Promise.all([
          getInterviewResult(
            Number(sessionId),
          ),
          getTopics(),
        ]);

        setResult(interviewResult);
        setTopics(topicData);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load interview result.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadResult();
  }, [sessionId]);


  const topic = topics.find(
    (item) =>
      item.id === result?.topic_id,
  );


  if (loading) {
    return (
      <div className="result-page">
        <div className="result-container">
          <div className="result-loading">
            Loading your interview report...
          </div>
        </div>
      </div>
    );
  }


  if (error || !result) {
    return (
      <div className="result-page">
        <div className="result-container">

          <div className="result-error">

            <h1>
              Unable to load report
            </h1>

            <p>
              {error ||
                "Interview result was not found."}
            </p>

            <button
              className="result-button"
              onClick={() =>
                navigate("/dashboard")
              }
            >
              Back to Dashboard
            </button>

          </div>

        </div>
      </div>
    );
  }


  return (
    <div className="result-page">

      <div className="result-container">

        {/* =================================================
            HEADER
        ================================================== */}

        <header className="result-header">

          <button
            className="result-back-button"
            onClick={() =>
              navigate("/dashboard")
            }
          >
            ← Back to Dashboard
          </button>

          <div className="result-eyebrow">
            INTERVIEW REPORT
          </div>

          <div className="result-header-row">

            <div>
              <h1>
                {topic?.name ||
                  `Topic #${result.topic_id}`}
              </h1>

              <p>
                Interview completed on{" "}
                {formatDateTime(
                  result.created_at,
                )}
              </p>
            </div>

            <div className="result-final-score">

              <span>
                FINAL SCORE
              </span>

              <strong>
                {result.overall_score !==
                null
                  ? result.overall_score.toFixed(
                      0,
                    )
                  : "—"}
              </strong>

              <small>
                / 100
              </small>

            </div>

          </div>

        </header>


        {/* =================================================
            INTERVIEW INFORMATION
        ================================================== */}

        <section className="result-info-grid">

          <div className="result-info-card">
            <span>
              STATUS
            </span>

            <strong>
              {capitalize(
                result.status.replace(
                  "_",
                  " ",
                ),
              )}
            </strong>
          </div>


          <div className="result-info-card">
            <span>
              QUESTIONS
            </span>

            <strong>
              {result.answers.length}
            </strong>
          </div>


          <div className="result-info-card">
            <span>
              STARTING DIFFICULTY
            </span>

            <strong>
              {capitalize(
                result.starting_difficulty,
              )}
            </strong>
          </div>


          <div className="result-info-card">
            <span>
              FINAL DIFFICULTY
            </span>

            <strong>
              {capitalize(
                result.final_difficulty,
              )}
            </strong>
          </div>

        </section>


        {/* =================================================
            DIFFICULTY PROGRESSION
        ================================================== */}

        {result.difficulty_progression
          .length > 0 && (
          <section className="result-progression">

            <div>
              <div className="result-eyebrow">
                ADAPTIVE INTERVIEW
              </div>

              <h2>
                Difficulty progression
              </h2>

              <p>
                Your difficulty changed based
                on your interview performance.
              </p>
            </div>


            <div className="result-progression-list">

              {result.difficulty_progression.map(
                (
                  difficulty,
                  index,
                ) => (
                  <div
                    className="result-progression-item"
                    key={`${difficulty}-${index}`}
                  >
                    <span>
                      {index + 1}
                    </span>

                    <strong>
                      {capitalize(
                        difficulty,
                      )}
                    </strong>

                    {index <
                      result
                        .difficulty_progression
                        .length -
                        1 && (
                      <b>
                        →
                      </b>
                    )}
                  </div>
                ),
              )}

            </div>

          </section>
        )}


        {/* =================================================
            SCORE BREAKDOWN
        ================================================== */}

        <section className="result-section">

          <div className="result-eyebrow">
            PERFORMANCE
          </div>

          <h2>
            Score breakdown
          </h2>

          <p className="result-section-description">
            Your performance was evaluated
            across multiple criteria.
          </p>


          <div className="result-score-grid">

            {(() => {
              const technicalScores =
                result.answers
                  .map(
                    (answer) =>
                      answer.technical_score,
                  )
                  .filter(
                    (
                      score,
                    ): score is number =>
                      score !== null,
                  );

              const communicationScores =
                result.answers
                  .map(
                    (answer) =>
                      answer.communication_score,
                  )
                  .filter(
                    (
                      score,
                    ): score is number =>
                      score !== null,
                  );

              const relevanceScores =
                result.answers
                  .map(
                    (answer) =>
                      answer.relevance_score,
                  )
                  .filter(
                    (
                      score,
                    ): score is number =>
                      score !== null,
                  );


              const average = (
                scores: number[],
              ): number | null => {
                if (
                  scores.length ===
                  0
                ) {
                  return null;
                }

                return (
                  scores.reduce(
                    (
                      sum,
                      score,
                    ) =>
                      sum + score,
                    0,
                  ) /
                  scores.length
                );
              };


              return (
                <>
                  <ScoreCard
                    label="Overall"
                    score={
                      result.overall_score
                    }
                  />

                  <ScoreCard
                    label="Technical"
                    score={average(
                      technicalScores,
                    )}
                  />

                  <ScoreCard
                    label="Communication"
                    score={average(
                      communicationScores,
                    )}
                  />

                  <ScoreCard
                    label="Relevance"
                    score={average(
                      relevanceScores,
                    )}
                  />
                </>
              );
            })()}

          </div>

        </section>


        {/* =================================================
            PERSONALIZED AI REPORT
        ================================================== */}

        <section className="result-ai-report">

          <div className="result-ai-heading">

            <div>
              <div className="result-eyebrow">
                AI FINAL ASSESSMENT
              </div>

              <h2>
                Your personalized feedback
              </h2>

              <p>
                This assessment is based on
                your actual answers and
                performance throughout the
                interview.
              </p>
            </div>

          </div>


          <div className="result-report-grid">

            <ReportSection
              label="SUMMARY"
              title="Overall assessment"
              content={
                result.final_summary
              }
            />


            <ReportSection
              label="STRENGTHS"
              title="What you did well"
              content={
                result.final_strengths
              }
            />


            <ReportSection
              label="WEAKNESSES"
              title="Areas to improve"
              content={
                result.final_weaknesses
              }
            />


            <ReportSection
              label="TECHNICAL"
              title="Technical assessment"
              content={
                result.technical_assessment
              }
            />


            <ReportSection
              label="COMMUNICATION"
              title="Communication assessment"
              content={
                result.communication_assessment
              }
            />


            <ReportSection
              label="PROBLEM SOLVING"
              title="Problem-solving assessment"
              content={
                result.problem_solving_assessment
              }
            />

          </div>


          <div className="result-recommendations">

            <div className="result-eyebrow">
              RECOMMENDATIONS
            </div>

            <h2>
              What you should work on next
            </h2>

            <p>
              {result.final_recommendations ||
                "No recommendations were generated."}
            </p>

          </div>

        </section>


        {/* =================================================
            QUESTION BY QUESTION REVIEW
        ================================================== */}

        <section className="result-section">

          <div className="result-eyebrow">
            DETAILED REVIEW
          </div>

          <h2>
            Question-by-question performance
          </h2>

          <p className="result-section-description">
            Review exactly how you performed
            on each question.
          </p>


          <div className="result-question-list">

            {result.answers.map(
              (
                answer,
                index,
              ) => (
                <article
                  className="result-question-card"
                  key={answer.question_id}
                >

                  <div className="result-question-header">

                    <div>
                      <span>
                        QUESTION{" "}
                        {index + 1}
                      </span>

                      <h3>
                        {answer.question_text}
                      </h3>
                    </div>

                    <div className="result-question-score">

                      <small>
                        SCORE
                      </small>

                      <strong>
                        {answer.overall_score !==
                        null
                          ? answer.overall_score.toFixed(
                              0,
                            )
                          : "—"}
                      </strong>

                    </div>

                  </div>


                  <div className="result-question-difficulty">
                    {capitalize(
                      answer.difficulty,
                    )}
                  </div>


                  <div className="result-answer-block">

                    <span>
                      YOUR ANSWER
                    </span>

                    <p>
                      {answer.answer_text ||
                        "No answer provided."}
                    </p>

                  </div>


                  <div className="result-question-scores">

                    <div>
                      <span>
                        Technical
                      </span>

                      <strong>
                        {answer.technical_score !==
                        null
                          ? answer.technical_score.toFixed(
                              0,
                            )
                          : "—"}
                      </strong>
                    </div>


                    <div>
                      <span>
                        Communication
                      </span>

                      <strong>
                        {answer.communication_score !==
                        null
                          ? answer.communication_score.toFixed(
                              0,
                            )
                          : "—"}
                      </strong>
                    </div>


                    <div>
                      <span>
                        Relevance
                      </span>

                      <strong>
                        {answer.relevance_score !==
                        null
                          ? answer.relevance_score.toFixed(
                              0,
                            )
                          : "—"}
                      </strong>
                    </div>

                  </div>


                  <div className="result-feedback-grid">

                    <div>
                      <span>
                        FEEDBACK
                      </span>

                      <p>
                        {answer.feedback ||
                          "No feedback available."}
                      </p>
                    </div>


                    <div>
                      <span>
                        STRENGTHS
                      </span>

                      <p>
                        {answer.strengths ||
                          "No strengths recorded."}
                      </p>
                    </div>


                    <div>
                      <span>
                        IMPROVEMENTS
                      </span>

                      <p>
                        {answer.improvements ||
                          "No improvements recorded."}
                      </p>
                    </div>

                  </div>

                </article>
              ),
            )}

          </div>

        </section>


        {/* =================================================
            FOOTER ACTION
        ================================================== */}

        <div className="result-footer-action">

          <button
            className="result-button"
            onClick={() =>
              navigate("/dashboard")
            }
          >
            ← Back to Performance Dashboard
          </button>

          <button
            className="result-primary-button"
            onClick={() =>
              navigate("/interviews/new")
            }
          >
            Start Another Interview →
          </button>

        </div>

      </div>
    </div>
  );
}