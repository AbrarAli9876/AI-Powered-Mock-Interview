import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API_BASE_URL = "http://localhost:8000";

type Difficulty = "easy" | "medium" | "hard";

interface Topic {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
}

interface InterviewResponse {
  id: number;
  user_id: number;
  topic_id: number;
  starting_difficulty: Difficulty;
  current_difficulty: Difficulty;
  status: string;
  total_questions: number;
  current_question_number: number;
}

const difficulties: {
  value: Difficulty;
  label: string;
  description: string;
}[] = [
  {
    value: "easy",
    label: "Easy",
    description:
      "Fundamental questions to warm up and build confidence.",
  },
  {
    value: "medium",
    label: "Medium",
    description:
      "Standard technical interview questions with moderate depth.",
  },
  {
    value: "hard",
    label: "Hard",
    description:
      "Challenging questions designed to test deeper understanding.",
  },
];

export default function InterviewSetup() {
  const navigate = useNavigate();

  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopic, setSelectedTopic] =
    useState<number | null>(null);

  const [selectedDifficulty, setSelectedDifficulty] =
    useState<Difficulty>("medium");

  const [isLoadingTopics, setIsLoadingTopics] =
    useState(true);

  const [isStarting, setIsStarting] =
    useState(false);

  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login", { replace: true });
      return;
    }

    const fetchTopics = async () => {
      try {
        setIsLoadingTopics(true);
        setError("");

        const response = await fetch(
          `${API_BASE_URL}/topics`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
              Accept: "application/json",
            },
          }
        );

        if (!response.ok) {
          if (response.status === 401) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("user");

            navigate("/login", {
              replace: true,
            });

            return;
          }

          throw new Error(
            "Unable to load interview topics."
          );
        }

        const data: Topic[] = await response.json();

        setTopics(data);

        if (data.length > 0) {
          setSelectedTopic(data[0].id);
        }
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load interview topics."
        );
      } finally {
        setIsLoadingTopics(false);
      }
    };

    fetchTopics();
  }, [navigate]);

  const handleStartInterview = async () => {
    if (!selectedTopic) {
      setError("Please select an interview topic.");
      return;
    }

    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login", { replace: true });
      return;
    }

    try {
      setIsStarting(true);
      setError("");

      const response = await fetch(
        `${API_BASE_URL}/interviews`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({
            topic_id: selectedTopic,
            starting_difficulty: selectedDifficulty,
          }),
        }
      );

      if (!response.ok) {
        if (response.status === 401) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("user");

          navigate("/login", {
            replace: true,
          });

          return;
        }

        const errorData = await response.json().catch(
          () => null
        );

        throw new Error(
          errorData?.detail ||
            "Unable to start the interview."
        );
      }

      const interview: InterviewResponse =
        await response.json();

      navigate(`/interviews/${interview.id}`, {
        replace: true,
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to start the interview."
      );
    } finally {
      setIsStarting(false);
    }
  };

  const selectedTopicData = topics.find(
    (topic) => topic.id === selectedTopic
  );

  return (
    <div className="app-background min-h-screen">

      {/* =====================================================
          BACKGROUND
          ===================================================== */}

      <div className="app-grid" />

      <div
        className="
          glow-orb
          glow-orb-violet
          left-[-150px]
          top-[180px]
          animate-pulse-slow
        "
      />

      <div
        className="
          glow-orb
          glow-orb-cyan
          right-[-120px]
          top-[300px]
          animate-pulse-slow
        "
      />


      {/* =====================================================
          HEADER
          ===================================================== */}

      <header
        className="
          relative
          z-20
          border-b
          border-white/[0.06]
        "
      >

        <div
          className="
            mx-auto
            flex
            max-w-7xl
            items-center
            justify-between
            px-6
            py-5
            lg:px-10
          "
        >

          <button
            onClick={() => navigate("/home")}
            className="
              flex
              items-center
              gap-3
              text-left
            "
          >

            <div
              className="
                flex
                h-10
                w-10
                items-center
                justify-center
                rounded-xl
                border
                border-violet-400/30
                bg-violet-500/10
                shadow-glow
              "
            >
              <span
                className="
                  font-display
                  text-sm
                  font-bold
                  text-violet-300
                "
              >
                AI
              </span>
            </div>


            <div>

              <div
                className="
                  font-display
                  text-sm
                  font-semibold
                  tracking-wide
                  text-white
                "
              >
                MOCK INTERVIEW
              </div>

              <div
                className="
                  font-mono
                  text-[9px]
                  uppercase
                  tracking-[0.2em]
                  text-slate-600
                "
              >
                Interview setup
              </div>

            </div>

          </button>


          <button
            onClick={() => navigate("/home")}
            className="
              rounded-lg
              border
              border-white/10
              bg-white/[0.025]
              px-4
              py-2
              text-sm
              text-slate-400
              transition
              hover:border-white/20
              hover:bg-white/[0.05]
              hover:text-white
            "
          >
            ← Back
          </button>

        </div>

      </header>


      {/* =====================================================
          MAIN
          ===================================================== */}

      <main
        className="
          relative
          z-10
          mx-auto
          max-w-5xl
          px-6
          py-12
          lg:px-10
          lg:py-16
        "
      >

        {/* Heading */}

        <section className="mb-10">

          <div
            className="
              font-mono
              text-[10px]
              uppercase
              tracking-[0.2em]
              text-violet-400
            "
          >
            New interview
          </div>

          <h1
            className="
              mt-3
              font-display
              text-4xl
              font-semibold
              tracking-[-0.035em]
              text-white
              sm:text-5xl
            "
          >
            Configure your challenge.
          </h1>

          <p
            className="
              mt-4
              max-w-2xl
              text-base
              leading-7
              text-slate-500
            "
          >
            Choose what you want to practice and
            where you want the interview to begin.
            The AI will adapt the difficulty as you
            perform.
          </p>

        </section>


        {/* ===================================================
            ERROR
            =================================================== */}

        {error && (
          <div
            role="alert"
            className="
              mb-6
              flex
              items-start
              gap-3
              rounded-xl
              border
              border-red-400/15
              bg-red-400/[0.04]
              p-4
            "
          >

            <div
              className="
                mt-0.5
                flex
                h-6
                w-6
                shrink-0
                items-center
                justify-center
                rounded-full
                bg-red-400/10
                text-xs
                text-red-300
              "
            >
              !
            </div>

            <div>

              <div className="text-sm font-medium text-red-300">
                Something went wrong
              </div>

              <div className="mt-1 text-xs text-red-300/60">
                {error}
              </div>

            </div>

          </div>
        )}


        {/* ===================================================
            TOPIC SELECTION
            =================================================== */}

        <section>

          <div className="mb-5">

            <div
              className="
                font-mono
                text-[10px]
                uppercase
                tracking-[0.18em]
                text-slate-600
              "
            >
              Step 01
            </div>

            <h2
              className="
                mt-2
                font-display
                text-xl
                font-semibold
                text-white
              "
            >
              What do you want to practice?
            </h2>

          </div>


          {isLoadingTopics ? (
            <div
              className="
                glass-panel
                flex
                min-h-48
                items-center
                justify-center
                rounded-2xl
              "
            >

              <div className="text-center">

                <div
                  className="
                    mx-auto
                    h-8
                    w-8
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
                    tracking-[0.15em]
                    text-slate-600
                  "
                >
                  Loading topics
                </p>

              </div>

            </div>
          ) : topics.length === 0 ? (
            <div
              className="
                glass-panel
                rounded-2xl
                p-8
                text-center
              "
            >

              <div
                className="
                  mx-auto
                  flex
                  h-12
                  w-12
                  items-center
                  justify-center
                  rounded-xl
                  border
                  border-amber-400/10
                  bg-amber-400/[0.04]
                  font-mono
                  text-sm
                  text-amber-300
                "
              >
                —
              </div>

              <h3
                className="
                  mt-5
                  font-display
                  font-semibold
                  text-white
                "
              >
                No topics available
              </h3>

              <p className="mt-2 text-sm text-slate-600">
                There are currently no active interview
                topics. Please try again later.
              </p>

            </div>
          ) : (
            <div className="grid gap-3 sm:grid-cols-2">

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
                    aria-pressed={isSelected}
                    className={`
                      group
                      rounded-2xl
                      border
                      p-5
                      text-left
                      transition-all
                      duration-300
                      ${
                        isSelected
                          ? "border-violet-400/30 bg-violet-500/[0.08] shadow-[0_0_35px_rgba(139,92,246,0.08)]"
                          : "border-white/[0.06] bg-white/[0.02] hover:border-white/[0.12] hover:bg-white/[0.035]"
                      }
                    `}
                  >

                    <div className="flex items-start justify-between gap-4">

                      <div>

                        <h3
                          className={`
                            font-display
                            text-base
                            font-semibold
                            transition-colors
                            ${
                              isSelected
                                ? "text-violet-200"
                                : "text-white"
                            }
                          `}
                        >
                          {topic.name}
                        </h3>

                        <p
                          className="
                            mt-2
                            text-xs
                            leading-5
                            text-slate-600
                          "
                        >
                          {topic.description ||
                            "Technical interview practice."}
                        </p>

                      </div>


                      <div
                        className={`
                          flex
                          h-6
                          w-6
                          shrink-0
                          items-center
                          justify-center
                          rounded-full
                          border
                          ${
                            isSelected
                              ? "border-violet-400/40 bg-violet-400/10"
                              : "border-white/10 bg-white/[0.02]"
                          }
                        `}
                      >

                        {isSelected && (
                          <div
                            className="
                              h-2
                              w-2
                              rounded-full
                              bg-violet-300
                              shadow-[0_0_10px_rgba(196,181,253,0.8)]
                            "
                          />
                        )}

                      </div>

                    </div>

                  </button>
                );
              })}

            </div>
          )}

        </section>


        {/* ===================================================
            DIFFICULTY
            =================================================== */}

        <section className="mt-12">

          <div className="mb-5">

            <div
              className="
                font-mono
                text-[10px]
                uppercase
                tracking-[0.18em]
                text-slate-600
              "
            >
              Step 02
            </div>

            <h2
              className="
                mt-2
                font-display
                text-xl
                font-semibold
                text-white
              "
            >
              Choose your starting difficulty.
            </h2>

          </div>


          <div className="grid gap-3 md:grid-cols-3">

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
                      difficulty.value
                    )
                  }
                  aria-pressed={isSelected}
                  className={`
                    group
                    rounded-2xl
                    border
                    p-5
                    text-left
                    transition-all
                    duration-300
                    ${
                      isSelected
                        ? "border-cyan-400/25 bg-cyan-400/[0.045]"
                        : "border-white/[0.06] bg-white/[0.02] hover:border-white/[0.12] hover:bg-white/[0.035]"
                    }
                  `}
                >

                  <div className="flex items-center justify-between">

                    <span
                      className={`
                        font-mono
                        text-[10px]
                        uppercase
                        tracking-[0.16em]
                        ${
                          isSelected
                            ? "text-cyan-300"
                            : "text-slate-500"
                        }
                      `}
                    >
                      {difficulty.value}
                    </span>


                    <div
                      className={`
                        flex
                        h-5
                        w-5
                        items-center
                        justify-center
                        rounded-full
                        border
                        ${
                          isSelected
                            ? "border-cyan-400/40"
                            : "border-white/10"
                        }
                      `}
                    >

                      {isSelected && (
                        <div className="h-2 w-2 rounded-full bg-cyan-300" />
                      )}

                    </div>

                  </div>


                  <h3
                    className="
                      mt-5
                      font-display
                      text-base
                      font-semibold
                      text-white
                    "
                  >
                    {difficulty.label}
                  </h3>


                  <p
                    className="
                      mt-2
                      text-xs
                      leading-5
                      text-slate-600
                    "
                  >
                    {difficulty.description}
                  </p>

                </button>
              );
            })}

          </div>

        </section>


        {/* ===================================================
            SUMMARY
            =================================================== */}

        <section className="mt-12">

          <div
            className="
              glass-panel
              overflow-hidden
              rounded-2xl
            "
          >

            <div
              className="
                border-b
                border-white/[0.06]
                px-6
                py-4
              "
            >

              <div
                className="
                  font-mono
                  text-[10px]
                  uppercase
                  tracking-[0.18em]
                  text-slate-600
                "
              >
                Configuration
              </div>

            </div>


            <div
              className="
                grid
                gap-6
                px-6
                py-6
                sm:grid-cols-2
              "
            >

              <div>

                <div
                  className="
                    font-mono
                    text-[9px]
                    uppercase
                    tracking-[0.15em]
                    text-slate-700
                  "
                >
                  Topic
                </div>

                <div className="mt-2 text-sm font-medium text-slate-200">
                  {selectedTopicData?.name ||
                    "No topic selected"}
                </div>

              </div>


              <div>

                <div
                  className="
                    font-mono
                    text-[9px]
                    uppercase
                    tracking-[0.15em]
                    text-slate-700
                  "
                >
                  Starting difficulty
                </div>

                <div className="mt-2 text-sm font-medium capitalize text-slate-200">
                  {selectedDifficulty}
                </div>

              </div>

            </div>

          </div>

        </section>


        {/* ===================================================
            START BUTTON
            =================================================== */}

        <div
          className="
            mt-8
            flex
            flex-col-reverse
            gap-3
            sm:flex-row
            sm:justify-end
          "
        >

          <button
            type="button"
            onClick={() => navigate("/home")}
            disabled={isStarting}
            className="
              rounded-xl
              border
              border-white/10
              bg-white/[0.025]
              px-6
              py-3.5
              font-display
              text-sm
              font-medium
              text-slate-400
              transition
              hover:border-white/20
              hover:bg-white/[0.05]
              hover:text-white
              disabled:cursor-not-allowed
              disabled:opacity-40
            "
          >
            Cancel
          </button>


          <button
            type="button"
            onClick={handleStartInterview}
            disabled={
              isStarting ||
              isLoadingTopics ||
              !selectedTopic
            }
            className="
              group
              inline-flex
              items-center
              justify-center
              gap-3
              rounded-xl
              bg-white
              px-7
              py-3.5
              font-display
              text-sm
              font-semibold
              text-slate-950
              shadow-[0_10px_35px_rgba(255,255,255,0.06)]
              transition-all
              duration-300
              hover:-translate-y-0.5
              hover:shadow-[0_15px_45px_rgba(139,92,246,0.2)]
              active:translate-y-0
              disabled:cursor-not-allowed
              disabled:opacity-40
              disabled:hover:translate-y-0
            "
          >

            {isStarting ? (
              <>
                <span
                  className="
                    h-4
                    w-4
                    animate-spin
                    rounded-full
                    border-2
                    border-slate-400
                    border-t-slate-950
                  "
                />

                Creating interview...
              </>
            ) : (
              <>
                Start interview

                <span
                  className="
                    transition-transform
                    duration-300
                    group-hover:translate-x-1
                  "
                >
                  →
                </span>
              </>
            )}

          </button>

        </div>


        {/* ===================================================
            FOOTER NOTE
            =================================================== */}

        <div
          className="
            mt-10
            border-t
            border-white/[0.05]
            pt-6
            text-center
          "
        >

          <p
            className="
              font-mono
              text-[9px]
              uppercase
              tracking-[0.15em]
              text-slate-700
            "
          >
            Your interview difficulty adapts based
            on your performance
          </p>

        </div>

      </main>

    </div>
  );
}