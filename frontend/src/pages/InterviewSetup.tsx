import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  createInterview,
  getTopics,
  type Difficulty,
  type Topic,
} from "../lib/api";

type QuestionCount = 10 | 15 | 20;

const questionCounts: QuestionCount[] = [10, 15, 20];

const difficulties: {
  value: Difficulty;
  label: string;
  description: string;
}[] = [
  {
    value: "easy",
    label: "Easy",
    description: "Basic concepts and fundamental questions",
  },
  {
    value: "medium",
    label: "Medium",
    description: "Intermediate concepts and practical understanding",
  },
  {
    value: "hard",
    label: "Hard",
    description: "Advanced concepts and challenging problems",
  },
];

function capitalize(value: string): string {
  if (!value) return "Unknown";

  return value.charAt(0).toUpperCase() + value.slice(1);
}

export default function InterviewSetup() {
  const navigate = useNavigate();

  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<number | null>(null);
  const [selectedDifficulty, setSelectedDifficulty] =
    useState<Difficulty>("easy");

  const [questionCount, setQuestionCount] =
    useState<QuestionCount>(15);

  const [isLoading, setIsLoading] = useState(true);
  const [isStarting, setIsStarting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadTopics() {
      try {
        setIsLoading(true);
        setError(null);

        const data = await getTopics();

        if (!isMounted) return;

        setTopics(data);

        if (data.length > 0) {
          setSelectedTopic(data[0].id);
        }
      } catch (err) {
        if (!isMounted) return;

        setError(
          err instanceof Error
            ? err.message
            : "Failed to load topics.",
        );
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    void loadTopics();

    return () => {
      isMounted = false;
    };
  }, []);

  async function handleStartInterview() {
    if (selectedTopic === null) {
      setError("Please select a topic.");
      return;
    }

    try {
      setIsStarting(true);
      setError(null);

      const interview = await createInterview(
        selectedTopic,
        selectedDifficulty,
        questionCount,
      );

      navigate(`/interviews/${interview.id}`);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to start interview.",
      );
    } finally {
      setIsStarting(false);
    }
  }

  if (isLoading) {
    return (
      <div className="app-background flex min-h-screen items-center justify-center px-6">
        <div className="text-center">
          <div
            className="
              mx-auto h-10 w-10 animate-spin rounded-full
              border-2 border-white/10 border-t-violet-400
            "
          />

          <p
            className="
              mt-4 font-mono text-[10px] uppercase
              tracking-[0.18em] text-slate-500
            "
          >
            Loading interview setup
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="app-background min-h-screen">
      <main className="mx-auto w-full max-w-5xl px-6 py-10 sm:px-8 lg:px-10">
        {/* Header */}
        <header className="mb-10">
          <button
            type="button"
            onClick={() => navigate("/home")}
            className="
              mb-8 inline-flex items-center gap-2 text-sm
              text-slate-500 transition-colors hover:text-white
            "
          >
            <span>←</span>
            Back to home
          </button>

          <div
            className="
              font-mono text-[10px] uppercase
              tracking-[0.2em] text-violet-400
            "
          >
            Interview setup
          </div>

          <h1
            className="
              mt-3 font-display text-4xl font-semibold
              tracking-tight text-white sm:text-5xl
            "
          >
            Configure your interview
          </h1>

          <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-400">
            Choose a topic, starting difficulty, and number of
            questions. Your interview will adapt based on your
            performance.
          </p>
        </header>

        {/* Error message */}
        {error && (
          <div
            role="alert"
            className="
              mb-6 rounded-2xl border border-red-400/20
              bg-red-400/5 px-5 py-4 text-sm text-red-300
            "
          >
            {error}
          </div>
        )}

        {/* Topic and difficulty */}
        <div className="grid gap-8 lg:grid-cols-[1.15fr_0.85fr]">
          {/* Step 01: Topics */}
          <section
            className="
              rounded-3xl border border-white/[0.06]
              bg-white/[0.025] p-6 sm:p-8
            "
          >
            <div
              className="
                font-mono text-[10px] uppercase
                tracking-[0.18em] text-slate-500
              "
            >
              Step 01
            </div>

            <h2 className="mt-2 font-display text-2xl font-semibold text-white">
              Choose a topic
            </h2>

            <p className="mt-2 text-sm leading-6 text-slate-500">
              Select the technical topic you want to practice.
            </p>

            {topics.length === 0 ? (
              <div
                className="
                  mt-8 rounded-2xl border border-white/[0.06]
                  bg-black/10 p-6 text-center text-sm text-slate-500
                "
              >
                No active topics are available.
              </div>
            ) : (
              <div className="mt-7 grid gap-3">
                {topics.map((topic) => {
                  const isSelected = selectedTopic === topic.id;

                  return (
                    <button
                      key={topic.id}
                      type="button"
                      aria-pressed={isSelected}
                      onClick={() => setSelectedTopic(topic.id)}
                      className={`
                        w-full rounded-2xl border p-5 text-left
                        transition-all duration-200
                        ${
                          isSelected
                            ? "border-violet-400/40 bg-violet-400/10"
                            : "border-white/[0.06] bg-white/[0.02] hover:border-white/[0.12] hover:bg-white/[0.04]"
                        }
                      `}
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <h3
                            className={`
                              font-display text-lg font-semibold
                              ${
                                isSelected
                                  ? "text-violet-300"
                                  : "text-white"
                              }
                            `}
                          >
                            {topic.name}
                          </h3>

                          {topic.description && (
                            <p className="mt-2 text-sm leading-5 text-slate-500">
                              {topic.description}
                            </p>
                          )}
                        </div>

                        <div
                          className={`
                            mt-1 flex h-5 w-5 shrink-0
                            items-center justify-center rounded-full border
                            ${
                              isSelected
                                ? "border-violet-400 bg-violet-400"
                                : "border-white/20"
                            }
                          `}
                        >
                          {isSelected && (
                            <div className="h-2 w-2 rounded-full bg-slate-950" />
                          )}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </section>

          {/* Step 02: Difficulty */}
          <section
            className="
              rounded-3xl border border-white/[0.06]
              bg-white/[0.025] p-6 sm:p-8
            "
          >
            <div
              className="
                font-mono text-[10px] uppercase
                tracking-[0.18em] text-slate-500
              "
            >
              Step 02
            </div>

            <h2 className="mt-2 font-display text-2xl font-semibold text-white">
              Starting difficulty
            </h2>

            <p className="mt-2 text-sm leading-6 text-slate-500">
              The difficulty will adapt according to your answers.
            </p>

            <div className="mt-7 space-y-3">
              {difficulties.map((difficulty) => {
                const isSelected =
                  selectedDifficulty === difficulty.value;

                return (
                  <button
                    key={difficulty.value}
                    type="button"
                    aria-pressed={isSelected}
                    onClick={() =>
                      setSelectedDifficulty(difficulty.value)
                    }
                    className={`
                      w-full rounded-2xl border p-5 text-left
                      transition-all duration-200
                      ${
                        isSelected
                          ? "border-violet-400/40 bg-violet-400/10"
                          : "border-white/[0.06] bg-white/[0.02] hover:border-white/[0.12] hover:bg-white/[0.04]"
                      }
                    `}
                  >
                    <div className="flex items-center justify-between gap-4">
                      <div>
                        <h3
                          className={`
                            font-display text-lg font-semibold
                            ${
                              isSelected
                                ? "text-violet-300"
                                : "text-white"
                            }
                          `}
                        >
                          {difficulty.label}
                        </h3>

                        <p className="mt-1 text-xs leading-5 text-slate-500">
                          {difficulty.description}
                        </p>
                      </div>

                      <div
                        className={`
                          flex h-5 w-5 shrink-0 items-center
                          justify-center rounded-full border
                          ${
                            isSelected
                              ? "border-violet-400 bg-violet-400"
                              : "border-white/20"
                          }
                        `}
                      >
                        {isSelected && (
                          <div className="h-2 w-2 rounded-full bg-slate-950" />
                        )}
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>

            <div
              className="
                mt-6 rounded-2xl border border-white/[0.06]
                bg-black/10 p-5
              "
            >
              <div
                className="
                  font-mono text-[9px] uppercase
                  tracking-[0.16em] text-slate-600
                "
              >
                Adaptive interview
              </div>

              <p className="mt-2 text-xs leading-5 text-slate-500">
                Strong answers can increase the difficulty, while
                weaker answers can reduce it.
              </p>
            </div>
          </section>
        </div>

        {/* Step 03: Number of questions */}
        <section
          className="
            mt-8 rounded-3xl border border-white/[0.06]
            bg-white/[0.025] p-6 sm:p-8
          "
        >
          <div
            className="
              font-mono text-[10px] uppercase
              tracking-[0.18em] text-slate-500
            "
          >
            Step 03
          </div>

          <h2 className="mt-2 font-display text-2xl font-semibold text-white">
            Number of questions
          </h2>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            Choose how many technical questions you want to answer.
          </p>

          <div className="mt-7 grid grid-cols-1 gap-3 sm:grid-cols-3">
            {questionCounts.map((count) => {
              const isSelected = questionCount === count;

              return (
                <button
                  key={count}
                  type="button"
                  aria-pressed={isSelected}
                  onClick={() => setQuestionCount(count)}
                  className={`
                    rounded-2xl border p-5 text-left
                    transition-all duration-200
                    ${
                      isSelected
                        ? "border-violet-400/40 bg-violet-400/10"
                        : "border-white/[0.06] bg-white/[0.02] hover:border-white/[0.12] hover:bg-white/[0.04]"
                    }
                  `}
                >
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <h3
                        className={`
                          font-display text-xl font-semibold
                          ${
                            isSelected
                              ? "text-violet-300"
                              : "text-white"
                          }
                        `}
                      >
                        {count} Questions
                      </h3>

                      <p className="mt-2 text-xs leading-5 text-slate-500">
                        {count === 10
                          ? "Short practice session"
                          : count === 15
                            ? "Balanced practice session"
                            : "Extended practice session"}
                      </p>
                    </div>

                    <div
                      className={`
                        flex h-5 w-5 shrink-0 items-center
                        justify-center rounded-full border
                        ${
                          isSelected
                            ? "border-violet-400 bg-violet-400"
                            : "border-white/20"
                        }
                      `}
                    >
                      {isSelected && (
                        <div className="h-2 w-2 rounded-full bg-slate-950" />
                      )}
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </section>

        {/* Interview format */}
        <section
          className="
            mt-8 rounded-3xl border border-cyan-400/10
            bg-cyan-400/[0.025] p-6 sm:p-8
          "
        >
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-cyan-400">
            Interview format
          </p>

          <div className="mt-5 grid gap-5 md:grid-cols-3">
            <div>
              <p className="text-sm font-semibold text-white">
                Adaptive difficulty
              </p>
              <p className="mt-1 text-xs leading-5 text-slate-400">
                Questions adapt to your performance throughout
                the interview.
              </p>
            </div>

            <div>
              <p className="text-sm font-semibold text-white">
                AI evaluation
              </p>
              <p className="mt-1 text-xs leading-5 text-slate-400">
                Your answers are evaluated for technical accuracy,
                relevance, and communication.
              </p>
            </div>

            <div>
              <p className="text-sm font-semibold text-white">
                Detailed final report
              </p>
              <p className="mt-1 text-xs leading-5 text-slate-400">
                Receive strengths, weaknesses, assessments, and
                recommendations after completion.
              </p>
            </div>
          </div>
        </section>

        {/* Start interview */}
        <section
          className="
            mt-8 rounded-3xl border border-white/[0.06]
            bg-white/[0.025] p-6 sm:p-8
          "
        >
          <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div
                className="
                  font-mono text-[10px] uppercase
                  tracking-[0.18em] text-slate-500
                "
              >
                Ready?
              </div>

              <h2 className="mt-2 font-display text-2xl font-semibold text-white">
                Start your mock interview
              </h2>

              <p className="mt-2 text-sm text-slate-500">
                {topics.find((topic) => topic.id === selectedTopic)?.name ??
                  "Choose a topic"}
                {" · "}
                {capitalize(selectedDifficulty)}
                {" · "}
                {questionCount} questions
              </p>
            </div>

            <button
              type="button"
              onClick={handleStartInterview}
              disabled={
                selectedTopic === null ||
                isStarting ||
                topics.length === 0
              }
              className="
                group inline-flex min-w-[210px] items-center
                justify-center gap-3 rounded-2xl bg-white
                px-6 py-4 font-display text-sm font-semibold
                text-slate-950 transition-all duration-200
                hover:-translate-y-0.5
                hover:shadow-[0_15px_45px_rgba(139,92,246,0.25)]
                disabled:cursor-not-allowed disabled:opacity-40
                disabled:hover:translate-y-0
              "
            >
              {isStarting ? "Starting..." : "Start Interview"}

              {!isStarting && (
                <span className="transition-transform duration-200 group-hover:translate-x-1">
                  →
                </span>
              )}
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}