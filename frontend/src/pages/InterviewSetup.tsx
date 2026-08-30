import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  createInterview,
  getTopics,
  type Difficulty,
  type Topic,
} from "../lib/api";

const difficulties: {
  value: Difficulty;
  label: string;
  description: string;
}[] = [
  {
    value: "easy",
    label: "Easy",
    description:
      "Basic concepts and fundamental questions",
  },
  {
    value: "medium",
    label: "Medium",
    description:
      "Intermediate concepts and practical understanding",
  },
  {
    value: "hard",
    label: "Hard",
    description:
      "Advanced concepts and challenging problems",
  },
];

export default function InterviewSetup() {
  const navigate = useNavigate();

  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopic, setSelectedTopic] =
    useState<number | null>(null);

  const [selectedDifficulty, setSelectedDifficulty] =
    useState<Difficulty>("easy");

  const [isLoading, setIsLoading] =
    useState(true);

  const [isStarting, setIsStarting] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  /*
   * Load available topics
   */
  useEffect(() => {
    const loadTopics = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const data = await getTopics();

        setTopics(data);

        if (data.length > 0) {
          setSelectedTopic(data[0].id);
        }
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load topics.",
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadTopics();
  }, []);

  /*
   * Start interview
   */
  const handleStartInterview = async () => {
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
      );

      /*
       * Navigate to the interview room.
       */
      navigate(
        `/interviews/${interview.id}`,
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to start interview.",
      );
    } finally {
      setIsStarting(false);
    }
  };

  /*
   * Loading state
   */
  if (isLoading) {
    return (
      <div className="app-background min-h-screen flex items-center justify-center px-6">
        <div className="text-center">
          <div
            className="
              mx-auto
              h-10
              w-10
              animate-spin
              rounded-full
              border-2
              border-white/10
              border-t-violet-400
            "
          />

          <p
            className="
              mt-4
              font-mono
              text-[10px]
              uppercase
              tracking-[0.18em]
              text-slate-500
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
        <div className="mb-10">
          <button
            type="button"
            onClick={() => navigate("/home")}
            className="
              mb-8
              inline-flex
              items-center
              gap-2
              text-sm
              text-slate-500
              transition-colors
              hover:text-white
            "
          >
            <span>←</span>
            Back to home
          </button>

          <div
            className="
              font-mono
              text-[10px]
              uppercase
              tracking-[0.2em]
              text-violet-400
            "
          >
            Interview setup
          </div>

          <h1
            className="
              mt-3
              font-display
              text-4xl
              font-semibold
              tracking-tight
              text-white
              sm:text-5xl
            "
          >
            Configure your interview
          </h1>

          <p
            className="
              mt-4
              max-w-2xl
              text-sm
              leading-6
              text-slate-400
            "
          >
            Choose a topic and starting difficulty.
            Your interview will adapt based on your
            performance.
          </p>
        </div>

        {/* Error */}
        {error && (
          <div
            className="
              mb-6
              rounded-2xl
              border
              border-red-400/20
              bg-red-400/5
              px-5
              py-4
              text-sm
              text-red-300
            "
          >
            {error}
          </div>
        )}

        <div className="grid gap-8 lg:grid-cols-[1.15fr_0.85fr]">
          {/* Topic selection */}
          <section
            className="
              rounded-3xl
              border
              border-white/[0.06]
              bg-white/[0.025]
              p-6
              sm:p-8
            "
          >
            <div
              className="
                font-mono
                text-[10px]
                uppercase
                tracking-[0.18em]
                text-slate-500
              "
            >
              Step 01
            </div>

            <h2
              className="
                mt-2
                font-display
                text-2xl
                font-semibold
                text-white
              "
            >
              Choose a topic
            </h2>

            <p
              className="
                mt-2
                text-sm
                leading-6
                text-slate-500
              "
            >
              Select the technical topic you want
              to practice.
            </p>

            {topics.length === 0 ? (
              <div
                className="
                  mt-8
                  rounded-2xl
                  border
                  border-white/[0.06]
                  bg-black/10
                  p-6
                  text-center
                  text-sm
                  text-slate-500
                "
              >
                No active topics are available.
              </div>
            ) : (
              <div className="mt-7 grid gap-3">
                {topics.map((topic) => {
                  const isSelected =
                    selectedTopic === topic.id;

                  return (
                    <button
                      key={topic.id}
                      type="button"
                      onClick={() =>
                        setSelectedTopic(topic.id)
                      }
                      className={`
                        w-full
                        rounded-2xl
                        border
                        p-5
                        text-left
                        transition-all
                        duration-200
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
                              font-display
                              text-lg
                              font-semibold
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
                            <p
                              className="
                                mt-2
                                text-sm
                                leading-5
                                text-slate-500
                              "
                            >
                              {topic.description}
                            </p>
                          )}
                        </div>

                        <div
                          className={`
                            mt-1
                            flex
                            h-5
                            w-5
                            shrink-0
                            items-center
                            justify-center
                            rounded-full
                            border
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

          {/* Difficulty selection */}
          <section
            className="
              rounded-3xl
              border
              border-white/[0.06]
              bg-white/[0.025]
              p-6
              sm:p-8
            "
          >
            <div
              className="
                font-mono
                text-[10px]
                uppercase
                tracking-[0.18em]
                text-slate-500
              "
            >
              Step 02
            </div>

            <h2
              className="
                mt-2
                font-display
                text-2xl
                font-semibold
                text-white
              "
            >
              Starting difficulty
            </h2>

            <p
              className="
                mt-2
                text-sm
                leading-6
                text-slate-500
              "
            >
              The difficulty will adapt according
              to your answers.
            </p>

            <div className="mt-7 space-y-3">
              {difficulties.map((difficulty) => {
                const isSelected =
                  selectedDifficulty ===
                  difficulty.value;

                return (
                  <button
                    key={difficulty.value}
                    type="button"
                    onClick={() =>
                      setSelectedDifficulty(
                        difficulty.value,
                      )
                    }
                    className={`
                      w-full
                      rounded-2xl
                      border
                      p-5
                      text-left
                      transition-all
                      duration-200
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
                            font-display
                            text-lg
                            font-semibold
                            ${
                              isSelected
                                ? "text-violet-300"
                                : "text-white"
                            }
                          `}
                        >
                          {difficulty.label}
                        </h3>

                        <p
                          className="
                            mt-1
                            text-xs
                            leading-5
                            text-slate-500
                          "
                        >
                          {difficulty.description}
                        </p>
                      </div>

                      <div
                        className={`
                          flex
                          h-5
                          w-5
                          shrink-0
                          items-center
                          justify-center
                          rounded-full
                          border
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

            {/* Adaptive information */}
            <div
              className="
                mt-6
                rounded-2xl
                border
                border-white/[0.06]
                bg-black/10
                p-5
              "
            >
              <div
                className="
                  font-mono
                  text-[9px]
                  uppercase
                  tracking-[0.16em]
                  text-slate-600
                "
              >
                Adaptive interview
              </div>

              <p
                className="
                  mt-2
                  text-xs
                  leading-5
                  text-slate-500
                "
              >
                Strong answers can increase the
                difficulty, while weaker answers can
                reduce it.
              </p>
            </div>
          </section>
        </div>

        {/* Start interview */}
        <section
          className="
            mt-8
            rounded-3xl
            border
            border-white/[0.06]
            bg-white/[0.025]
            p-6
            sm:p-8
          "
        >
          <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <div
                className="
                  font-mono
                  text-[10px]
                  uppercase
                  tracking-[0.18em]
                  text-slate-500
                "
              >
                Ready?
              </div>

              <h2
                className="
                  mt-2
                  font-display
                  text-2xl
                  font-semibold
                  text-white
                "
              >
                Start your mock interview
              </h2>

              <p
                className="
                  mt-2
                  text-sm
                  text-slate-500
                "
              >
                Your answers will be evaluated by
                AI during the interview.
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
                group
                inline-flex
                min-w-[210px]
                items-center
                justify-center
                gap-3
                rounded-2xl
                bg-white
                px-6
                py-4
                font-display
                text-sm
                font-semibold
                text-slate-950
                transition-all
                duration-200
                hover:-translate-y-0.5
                hover:shadow-[0_15px_45px_rgba(139,92,246,0.25)]
                disabled:cursor-not-allowed
                disabled:opacity-40
                disabled:hover:translate-y-0
              "
            >
              {isStarting
                ? "Starting..."
                : "Start Interview"}

              {!isStarting && (
                <span
                  className="
                    transition-transform
                    duration-200
                    group-hover:translate-x-1
                  "
                >
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