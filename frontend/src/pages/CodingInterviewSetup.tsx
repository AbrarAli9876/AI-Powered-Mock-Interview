import {
  useState,
} from "react";

import {
  useNavigate,
} from "react-router-dom";

import {
  createCodingInterview,
  type CodingLanguage,
  type Difficulty,
} from "../lib/api";

/* =========================================================
   LANGUAGE OPTIONS
   ========================================================= */

const languages: {
  value: CodingLanguage;
  label: string;
  description: string;
}[] = [
  {
    value: "python",
    label: "Python",
    description:
      "Clean and beginner-friendly programming.",
  },

  {
    value: "javascript",
    label: "JavaScript",
    description:
      "Popular language for web development.",
  },

  {
    value: "java",
    label: "Java",
    description:
      "Object-oriented programming language.",
  },

  {
    value: "cpp",
    label: "C++",
    description:
      "Powerful language for performance-focused programming.",
  },

  {
    value: "sql",
    label: "SQL",
    description:
      "Query, filter, join, and analyze relational data.",
  },
];


/* =========================================================
   DIFFICULTY OPTIONS
   ========================================================= */

const difficulties: {
  value: Difficulty;
  label: string;
  description: string;
}[] = [
  {
    value: "easy",
    label: "Easy",
    description:
      "Basic programming and problem-solving concepts.",
  },

  {
    value: "medium",
    label: "Medium",
    description:
      "Intermediate algorithms and practical problems.",
  },

  {
    value: "hard",
    label: "Hard",
    description:
      "Advanced algorithms and challenging problems.",
  },
];


/* =========================================================
   QUESTION COUNT
   ========================================================= */

const QUESTION_COUNTS = [
  3,
  5,
  10,
];


/* =========================================================
   COMPONENT
   ========================================================= */

function CodingInterviewSetup() {
  const navigate = useNavigate();


  /* =======================================================
     STATE
     ======================================================= */

  const [
    selectedLanguage,
    setSelectedLanguage,
  ] = useState<CodingLanguage>(
    "python",
  );


  const [
    selectedDifficulty,
    setSelectedDifficulty,
  ] = useState<Difficulty>(
    "easy",
  );


  const [
    questionCount,
    setQuestionCount,
  ] = useState<number>(5);


  const [
    starting,
    setStarting,
  ] = useState(false);


  const [
    error,
    setError,
  ] = useState<string | null>(null);


  /* =========================================================
     START CODING INTERVIEW
     ========================================================= */

  async function handleStartInterview() {
    try {
      setStarting(true);
      setError(null);

      const setup = {
        language: selectedLanguage,
        difficulty: selectedDifficulty,
        questionCount,
      };

      // Keep coding-interview settings separate from technical-interview settings.
      sessionStorage.setItem("codingInterviewSetup", JSON.stringify(setup));
      sessionStorage.removeItem("codingInterviewPreflightVerified");
      sessionStorage.setItem("codingInterviewPreflightStage", "fullscreen");

      // The coding session is created only after all three checks are complete.
      navigate("/coding-interview/preflight/fullscreen", { state: { setup } });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to open coding interview security checks.",
      );
    } finally {
      setStarting(false);
    }
  }


  /* =========================================================
     RENDER
     ========================================================= */

  return (
    <div className="app-background min-h-screen">

      <div className="app-grid" />


      <main className="relative z-10 mx-auto max-w-6xl px-6 py-12">


        {/* ===================================================
            BACK
        ==================================================== */}

        <button
          type="button"
          onClick={() =>
            navigate("/home")
          }
          className="mb-8 text-sm text-slate-400 hover:text-white"
        >
          ← Back to home
        </button>


        {/* ===================================================
            HEADER
        ==================================================== */}

        <div className="mb-10">

          <p className="mb-3 font-mono text-xs uppercase tracking-[0.3em] text-violet-400">
            Coding Interview
          </p>


          <h1 className="text-4xl font-semibold tracking-tight text-white md:text-5xl">
            Configure your coding interview
          </h1>


          <p className="mt-4 max-w-2xl text-base leading-7 text-slate-400">
            Choose a programming language,
            difficulty, and number of coding
            problems before starting your
            interview.
          </p>

        </div>


        {/* ===================================================
            ERROR
        ==================================================== */}

        {error && (

          <div className="mb-6 rounded-xl border border-rose-500/30 bg-rose-500/10 px-5 py-4 text-sm text-rose-300">
            {error}
          </div>

        )}


        <div className="space-y-8">


          {/* =================================================
              LANGUAGE
          ================================================== */}

          <section className="glass-panel rounded-2xl p-7">

            <div className="mb-6">

              <p className="font-mono text-xs uppercase tracking-[0.25em] text-slate-500">
                Step 01
              </p>


              <h2 className="mt-2 text-2xl font-semibold text-white">
                Choose a language
              </h2>


              <p className="mt-2 text-sm text-slate-400">
                Select the programming language
                you want to use during the
                interview.
              </p>

            </div>


            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">

              {languages.map(
                (language) => {

                  const selected =
                    selectedLanguage ===
                    language.value;


                  return (

                    <button
                      key={
                        language.value
                      }
                      type="button"
                      onClick={() =>
                        setSelectedLanguage(
                          language.value,
                        )
                      }
                      disabled={starting}
                      className={`rounded-xl border p-5 text-left transition ${
                        selected
                          ? "border-cyan-400/50 bg-cyan-400/10"
                          : "border-white/10 bg-white/[0.02] hover:border-white/20"
                      } disabled:cursor-not-allowed disabled:opacity-60`}
                    >

                      <div className="flex items-center justify-between">

                        <h3 className="text-lg font-semibold text-white">
                          {
                            language.label
                          }
                        </h3>


                        <div
                          className={`h-5 w-5 rounded-full border ${
                            selected
                              ? "border-cyan-400 bg-cyan-400"
                              : "border-white/20"
                          }`}
                        />

                      </div>


                      <p className="mt-2 text-xs leading-5 text-slate-400">
                        {
                          language.description
                        }
                      </p>

                    </button>

                  );
                },
              )}

            </div>

          </section>


          {/* =================================================
              DIFFICULTY
          ================================================== */}

          <section className="glass-panel rounded-2xl p-7">

            <div className="mb-6">

              <p className="font-mono text-xs uppercase tracking-[0.25em] text-slate-500">
                Step 02
              </p>


              <h2 className="mt-2 text-2xl font-semibold text-white">
                Difficulty
              </h2>


              <p className="mt-2 text-sm text-slate-400">
                Choose the difficulty of the
                coding problems.
              </p>

            </div>


            <div className="grid gap-4 md:grid-cols-3">

              {difficulties.map(
                (difficulty) => {

                  const selected =
                    selectedDifficulty ===
                    difficulty.value;


                  return (

                    <button
                      key={
                        difficulty.value
                      }
                      type="button"
                      onClick={() =>
                        setSelectedDifficulty(
                          difficulty.value,
                        )
                      }
                      disabled={starting}
                      className={`rounded-xl border p-5 text-left transition ${
                        selected
                          ? "border-violet-500/60 bg-violet-500/10"
                          : "border-white/10 bg-white/[0.02] hover:border-white/20"
                      } disabled:cursor-not-allowed disabled:opacity-60`}
                    >

                      <div className="flex items-center justify-between">

                        <h3 className="text-lg font-semibold text-white">
                          {
                            difficulty.label
                          }
                        </h3>


                        <div
                          className={`h-5 w-5 rounded-full border ${
                            selected
                              ? "border-violet-400 bg-violet-400"
                              : "border-white/20"
                          }`}
                        />

                      </div>


                      <p className="mt-2 text-sm leading-6 text-slate-400">
                        {
                          difficulty.description
                        }
                      </p>

                    </button>

                  );
                },
              )}

            </div>

          </section>


          {/* =================================================
              QUESTION COUNT
          ================================================== */}

          <section className="glass-panel rounded-2xl p-7">

            <div className="mb-6">

              <p className="font-mono text-xs uppercase tracking-[0.25em] text-slate-500">
                Step 03
              </p>


              <h2 className="mt-2 text-2xl font-semibold text-white">
                Number of questions
              </h2>


              <p className="mt-2 text-sm text-slate-400">
                Choose how many coding problems
                you want to solve.
              </p>

            </div>


            <div className="flex flex-wrap gap-3">

              {QUESTION_COUNTS.map(
                (count) => {

                  const selected =
                    questionCount ===
                    count;


                  return (

                    <button
                      key={count}
                      type="button"
                      onClick={() =>
                        setQuestionCount(
                          count,
                        )
                      }
                      disabled={starting}
                      className={`rounded-lg border px-6 py-3 text-sm font-medium transition ${
                        selected
                          ? "border-violet-500/60 bg-violet-500/15 text-white"
                          : "border-white/10 bg-white/[0.02] text-slate-400 hover:text-white"
                      } disabled:cursor-not-allowed disabled:opacity-60`}
                    >
                      {count} Questions
                    </button>

                  );
                },
              )}

            </div>

          </section>


          {/* =================================================
              INTERVIEW RULES
          ================================================== */}

          <section className="rounded-2xl border border-cyan-400/10 bg-cyan-400/[0.03] p-7">

            <p className="font-mono text-xs uppercase tracking-[0.25em] text-cyan-400/70">
              Interview Format
            </p>


            <div className="mt-5 grid gap-4 md:grid-cols-3">

              <div>

                <p className="text-sm font-semibold text-white">
                  Fixed Difficulty
                </p>

                <p className="mt-1 text-xs leading-5 text-slate-400">
                  All questions will remain at
                  the difficulty you selected.
                </p>

              </div>


              <div>

                <p className="text-sm font-semibold text-white">
                  Multiple Test Cases
                </p>

                <p className="mt-1 text-xs leading-5 text-slate-400">
                  Your solution will be tested
                  against the configured test cases.
                </p>

              </div>


              <div>

                <p className="text-sm font-semibold text-white">
                  Two Hints
                </p>

                <p className="mt-1 text-xs leading-5 text-slate-400">
                  Each coding problem provides
                  two hints to help you solve it.
                </p>

              </div>

            </div>

          </section>


          {/* =================================================
              START
          ================================================== */}

          <section className="glass-panel rounded-2xl p-7">

            <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">

              <div>

                <p className="font-mono text-xs uppercase tracking-[0.25em] text-slate-500">
                  Ready?
                </p>


                <h2 className="mt-2 text-2xl font-semibold text-white">
                  Start your coding interview
                </h2>


                <p className="mt-2 text-sm text-slate-400">
                  {
                    selectedLanguage
                  }{" "}
                  •{" "}
                  {
                    selectedDifficulty
                  }{" "}
                  •{" "}
                  {
                    questionCount
                  }{" "}
                  questions
                </p>

              </div>


              <button
                type="button"
                disabled={starting}
                onClick={
                  handleStartInterview
                }
                className="rounded-xl bg-violet-500 px-7 py-4 text-sm font-semibold text-white shadow-lg shadow-violet-500/20 transition hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {starting
                  ? "Preparing..."
                  : "Start Coding Interview →"}
              </button>

            </div>

          </section>

        </div>

      </main>

    </div>
  );
}


export default CodingInterviewSetup;