import { useState } from "react";

import {
  useNavigate,
} from "react-router-dom";

import {
  CodingLanguage,
  Difficulty,
  getCodingQuestions,
} from "../lib/api";


/* =========================================================
   PROGRAMMING LANGUAGES
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
];


/* =========================================================
   DIFFICULTIES
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
   COMPONENT
   ========================================================= */

function CodingInterviewSetup() {
  const navigate = useNavigate();

  const [selectedLanguage, setSelectedLanguage] =
    useState<CodingLanguage>("python");

  const [selectedDifficulty, setSelectedDifficulty] =
    useState<Difficulty>("easy");

  const [questionCount, setQuestionCount] =
    useState<number>(5);

  const [starting, setStarting] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  /* =======================================================
     START CODING INTERVIEW
     ======================================================= */

  async function handleStartInterview() {
    try {
      setStarting(true);
      setError(null);

      /*
       * Get coding questions based on:
       *
       * 1. Programming language
       * 2. Difficulty
       *
       * Topic selection is intentionally removed because
       * the programming language now determines the coding
       * question pool.
       */

      const questions =
        await getCodingQuestions(
          selectedLanguage,
          selectedDifficulty,
        );


      if (questions.length === 0) {
        setError(
          "No coding questions are available for this language and difficulty.",
        );

        return;
      }


      /*
       * Pass the selected configuration and questions
       * to the coding interview room.
       */

      navigate(
        "/coding-interview",
        {
          state: {
            language: selectedLanguage,
            difficulty: selectedDifficulty,
            questionCount: Math.min(
              questionCount,
              questions.length,
            ),
            questions,
          },
        },
      );

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to start coding interview.",
      );

    } finally {
      setStarting(false);
    }
  }


  /* =======================================================
     UI
     ======================================================= */

  return (
    <div className="app-background min-h-screen">

      <div className="app-grid" />


      <main
        className="
          relative
          z-10
          mx-auto
          max-w-6xl
          px-6
          py-12
        "
      >

        {/* =================================================
            BACK
        ================================================== */}

        <button
          type="button"
          onClick={() =>
            navigate("/home")
          }
          className="
            mb-8
            text-sm
            text-slate-400
            transition
            hover:text-white
          "
        >
          ← Back to home
        </button>


        {/* =================================================
            HEADER
        ================================================== */}

        <div className="mb-10">

          <p
            className="
              mb-3
              font-mono
              text-xs
              uppercase
              tracking-[0.3em]
              text-violet-400
            "
          >
            Coding Interview
          </p>


          <h1
            className="
              text-4xl
              font-semibold
              tracking-tight
              text-white
              md:text-5xl
            "
          >
            Configure your coding interview
          </h1>


          <p
            className="
              mt-4
              max-w-2xl
              text-base
              leading-7
              text-slate-400
            "
          >
            Choose a programming language, difficulty,
            and number of questions before starting
            your coding interview.
          </p>

        </div>


        {/* =================================================
            ERROR
        ================================================== */}

        {error && (
          <div
            className="
              mb-6
              rounded-xl
              border
              border-rose-500/30
              bg-rose-500/10
              px-5
              py-4
              text-sm
              text-rose-300
            "
          >
            {error}
          </div>
        )}


        {/* =================================================
            MAIN OPTIONS
        ================================================== */}

        <div className="space-y-8">


          {/* ===============================================
              LANGUAGE
          ================================================ */}

          <section
            className="
              glass-panel
              rounded-2xl
              p-7
            "
          >

            <div className="mb-6">

              <p
                className="
                  font-mono
                  text-xs
                  uppercase
                  tracking-[0.25em]
                  text-slate-500
                "
              >
                Step 01
              </p>


              <h2
                className="
                  mt-2
                  text-2xl
                  font-semibold
                  text-white
                "
              >
                Choose a language
              </h2>


              <p
                className="
                  mt-2
                  text-sm
                  text-slate-400
                "
              >
                Select the programming language you
                want to use during the interview.
              </p>

            </div>


            <div
              className="
                grid
                gap-4
                sm:grid-cols-2
                lg:grid-cols-4
              "
            >

              {languages.map((language) => {

                const selected =
                  selectedLanguage ===
                  language.value;


                return (
                  <button
                    key={language.value}
                    type="button"
                    onClick={() =>
                      setSelectedLanguage(
                        language.value,
                      )
                    }
                    className={`
                      rounded-xl
                      border
                      p-5
                      text-left
                      transition

                      ${
                        selected
                          ? "border-cyan-400/50 bg-cyan-400/10"
                          : "border-white/10 bg-white/[0.02] hover:border-white/20"
                      }
                    `}
                  >

                    <div
                      className="
                        flex
                        items-start
                        justify-between
                        gap-4
                      "
                    >

                      <div>

                        <h3
                          className="
                            text-lg
                            font-semibold
                            text-white
                          "
                        >
                          {language.label}
                        </h3>


                        <p
                          className="
                            mt-2
                            text-xs
                            leading-5
                            text-slate-400
                          "
                        >
                          {language.description}
                        </p>

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
                            selected
                              ? "border-cyan-400"
                              : "border-white/20"
                          }
                        `}
                      >

                        {selected && (
                          <div
                            className="
                              h-2.5
                              w-2.5
                              rounded-full
                              bg-cyan-400
                            "
                          />
                        )}

                      </div>

                    </div>

                  </button>
                );

              })}

            </div>

          </section>


          {/* ===============================================
              DIFFICULTY
          ================================================ */}

          <section
            className="
              glass-panel
              rounded-2xl
              p-7
            "
          >

            <div className="mb-6">

              <p
                className="
                  font-mono
                  text-xs
                  uppercase
                  tracking-[0.25em]
                  text-slate-500
                "
              >
                Step 02
              </p>


              <h2
                className="
                  mt-2
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
                  text-slate-400
                "
              >
                Questions can adapt based on your
                performance.
              </p>

            </div>


            <div
              className="
                grid
                gap-4
                md:grid-cols-3
              "
            >

              {difficulties.map((difficulty) => {

                const selected =
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
                      rounded-xl
                      border
                      p-5
                      text-left
                      transition

                      ${
                        selected
                          ? "border-violet-500/60 bg-violet-500/10"
                          : "border-white/10 bg-white/[0.02] hover:border-white/20"
                      }
                    `}
                  >

                    <div
                      className="
                        flex
                        items-center
                        justify-between
                      "
                    >

                      <h3
                        className="
                          text-lg
                          font-semibold
                          text-white
                        "
                      >
                        {difficulty.label}
                      </h3>


                      <div
                        className={`
                          h-5
                          w-5
                          rounded-full
                          border

                          ${
                            selected
                              ? "border-violet-400 bg-violet-400"
                              : "border-white/20"
                          }
                        `}
                      />

                    </div>


                    <p
                      className="
                        mt-2
                        text-sm
                        leading-6
                        text-slate-400
                      "
                    >
                      {difficulty.description}
                    </p>

                  </button>
                );

              })}

            </div>

          </section>


          {/* ===============================================
              QUESTION COUNT
          ================================================ */}

          <section
            className="
              glass-panel
              rounded-2xl
              p-7
            "
          >

            <div className="mb-6">

              <p
                className="
                  font-mono
                  text-xs
                  uppercase
                  tracking-[0.25em]
                  text-slate-500
                "
              >
                Step 03
              </p>


              <h2
                className="
                  mt-2
                  text-2xl
                  font-semibold
                  text-white
                "
              >
                Number of questions
              </h2>


              <p
                className="
                  mt-2
                  text-sm
                  text-slate-400
                "
              >
                Choose how many coding problems you
                want to solve.
              </p>

            </div>


            <div className="flex flex-wrap gap-3">

              {[3, 5, 7, 10].map((count) => {

                const selected =
                  questionCount === count;


                return (
                  <button
                    key={count}
                    type="button"
                    onClick={() =>
                      setQuestionCount(count)
                    }
                    className={`
                      rounded-lg
                      border
                      px-6
                      py-3
                      text-sm
                      font-medium
                      transition

                      ${
                        selected
                          ? "border-violet-500/60 bg-violet-500/15 text-white"
                          : "border-white/10 bg-white/[0.02] text-slate-400 hover:text-white"
                      }
                    `}
                  >
                    {count} Questions
                  </button>
                );

              })}

            </div>

          </section>


          {/* ===============================================
              START
          ================================================ */}

          <section
            className="
              glass-panel
              rounded-2xl
              p-7
            "
          >

            <div
              className="
                flex
                flex-col
                gap-6
                md:flex-row
                md:items-center
                md:justify-between
              "
            >

              <div>

                <p
                  className="
                    font-mono
                    text-xs
                    uppercase
                    tracking-[0.25em]
                    text-slate-500
                  "
                >
                  Ready?
                </p>


                <h2
                  className="
                    mt-2
                    text-2xl
                    font-semibold
                    text-white
                  "
                >
                  Start your coding interview
                </h2>


                <p
                  className="
                    mt-2
                    text-sm
                    text-slate-400
                  "
                >
                  Your code will be tested against
                  coding test cases during the interview.
                </p>

              </div>


              <button
                type="button"
                disabled={starting}
                onClick={handleStartInterview}
                className="
                  rounded-xl
                  bg-violet-500
                  px-7
                  py-4
                  text-sm
                  font-semibold
                  text-white
                  shadow-lg
                  shadow-violet-500/20
                  transition
                  hover:bg-violet-400
                  disabled:cursor-not-allowed
                  disabled:opacity-50
                "
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