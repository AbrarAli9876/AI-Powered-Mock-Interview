import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getTopics,
  type Difficulty,
  type Topic,
} from "../lib/api";

type QuestionCount = 10 | 15 | 20;

const questionCounts: {
  value: QuestionCount;
  description: string;
}[] = [
  {
    value: 10,
    description: "Short practice session",
  },
  {
    value: 15,
    description: "Balanced practice session",
  },
  {
    value: 20,
    description: "Extended practice session",
  },
];

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
  const [selectedTopic, setSelectedTopic] = useState<number | null>(
    null,
  );

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
        setSelectedTopic(data.length > 0 ? data[0].id : null);
      } catch (err) {
        if (!isMounted) return;

        setError(
          err instanceof Error
            ? err.message
            : "Failed to load interview topics.",
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
      setError("Please select a technical topic.");
      return;
    }

    try {
      setIsStarting(true);
      setError(null);

      const setup = {
        topicId: selectedTopic,
        startingDifficulty: selectedDifficulty,
        questionCount,
      };

      sessionStorage.setItem(
        "technicalInterviewSetup",
        JSON.stringify(setup),
      );

      sessionStorage.removeItem(
        "technicalInterviewPreflightVerified",
      );

      sessionStorage.setItem(
        "technicalInterviewPreflightStage",
        "fullscreen",
      );

      navigate("/interviews/preflight/fullscreen", {
        state: { setup },
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to open interview security checks.",
      );
    } finally {
      setIsStarting(false);
    }
  }

  if (isLoading) {
    return (
      <div className="app-background flex min-h-screen items-center justify-center px-6">
        <div className="text-center">
          <div className="mx-auto h-10 w-10 animate-spin rounded-full border-2 border-white/10 border-t-violet-400" />

          <p className="mt-4 font-mono text-xs uppercase tracking-[0.2em] text-slate-500">
            Loading interview setup
          </p>
        </div>
      </div>
    );
  }

  const selectedTopicName =
    topics.find((topic) => topic.id === selectedTopic)?.name ??
    "Choose a topic";

  return (
    <div className="app-background min-h-screen">
      <div className="app-grid" />

      <main className="relative z-10 mx-auto w-full max-w-6xl px-6 py-10 sm:px-8 lg:px-10">
        {/* PAGE NAVIGATION */}
        <button
          type="button"
          onClick={() => navigate("/home")}
          className="mb-8 inline-flex items-center gap-2 text-sm text-slate-400 transition hover:text-white"
        >
          <span aria-hidden="true">←</span>
          Back to home
        </button>

        {/* PAGE HEADER */}
        <header className="mb-10">
          <p className="mb-3 font-mono text-xs uppercase tracking-[0.3em] text-violet-400">
            Technical Interview
          </p>

          <h1 className="text-4xl font-semibold tracking-tight text-white md:text-5xl">
            Configure your interview
          </h1>

          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-400">
            Choose a technical topic, starting difficulty, and
            number of questions before starting your interview.
          </p>
        </header>

        {/* ERROR MESSAGE */}
        {error && (
          <div
            role="alert"
            className="mb-6 rounded-xl border border-rose-500/30 bg-rose-500/10 px-5 py-4 text-sm text-rose-300"
          >
            {error}
          </div>
        )}

        <div className="space-y-6">
          {/* STEP 01: TOPIC */}
          <section className="glass-panel rounded-2xl p-6 sm:p-7">
            <div className="mb-6">
              <p className="font-mono text-xs uppercase tracking-[0.25em] text-slate-500">
                Step 01
              </p>

              <h2 className="mt-2 text-2xl font-semibold text-white">
                Choose a topic
              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                Select the technical topic you want to practice.
              </p>
            </div>

            {topics.length === 0 ? (
              <div className="rounded-xl border border-white/10 bg-white/[0.02] p-6 text-sm text-slate-400">
                No active topics are available. Please check your
                backend topic configuration.
              </div>
            ) : (
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {topics.map((topic) => {
                  const selected = selectedTopic === topic.id;

                  return (
                    <button
                      key={topic.id}
                      type="button"
                      aria-pressed={selected}
                      disabled={isStarting}
                      onClick={() => setSelectedTopic(topic.id)}
                      className={`flex min-h-[88px] items-center justify-between gap-4 rounded-xl border p-6 text-left transition-all duration-200 ${
                        selected
                          ? "border-violet-400/50 bg-violet-400/10"
                          : "border-white/10 bg-white/[0.02] hover:border-white/20 hover:bg-white/[0.04]"
                      } disabled:cursor-not-allowed disabled:opacity-60`}
                    >
                      <h3
                        className={`text-lg font-semibold ${
                          selected
                            ? "text-violet-300"
                            : "text-white"
                        }`}
                      >
                        {topic.name}
                      </h3>

                      <span
                        className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border ${
                          selected
                            ? "border-violet-400 bg-violet-400"
                            : "border-white/20"
                        }`}
                      >
                        {selected && (
                          <span className="h-2 w-2 rounded-full bg-slate-950" />
                        )}
                      </span>
                    </button>
                  );
                })}
              </div>
            )}
          </section>

          {/* STEP 02: DIFFICULTY */}
          <section className="glass-panel rounded-2xl p-6 sm:p-7">
            <div className="mb-6">
              <p className="font-mono text-xs uppercase tracking-[0.25em] text-slate-500">
                Step 02
              </p>

              <h2 className="mt-2 text-2xl font-semibold text-white">
                Starting difficulty
              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                Select the difficulty level at which your interview
                will begin.
              </p>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              {difficulties.map((difficulty) => {
                const selected =
                  selectedDifficulty === difficulty.value;

                return (
                  <button
                    key={difficulty.value}
                    type="button"
                    aria-pressed={selected}
                    disabled={isStarting}
                    onClick={() =>
                      setSelectedDifficulty(difficulty.value)
                    }
                    className={`rounded-xl border p-5 text-left transition-all duration-200 ${
                      selected
                        ? "border-violet-400/50 bg-violet-400/10"
                        : "border-white/10 bg-white/[0.02] hover:border-white/20 hover:bg-white/[0.04]"
                    } disabled:cursor-not-allowed disabled:opacity-60`}
                  >
                    <div className="flex items-center justify-between gap-3">
                      <h3
                        className={`text-lg font-semibold ${
                          selected
                            ? "text-violet-300"
                            : "text-white"
                        }`}
                      >
                        {difficulty.label}
                      </h3>

                      <span
                        className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border ${
                          selected
                            ? "border-violet-400 bg-violet-400"
                            : "border-white/20"
                        }`}
                      >
                        {selected && (
                          <span className="h-2 w-2 rounded-full bg-slate-950" />
                        )}
                      </span>
                    </div>

                    <p className="mt-2 text-sm leading-6 text-slate-400">
                      {difficulty.description}
                    </p>
                  </button>
                );
              })}
            </div>

            <div className="mt-5 rounded-xl border border-white/10 bg-black/10 p-5">
              <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-slate-500">
                Adaptive interview
              </p>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                Questions can become more difficult when you perform
                well and easier when you need more support.
              </p>
            </div>
          </section>

          {/* STEP 03: QUESTION COUNT */}
          <section className="glass-panel rounded-2xl p-6 sm:p-7">
            <div className="mb-6">
              <p className="font-mono text-xs uppercase tracking-[0.25em] text-slate-500">
                Step 03
              </p>

              <h2 className="mt-2 text-2xl font-semibold text-white">
                Number of questions
              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                Choose how many technical questions you want to
                answer.
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-3">
              {questionCounts.map((item) => {
                const selected = questionCount === item.value;

                return (
                  <button
                    key={item.value}
                    type="button"
                    aria-pressed={selected}
                    disabled={isStarting}
                    onClick={() => setQuestionCount(item.value)}
                    className={`rounded-xl border p-5 text-left transition-all duration-200 ${
                      selected
                        ? "border-violet-400/50 bg-violet-400/10"
                        : "border-white/10 bg-white/[0.02] hover:border-white/20 hover:bg-white/[0.04]"
                    } disabled:cursor-not-allowed disabled:opacity-60`}
                  >
                    <div className="flex items-center justify-between gap-3">
                      <h3
                        className={`text-lg font-semibold ${
                          selected
                            ? "text-violet-300"
                            : "text-white"
                        }`}
                      >
                        {item.value} Questions
                      </h3>

                      <span
                        className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border ${
                          selected
                            ? "border-violet-400 bg-violet-400"
                            : "border-white/20"
                        }`}
                      >
                        {selected && (
                          <span className="h-2 w-2 rounded-full bg-slate-950" />
                        )}
                      </span>
                    </div>

                    <p className="mt-2 text-xs leading-5 text-slate-400">
                      {item.description}
                    </p>
                  </button>
                );
              })}
            </div>
          </section>

          {/* INTERVIEW FORMAT */}
          <section className="rounded-2xl border border-cyan-400/10 bg-cyan-400/[0.03] p-6 sm:p-7">
            <p className="font-mono text-xs uppercase tracking-[0.25em] text-cyan-400">
              Interview Format
            </p>

            <div className="mt-5 grid gap-6 md:grid-cols-3">
              <div>
                <p className="text-sm font-semibold text-white">
                  Adaptive difficulty
                </p>

                <p className="mt-2 text-xs leading-5 text-slate-400">
                  Questions adapt to your performance throughout
                  the interview.
                </p>
              </div>

              <div>
                <p className="text-sm font-semibold text-white">
                  AI evaluation
                </p>

                <p className="mt-2 text-xs leading-5 text-slate-400">
                  Your answers are evaluated for technical accuracy,
                  relevance, and communication.
                </p>
              </div>

              <div>
                <p className="text-sm font-semibold text-white">
                  Detailed final report
                </p>

                <p className="mt-2 text-xs leading-5 text-slate-400">
                  Receive feedback about strengths, weaknesses,
                  assessments, and recommendations after completion.
                </p>
              </div>
            </div>
          </section>

          {/* START INTERVIEW */}
          <section className="glass-panel rounded-2xl p-6 sm:p-7">
            <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
              <div>
                <p className="font-mono text-xs uppercase tracking-[0.25em] text-slate-500">
                  Ready?
                </p>

                <h2 className="mt-2 text-2xl font-semibold text-white">
                  Start your mock interview
                </h2>

                <p className="mt-2 text-sm text-slate-400">
                  {selectedTopicName}
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
                className="group inline-flex min-w-[210px] items-center justify-center gap-3 rounded-xl bg-violet-500 px-7 py-4 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition hover:-translate-y-0.5 hover:bg-violet-400 hover:shadow-violet-500/30 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:translate-y-0"
              >
                {isStarting ? "Preparing..." : "Start Interview"}

                {!isStarting && (
                  <span className="transition-transform group-hover:translate-x-1">
                    →
                  </span>
                )}
              </button>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
