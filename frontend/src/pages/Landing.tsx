import { useNavigate } from "react-router-dom";

export default function Landing() {
  const navigate = useNavigate();

  const scrollToFeatures = () => {
    document.getElementById("features")?.scrollIntoView({
      behavior: "smooth",
    });
  };

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  return (
    <div className="app-background min-h-screen">

      {/* ===================================================
          BACKGROUND
          =================================================== */}

      <div className="app-grid" />

      <div
        className="
          glow-orb
          glow-orb-violet
          left-[-100px]
          top-[160px]
          animate-pulse-slow
        "
      />

      <div
        className="
          glow-orb
          glow-orb-cyan
          right-[-80px]
          top-[100px]
          animate-pulse-slow
        "
      />


      {/* ===================================================
          NAVIGATION
          =================================================== */}

      <header className="relative z-10">

        <div
          className="
            mx-auto
            flex
            max-w-7xl
            items-center
            justify-between
            px-6
            py-7
            lg:px-10
          "
        >

          {/* Logo */}

          <button
            onClick={() => navigate("/")}
            className="
              group
              flex
              items-center
              gap-3
              bg-transparent
              p-0
              text-left
            "
            aria-label="AI Mock Interview home"
          >

            <div
              className="
                relative
                flex
                h-10
                w-10
                items-center
                justify-center
                overflow-hidden
                rounded-xl
                border
                border-violet-400/30
                bg-violet-500/10
                shadow-glow
              "
            >

              <div
                className="
                  absolute
                  inset-0
                  bg-gradient-to-br
                  from-violet-500/20
                  to-cyan-400/10
                "
              />

              <span
                className="
                  relative
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
                  tracking-[0.22em]
                  text-slate-500
                "
              >
                Intelligent Practice
              </div>

            </div>

          </button>


          {/* Navigation actions */}

          <div className="flex items-center gap-3">

            <button
              onClick={() => navigate("/login")}
              className="
                rounded-lg
                border
                border-white/10
                bg-white/[0.03]
                px-4
                py-2.5
                text-sm
                font-medium
                text-slate-300
                hover:border-white/20
                hover:bg-white/[0.07]
                hover:text-white
              "
            >
              Sign In
            </button>


            <button
              onClick={() => navigate("/register")}
              className="
                rounded-lg
                border
                border-violet-400/30
                bg-violet-500/15
                px-4
                py-2.5
                text-sm
                font-semibold
                text-violet-200
                shadow-[0_0_25px_rgba(139,92,246,0.12)]
                hover:bg-violet-500/25
              "
            >
              Create account
            </button>

          </div>

        </div>

      </header>


      {/* ===================================================
          HERO
          =================================================== */}

      <main className="relative z-10">

        <section
          className="
            mx-auto
            max-w-7xl
            px-6
            pb-24
            pt-20
            lg:px-10
            lg:pt-28
          "
        >

          <div
            className="
              grid
              items-center
              gap-16
              lg:grid-cols-[1.05fr_0.95fr]
            "
          >

            {/* =================================================
                HERO CONTENT
                ================================================= */}

            <div>

              {/* Status */}

              <div
                className="
                  mb-8
                  inline-flex
                  items-center
                  gap-2
                  rounded-full
                  border
                  border-white/10
                  bg-white/[0.035]
                  px-3.5
                  py-2
                  font-mono
                  text-[11px]
                  uppercase
                  tracking-[0.18em]
                  text-slate-400
                "
              >

                <span
                  className="
                    h-1.5
                    w-1.5
                    animate-pulse
                    rounded-full
                    bg-emerald-400
                    shadow-[0_0_10px_rgba(52,211,153,0.8)]
                  "
                />

                AI interviewer online

              </div>


              {/* Heading */}

              <h1
                className="
                  max-w-4xl
                  font-display
                  text-5xl
                  font-semibold
                  leading-[0.98]
                  tracking-[-0.045em]
                  text-white
                  sm:text-6xl
                  lg:text-7xl
                  xl:text-[84px]
                "
              >

                Practice like
                <br />

                <span
                  className="
                    bg-gradient-to-r
                    from-violet-300
                    via-purple-400
                    to-cyan-300
                    bg-clip-text
                    text-transparent
                  "
                >
                  you're already hired.
                </span>

              </h1>


              {/* Description */}

              <p
                className="
                  mt-8
                  max-w-xl
                  text-base
                  leading-7
                  text-slate-400
                  sm:text-lg
                "
              >
                A realistic AI-powered interview simulator
                that adapts to your performance, evaluates
                every answer, and shows exactly where you
                can improve.
              </p>


              {/* CTA */}

              <div className="mt-10 flex flex-wrap items-center gap-4">

                <button
                  onClick={() => navigate("/register")}
                  className="
                    group
                    relative
                    overflow-hidden
                    rounded-xl
                    bg-white
                    px-6
                    py-3.5
                    font-display
                    text-sm
                    font-semibold
                    text-slate-950
                    shadow-[0_10px_40px_rgba(255,255,255,0.08)]
                    hover:-translate-y-0.5
                    hover:shadow-[0_15px_45px_rgba(139,92,246,0.2)]
                  "
                >

                  <span className="relative z-10">
                    Start an interview
                  </span>

                  <span
                    className="
                      absolute
                      inset-0
                      -translate-x-full
                      bg-gradient-to-r
                      from-violet-200
                      to-cyan-200
                      transition-transform
                      duration-500
                      group-hover:translate-x-0
                    "
                  />

                </button>


                <button
                  onClick={() => navigate("/login")}
                  className="
                    rounded-xl
                    border
                    border-white/10
                    bg-white/[0.035]
                    px-6
                    py-3.5
                    font-display
                    text-sm
                    font-medium
                    text-slate-200
                    hover:border-white/20
                    hover:bg-white/[0.07]
                  "
                >
                  I already have an account
                </button>

              </div>


              {/* Trust indicators */}

              <div
                className="
                  mt-12
                  flex
                  flex-wrap
                  gap-x-8
                  gap-y-3
                  border-t
                  border-white/[0.06]
                  pt-6
                "
              >

                <div>

                  <div
                    className="
                      font-mono
                      text-[10px]
                      uppercase
                      tracking-[0.16em]
                      text-slate-600
                    "
                  >
                    Evaluation
                  </div>

                  <div className="mt-1 text-sm text-slate-300">
                    AI-powered
                  </div>

                </div>


                <div>

                  <div
                    className="
                      font-mono
                      text-[10px]
                      uppercase
                      tracking-[0.16em]
                      text-slate-600
                    "
                  >
                    Difficulty
                  </div>

                  <div className="mt-1 text-sm text-slate-300">
                    Adaptive
                  </div>

                </div>


                <div>

                  <div
                    className="
                      font-mono
                      text-[10px]
                      uppercase
                      tracking-[0.16em]
                      text-slate-600
                    "
                  >
                    Feedback
                  </div>

                  <div className="mt-1 text-sm text-slate-300">
                    Instant
                  </div>

                </div>

              </div>

            </div>


            {/* =================================================
                INTERVIEW PREVIEW
                ================================================= */}

            <div className="relative">

              <div
                className="
                  absolute
                  -inset-8
                  rounded-[40px]
                  bg-violet-500/[0.06]
                  blur-3xl
                "
              />


              <div
                className="
                  glass-panel
                  relative
                  overflow-hidden
                  rounded-3xl
                "
              >

                {/* Window bar */}

                <div
                  className="
                    flex
                    items-center
                    justify-between
                    border-b
                    border-white/[0.06]
                    px-5
                    py-4
                  "
                >

                  <div className="flex items-center gap-2">

                    <span className="h-2 w-2 rounded-full bg-red-400/80" />
                    <span className="h-2 w-2 rounded-full bg-amber-400/80" />
                    <span className="h-2 w-2 rounded-full bg-emerald-400/80" />

                  </div>


                  <div
                    className="
                      font-mono
                      text-[10px]
                      uppercase
                      tracking-[0.2em]
                      text-slate-600
                    "
                  >
                    Interview / 01
                  </div>

                </div>


                {/* AI content */}

                <div className="px-7 pb-8 pt-9">

                  <div className="flex items-start gap-4">

                    {/* AI Orb */}

                    <div
                      className="
                        relative
                        flex
                        h-14
                        w-14
                        shrink-0
                        items-center
                        justify-center
                      "
                    >

                      <div
                        className="
                          absolute
                          inset-0
                          animate-pulse-slow
                          rounded-full
                          bg-violet-500/20
                          blur-md
                        "
                      />

                      <div
                        className="
                          relative
                          flex
                          h-12
                          w-12
                          items-center
                          justify-center
                          rounded-full
                          border
                          border-violet-400/30
                          bg-gradient-to-br
                          from-violet-500/30
                          to-cyan-400/10
                        "
                      >

                        <div
                          className="
                            h-3
                            w-3
                            rounded-full
                            bg-violet-300
                            shadow-[0_0_18px_rgba(196,181,253,0.9)]
                          "
                        />

                      </div>

                    </div>


                    <div className="pt-1">

                      <div
                        className="
                          font-mono
                          text-[10px]
                          uppercase
                          tracking-[0.16em]
                          text-violet-300
                        "
                      >
                        AI interviewer
                      </div>

                      <div className="mt-1 text-xs text-slate-600">
                        Asking your next question
                      </div>

                    </div>

                  </div>


                  {/* Question */}

                  <div
                    className="
                      mt-8
                      rounded-2xl
                      border
                      border-white/[0.07]
                      bg-black/20
                      p-6
                    "
                  >

                    <div
                      className="
                        font-mono
                        text-[10px]
                        uppercase
                        tracking-[0.15em]
                        text-slate-600
                      "
                    >
                      Question 03 / 10
                    </div>

                    <p
                      className="
                        mt-4
                        font-display
                        text-xl
                        leading-8
                        text-slate-100
                      "
                    >
                      How would you design a
                      scalable API for a system
                      handling millions of requests?
                    </p>

                  </div>


                  {/* Waveform */}

                  <div className="mt-7">

                    <div
                      className="
                        mb-3
                        flex
                        items-center
                        justify-between
                      "
                    >

                      <span
                        className="
                          font-mono
                          text-[10px]
                          uppercase
                          tracking-[0.15em]
                          text-slate-600
                        "
                      >
                        Listening
                      </span>

                      <span className="text-xs text-emerald-400">
                        Your turn
                      </span>

                    </div>


                    <div className="flex h-12 items-center justify-center gap-1">

                      {[
                        18,
                        30,
                        42,
                        25,
                        36,
                        52,
                        28,
                        44,
                        32,
                        20,
                        39,
                        48,
                        27,
                        36,
                        22,
                        43,
                        31,
                        18,
                      ].map((height, index) => (
                        <div
                          key={index}
                          className="
                            w-1
                            rounded-full
                            bg-gradient-to-t
                            from-violet-500
                            to-cyan-300
                            opacity-80
                          "
                          style={{
                            height: `${height}%`,
                          }}
                        />
                      ))}

                    </div>

                  </div>


                  {/* Progress */}

                  <div className="mt-8">

                    <div className="mb-2 flex justify-between">

                      <span
                        className="
                          font-mono
                          text-[10px]
                          uppercase
                          tracking-[0.15em]
                          text-slate-600
                        "
                      >
                        Session progress
                      </span>

                      <span className="font-mono text-xs text-slate-400">
                        30%
                      </span>

                    </div>


                    <div className="h-1 overflow-hidden rounded-full bg-white/[0.06]">

                      <div
                        className="
                          h-full
                          w-[30%]
                          rounded-full
                          bg-gradient-to-r
                          from-violet-500
                          to-cyan-400
                        "
                      />

                    </div>

                  </div>

                </div>

              </div>

            </div>

          </div>

        </section>


        {/* ===================================================
            FEATURES
            =================================================== */}

        <section
          id="features"
          className="
            mx-auto
            max-w-7xl
            px-6
            pb-24
            lg:px-10
          "
        >

          <div className="mb-10">

            <div
              className="
                font-mono
                text-[10px]
                uppercase
                tracking-[0.2em]
                text-violet-400
              "
            >
              System capabilities
            </div>

            <h2
              className="
                mt-3
                font-display
                text-3xl
                font-semibold
                tracking-tight
                text-white
              "
            >
              More than a question generator.
            </h2>

          </div>


          <div className="grid gap-4 md:grid-cols-3">

            {[
              {
                number: "01",
                title: "Adaptive difficulty",
                description:
                  "Your performance determines what comes next. Strong answers push the interview forward.",
              },
              {
                number: "02",
                title: "AI evaluation",
                description:
                  "Every response is evaluated across technical accuracy, relevance, communication, and quality.",
              },
              {
                number: "03",
                title: "Actionable feedback",
                description:
                  "Finish with a structured report showing strengths, weaknesses, and where to improve.",
              },
            ].map((feature) => (

              <div
                key={feature.number}
                className="
                  glass-panel
                  group
                  rounded-2xl
                  p-6
                  transition-all
                  duration-300
                  hover:-translate-y-1
                  hover:border-violet-400/20
                  hover:shadow-glow
                "
              >

                <div
                  className="
                    font-mono
                    text-[10px]
                    tracking-[0.18em]
                    text-slate-600
                  "
                >
                  {feature.number}
                </div>

                <h3
                  className="
                    mt-8
                    font-display
                    text-lg
                    font-semibold
                    text-white
                  "
                >
                  {feature.title}
                </h3>

                <p
                  className="
                    mt-3
                    text-sm
                    leading-6
                    text-slate-500
                  "
                >
                  {feature.description}
                </p>

              </div>

            ))}

          </div>

        </section>

      </main>


      {/* ===================================================
          FOOTER
          =================================================== */}

      <footer
        className="
          relative
          z-10
          border-t
          border-white/[0.06]
          bg-black/10
        "
      >

        <div
          className="
            mx-auto
            max-w-7xl
            px-6
            py-10
            lg:px-10
          "
        >

          <div
            className="
              grid
              gap-10
              md:grid-cols-[1fr_auto]
              md:items-start
            "
          >

            {/* Brand */}

            <div>

              <div className="flex items-center gap-3">

                <div
                  className="
                    flex
                    h-9
                    w-9
                    items-center
                    justify-center
                    rounded-lg
                    border
                    border-violet-400/20
                    bg-violet-500/10
                  "
                >

                  <span
                    className="
                      font-display
                      text-xs
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
                    Intelligent Practice
                  </div>

                </div>

              </div>


              <p
                className="
                  mt-5
                  max-w-md
                  text-sm
                  leading-6
                  text-slate-600
                "
              >
                Practice technical interviews with an
                adaptive AI interviewer and turn every
                answer into an opportunity to improve.
              </p>

            </div>


            {/* Footer links */}

            <div
              className="
                grid
                grid-cols-2
                gap-12
                sm:grid-cols-3
              "
            >

              {/* Product */}

              <div>

                <div
                  className="
                    font-mono
                    text-[10px]
                    uppercase
                    tracking-[0.18em]
                    text-slate-600
                  "
                >
                  Product
                </div>


                <div className="mt-4 space-y-3">

                  <button
                    onClick={() => navigate("/register")}
                    className="
                      block
                      bg-transparent
                      p-0
                      text-sm
                      text-slate-500
                      hover:text-violet-300
                    "
                  >
                    Start interview
                  </button>


                  <button
                    onClick={() => navigate("/login")}
                    className="
                      block
                      bg-transparent
                      p-0
                      text-sm
                      text-slate-500
                      hover:text-violet-300
                    "
                  >
                    Sign in
                  </button>

                </div>

              </div>


              {/* Platform */}

              <div>

                <div
                  className="
                    font-mono
                    text-[10px]
                    uppercase
                    tracking-[0.18em]
                    text-slate-600
                  "
                >
                  Platform
                </div>


                <div className="mt-4 space-y-3">

                  <button
                    onClick={scrollToFeatures}
                    className="
                      block
                      bg-transparent
                      p-0
                      text-sm
                      text-slate-500
                      hover:text-violet-300
                    "
                  >
                    Features
                  </button>


                  <button
                    onClick={scrollToTop}
                    className="
                      block
                      bg-transparent
                      p-0
                      text-sm
                      text-slate-500
                      hover:text-violet-300
                    "
                  >
                    Back to top
                  </button>

                </div>

              </div>


              {/* Status */}

              <div>

                <div
                  className="
                    font-mono
                    text-[10px]
                    uppercase
                    tracking-[0.18em]
                    text-slate-600
                  "
                >
                  Status
                </div>


                <div
                  className="
                    mt-4
                    flex
                    items-center
                    gap-2
                  "
                >

                  <span
                    className="
                      h-1.5
                      w-1.5
                      rounded-full
                      bg-emerald-400
                      shadow-[0_0_10px_rgba(52,211,153,0.8)]
                    "
                  />

                  <span className="text-sm text-slate-500">
                    Systems operational
                  </span>

                </div>

              </div>

            </div>

          </div>


          {/* Bottom bar */}

          <div
            className="
              mt-10
              flex
              flex-col
              gap-3
              border-t
              border-white/[0.05]
              pt-6
              sm:flex-row
              sm:items-center
              sm:justify-between
            "
          >

            <div
              className="
                font-mono
                text-[10px]
                uppercase
                tracking-[0.15em]
                text-slate-700
              "
            >
              © 2026 AI Mock Interview
            </div>


            <div
              className="
                font-mono
                text-[10px]
                uppercase
                tracking-[0.15em]
                text-slate-700
              "
            >
              Built for better interviews
            </div>

          </div>

        </div>

      </footer>

    </div>
  );
}