import { useNavigate } from "react-router-dom";

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen overflow-hidden bg-[#070914] text-white">
      {/* =====================================================
          AMBIENT BACKGROUND
      ====================================================== */}

      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute left-[-180px] top-[-180px] h-[500px] w-[500px] rounded-full bg-violet-600/10 blur-[140px]" />

        <div className="absolute right-[-160px] top-[180px] h-[500px] w-[500px] rounded-full bg-cyan-500/10 blur-[150px]" />

        <div className="absolute bottom-[-250px] left-[35%] h-[500px] w-[500px] rounded-full bg-purple-600/10 blur-[150px]" />

        <div
          className="absolute inset-0 opacity-[0.035]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px)",
            backgroundSize: "48px 48px",
          }}
        />
      </div>

      {/* =====================================================
          NAVBAR
      ====================================================== */}

      <header className="relative z-10 border-b border-white/[0.06]">
        <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-6 lg:px-8">
          {/* Logo */}
          <button
            type="button"
            onClick={() => navigate("/")}
            className="group flex items-center gap-3"
            aria-label="Go to home"
          >
            <div className="relative flex h-9 w-9 items-center justify-center rounded-xl border border-violet-400/30 bg-violet-500/10">
              <div className="h-2.5 w-2.5 animate-pulse rounded-full bg-violet-300 shadow-[0_0_16px_rgba(196,181,253,0.9)]" />
            </div>

            <div className="text-left">
              <div className="text-sm font-semibold tracking-wide">
                AI Mock Interview
              </div>

              <div className="text-[9px] uppercase tracking-[0.25em] text-slate-500">
                Interview Lab
              </div>
            </div>
          </button>

          {/* Navigation */}
          <nav className="hidden items-center gap-8 md:flex">
            <a
              href="#how-it-works"
              className="text-sm text-slate-400 transition hover:text-white"
            >
              How it works
            </a>

            <a
              href="#features"
              className="text-sm text-slate-400 transition hover:text-white"
            >
              Features
            </a>
          </nav>

          {/* Auth */}
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => navigate("/login")}
              className="rounded-lg px-4 py-2 text-sm font-medium text-slate-300 transition hover:bg-white/[0.05] hover:text-white"
            >
              Sign in
            </button>

            <button
              type="button"
              onClick={() => navigate("/register")}
              className="rounded-lg border border-violet-400/30 bg-violet-500/10 px-4 py-2 text-sm font-semibold text-violet-200 transition hover:border-violet-300/50 hover:bg-violet-500/20"
            >
              Get started
            </button>
          </div>
        </div>
      </header>

      {/* =====================================================
          HERO
      ====================================================== */}

      <main className="relative z-10">
        <section className="mx-auto max-w-7xl px-6 pb-28 pt-20 lg:px-8 lg:pb-36 lg:pt-28">
          <div className="grid items-center gap-16 lg:grid-cols-[1.05fr_0.95fr]">
            {/* Hero copy */}
            <div>
              {/* Eyebrow */}
              <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-violet-400/20 bg-violet-500/[0.07] px-4 py-2">
                <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />

                <span className="text-[10px] font-semibold uppercase tracking-[0.22em] text-violet-200">
                  AI-powered interview practice
                </span>
              </div>

              <h1 className="max-w-4xl text-5xl font-semibold leading-[1.03] tracking-[-0.04em] text-white sm:text-6xl lg:text-7xl">
                Practice like you're
                <span className="block bg-gradient-to-r from-violet-200 via-purple-300 to-cyan-300 bg-clip-text text-transparent">
                  already in the room.
                </span>
              </h1>

              <p className="mt-7 max-w-2xl text-base leading-8 text-slate-400 sm:text-lg">
                Prepare for technical interviews with an AI interviewer that
                asks questions, evaluates your answers, adapts the difficulty,
                and gives you actionable feedback.
              </p>

              {/* CTA */}
              <div className="mt-9 flex flex-col gap-3 sm:flex-row">
                <button
                  type="button"
                  onClick={() => navigate("/register")}
                  className="group inline-flex items-center justify-center gap-3 rounded-xl bg-violet-400 px-6 py-3.5 text-sm font-bold text-[#100b1d] shadow-[0_0_30px_rgba(167,139,250,0.15)] transition duration-200 hover:-translate-y-0.5 hover:bg-violet-300 hover:shadow-[0_0_40px_rgba(167,139,250,0.25)] active:translate-y-0"
                >
                  Start practicing

                  <span className="transition-transform duration-200 group-hover:translate-x-1">
                    →
                  </span>
                </button>

                <button
                  type="button"
                  onClick={() => navigate("/login")}
                  className="inline-flex items-center justify-center rounded-xl border border-white/10 bg-white/[0.025] px-6 py-3.5 text-sm font-semibold text-slate-200 transition hover:border-white/20 hover:bg-white/[0.06]"
                >
                  I already have an account
                </button>
              </div>
            </div>

            {/* =================================================
                AI INTERVIEW VISUAL
            ================================================== */}

            <div className="relative mx-auto w-full max-w-xl">
              {/* Glow */}
              <div className="absolute inset-10 rounded-full bg-violet-500/10 blur-[90px]" />

              {/* Main card */}
              <div className="relative rounded-3xl border border-white/[0.08] bg-white/[0.025] p-5 shadow-2xl backdrop-blur-xl">
                {/* Top bar */}
                <div className="flex items-center justify-between border-b border-white/[0.06] pb-4">
                  <div>
                    <div className="text-[9px] uppercase tracking-[0.25em] text-violet-300">
                      Live interview
                    </div>

                    <div className="mt-1 text-sm font-semibold">
                      Python · Technical
                    </div>
                  </div>

                  <div className="flex items-center gap-2 rounded-full border border-emerald-400/10 bg-emerald-400/[0.05] px-3 py-1.5">
                    <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
                    <span className="text-[10px] text-emerald-300">
                      AI online
                    </span>
                  </div>
                </div>

                {/* AI Orb */}
                <div className="relative flex h-64 items-center justify-center">
                  <div className="absolute h-48 w-48 animate-[spin_18s_linear_infinite] rounded-full border border-violet-400/10" />

                  <div className="absolute h-36 w-36 rounded-full border border-violet-300/10" />

                  <div className="absolute h-28 w-28 animate-pulse rounded-full bg-violet-500/10 blur-2xl" />

                  <div className="relative flex h-24 w-24 items-center justify-center rounded-full border border-violet-300/30 bg-[#111326] shadow-[0_0_60px_rgba(167,139,250,0.2)]">
                    <div className="h-4 w-4 animate-pulse rounded-full bg-violet-200 shadow-[0_0_22px_rgba(196,181,253,1)]" />
                  </div>
                </div>

                {/* Question */}
                <div className="rounded-2xl border border-white/[0.06] bg-black/20 p-5">
                  <div className="mb-3 flex items-center justify-between">
                    <span className="text-[9px] uppercase tracking-[0.2em] text-slate-600">
                      Question 03
                    </span>

                    <span className="rounded-full border border-violet-300/20 bg-violet-400/5 px-2.5 py-1 text-[9px] uppercase tracking-wider text-violet-300">
                      Medium
                    </span>
                  </div>

                  <p className="text-base font-medium leading-7 text-slate-100">
                    Explain the difference between a list and a tuple in
                    Python.
                  </p>

                  {/* Fake waveform */}
                  <div className="mt-5 flex h-8 items-center gap-1">
                    {[18, 28, 12, 24, 35, 17, 29, 40, 22, 31, 16, 27, 20, 34].map(
                      (height, index) => (
                        <span
                          key={index}
                          className="w-1 rounded-full bg-violet-300/50"
                          style={{
                            height: `${height}%`,
                            animationDelay: `${index * 80}ms`,
                          }}
                        />
                      ),
                    )}
                  </div>
                </div>

                {/* Bottom status */}
                <div className="mt-4 flex items-center justify-between px-1">
                  <span className="text-[10px] text-slate-600">
                    AI is evaluating your response
                  </span>

                  <span className="text-[10px] font-medium text-violet-300">
                    75 / 100
                  </span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* =====================================================
            STATS STRIP
        ====================================================== */}

        <section className="border-y border-white/[0.06] bg-white/[0.015]">
          <div className="mx-auto grid max-w-7xl grid-cols-2 divide-x divide-white/[0.06] px-6 lg:grid-cols-4 lg:px-8">
            <div className="px-5 py-8 text-center">
              <div className="text-2xl font-semibold">3</div>
              <div className="mt-1 text-xs text-slate-500">
                Difficulty levels
              </div>
            </div>

            <div className="px-5 py-8 text-center">
              <div className="text-2xl font-semibold">AI</div>
              <div className="mt-1 text-xs text-slate-500">
                Answer evaluation
              </div>
            </div>

            <div className="px-5 py-8 text-center">
              <div className="text-2xl font-semibold">4</div>
              <div className="mt-1 text-xs text-slate-500">
                Evaluation metrics
              </div>
            </div>

            <div className="px-5 py-8 text-center">
              <div className="text-2xl font-semibold">∞</div>
              <div className="mt-1 text-xs text-slate-500">
                Practice sessions
              </div>
            </div>
          </div>
        </section>

        {/* =====================================================
            FEATURES
        ====================================================== */}

        <section
          id="features"
          className="mx-auto max-w-7xl px-6 py-28 lg:px-8"
        >
          <div className="max-w-2xl">
            <div className="text-[10px] font-semibold uppercase tracking-[0.25em] text-violet-300">
              Built for better interviews
            </div>

            <h2 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
              Not just questions.
              <span className="text-slate-500"> Real preparation.</span>
            </h2>

            <p className="mt-5 leading-7 text-slate-400">
              Every interview session is designed to help you understand what
              you know, where you struggle, and what you should improve.
            </p>
          </div>

          <div className="mt-14 grid gap-5 md:grid-cols-3">
            {/* Feature 1 */}
            <div className="group rounded-2xl border border-white/[0.07] bg-white/[0.025] p-7 transition duration-300 hover:-translate-y-1 hover:border-violet-300/20 hover:bg-white/[0.04]">
              <div className="mb-8 flex h-11 w-11 items-center justify-center rounded-xl border border-violet-300/20 bg-violet-400/10 text-violet-200">
                01
              </div>

              <h3 className="text-lg font-semibold">
                Adaptive interviews
              </h3>

              <p className="mt-3 text-sm leading-7 text-slate-500">
                Strong answers can increase the difficulty while weaker
                performance can bring the interview back to fundamentals.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="group rounded-2xl border border-white/[0.07] bg-white/[0.025] p-7 transition duration-300 hover:-translate-y-1 hover:border-cyan-300/20 hover:bg-white/[0.04]">
              <div className="mb-8 flex h-11 w-11 items-center justify-center rounded-xl border border-cyan-300/20 bg-cyan-400/10 text-cyan-200">
                02
              </div>

              <h3 className="text-lg font-semibold">
                Semantic AI evaluation
              </h3>

              <p className="mt-3 text-sm leading-7 text-slate-500">
                Your answer is evaluated for technical correctness, relevance,
                communication, completeness, and practical understanding.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="group rounded-2xl border border-white/[0.07] bg-white/[0.025] p-7 transition duration-300 hover:-translate-y-1 hover:border-purple-300/20 hover:bg-white/[0.04]">
              <div className="mb-8 flex h-11 w-11 items-center justify-center rounded-xl border border-purple-300/20 bg-purple-400/10 text-purple-200">
                03
              </div>

              <h3 className="text-lg font-semibold">
                Actionable feedback
              </h3>

              <p className="mt-3 text-sm leading-7 text-slate-500">
                Receive scores, strengths, weaknesses, feedback, and
                recommendations after your answers and at the end of the
                interview.
              </p>
            </div>
          </div>
        </section>

        {/* =====================================================
            HOW IT WORKS
        ====================================================== */}

        <section
          id="how-it-works"
          className="border-y border-white/[0.06] bg-white/[0.015]"
        >
          <div className="mx-auto max-w-7xl px-6 py-28 lg:px-8">
            <div className="text-center">
              <div className="text-[10px] font-semibold uppercase tracking-[0.25em] text-violet-300">
                The process
              </div>

              <h2 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
                From setup to feedback
              </h2>
            </div>

            <div className="mt-16 grid gap-10 md:grid-cols-4">
              {[
                {
                  number: "01",
                  title: "Choose a topic",
                  text: "Select the technical topic you want to practice.",
                },
                {
                  number: "02",
                  title: "Pick difficulty",
                  text: "Start with easy, medium, or hard questions.",
                },
                {
                  number: "03",
                  title: "Answer",
                  text: "Respond to questions as you would in a real interview.",
                },
                {
                  number: "04",
                  title: "Improve",
                  text: "Review AI feedback and use it to improve your next attempt.",
                },
              ].map((step) => (
                <div key={step.number} className="relative">
                  <div className="text-xs font-semibold tracking-[0.2em] text-violet-300">
                    {step.number}
                  </div>

                  <h3 className="mt-4 text-lg font-semibold">
                    {step.title}
                  </h3>

                  <p className="mt-3 text-sm leading-7 text-slate-500">
                    {step.text}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* =====================================================
            FINAL CTA
        ====================================================== */}

        <section className="mx-auto max-w-7xl px-6 py-28 lg:px-8">
          <div className="relative overflow-hidden rounded-3xl border border-violet-300/10 bg-gradient-to-br from-violet-500/[0.09] via-white/[0.025] to-cyan-500/[0.05] p-10 text-center sm:p-16">
            <div className="pointer-events-none absolute left-1/2 top-1/2 h-64 w-64 -translate-x-1/2 -translate-y-1/2 rounded-full bg-violet-500/10 blur-[100px]" />

            <div className="relative">
              <div className="text-[10px] font-semibold uppercase tracking-[0.25em] text-violet-300">
                Your next interview starts here
              </div>

              <h2 className="mx-auto mt-5 max-w-2xl text-3xl font-semibold tracking-tight sm:text-5xl">
                Turn interview anxiety into interview confidence.
              </h2>

              <p className="mx-auto mt-5 max-w-xl text-sm leading-7 text-slate-400">
                Practice technical questions, understand your weaknesses, and
                walk into your next interview better prepared.
              </p>

              <button
                type="button"
                onClick={() => navigate("/register")}
                className="group mt-8 inline-flex items-center gap-3 rounded-xl bg-white px-7 py-3.5 text-sm font-bold text-[#0b0c16] transition hover:-translate-y-0.5 hover:bg-violet-100 active:translate-y-0"
              >
                Create your account

                <span className="transition-transform group-hover:translate-x-1">
                  →
                </span>
              </button>
            </div>
          </div>
        </section>
      </main>

      {/* =====================================================
          FOOTER
      ====================================================== */}

      <footer className="border-t border-white/[0.06]">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-8 sm:flex-row sm:items-center sm:justify-between lg:px-8">
          <div>
            <div className="text-sm font-semibold">
              AI Mock Interview
            </div>

            <div className="mt-1 text-xs text-slate-600">
              Practice. Improve. Succeed.
            </div>
          </div>

          <div className="text-xs text-slate-600">
            © {new Date().getFullYear()} AI Mock Interview
          </div>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;