import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

interface CurrentUser {
  id: number;
  full_name: string;
  email: string;
  role: "user" | "admin";
  is_active: boolean;
}

interface StatCardProps {
  label: string;
  value: string;
  description: string;
}

function StatCard({
  label,
  value,
  description,
}: StatCardProps) {
  return (
    <div
      className="
        rounded-2xl
        border
        border-white/[0.06]
        bg-white/[0.025]
        p-5
        transition-all
        duration-300
        hover:border-white/[0.12]
        hover:bg-white/[0.04]
      "
    >
      <div
        className="
          font-mono
          text-[10px]
          uppercase
          tracking-[0.16em]
          text-slate-600
        "
      >
        {label}
      </div>

      <div
        className="
          mt-3
          font-display
          text-3xl
          font-semibold
          tracking-tight
          text-white
        "
      >
        {value}
      </div>

      <div className="mt-1 text-xs text-slate-600">
        {description}
      </div>
    </div>
  );
}

export default function Home() {
  const navigate = useNavigate();

  const [user, setUser] = useState<CurrentUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");
    const storedUser = localStorage.getItem("user");

    if (!storedToken || !storedUser) {
      navigate("/login", { replace: true });
      return;
    }

    try {
      const parsedUser: CurrentUser = JSON.parse(
        storedUser
      );

      if (parsedUser.role === "admin") {
        navigate("/admin", { replace: true });
        return;
      }

      setUser(parsedUser);
    } catch {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");

      navigate("/login", { replace: true });
      return;
    }

    setIsLoading(false);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    navigate("/login", {
      replace: true,
    });
  };

  if (isLoading) {
    return (
      <div
        className="
          app-background
          flex
          min-h-screen
          items-center
          justify-center
        "
      >
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
              text-slate-600
            "
          >
            Loading workspace
          </p>

        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const firstName =
    user.full_name.trim().split(" ")[0];

  return (
    <div className="app-background min-h-screen">

      {/* =====================================================
          AMBIENT BACKGROUND
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
          top-[320px]
          animate-pulse-slow
        "
      />


      {/* =====================================================
          NAVIGATION
          ===================================================== */}

      <header
        className="
          relative
          z-20
          border-b
          border-white/[0.06]
          bg-black/10
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

          {/* Brand */}

          <button
            onClick={() => navigate("/home")}
            className="
              flex
              items-center
              gap-3
              text-left
            "
            aria-label="Go to home"
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
                  tracking-[0.2em]
                  text-slate-600
                "
              >
                Candidate workspace
              </div>

            </div>

          </button>


          {/* User controls */}

          <div className="flex items-center gap-4">

            <div className="hidden text-right sm:block">

              <div className="text-sm font-medium text-slate-200">
                {user.full_name}
              </div>

              <div
                className="
                  font-mono
                  text-[9px]
                  uppercase
                  tracking-[0.16em]
                  text-slate-600
                "
              >
                Candidate
              </div>

            </div>


            <div
              className="
                hidden
                h-9
                w-px
                bg-white/[0.08]
                sm:block
              "
            />


            <button
              onClick={handleLogout}
              className="
                rounded-lg
                border
                border-white/10
                bg-white/[0.025]
                px-4
                py-2
                text-sm
                font-medium
                text-slate-400
                transition
                hover:border-red-400/20
                hover:bg-red-400/[0.04]
                hover:text-red-300
              "
            >
              Logout
            </button>

          </div>

        </div>

      </header>


      {/* =====================================================
          MAIN CONTENT
          ===================================================== */}

      <main
        className="
          relative
          z-10
          mx-auto
          max-w-7xl
          px-6
          py-10
          lg:px-10
          lg:py-14
        "
      >

        {/* ===================================================
            GREETING
            =================================================== */}

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
            Candidate workspace
          </div>


          <div
            className="
              mt-3
              flex
              flex-col
              justify-between
              gap-5
              lg:flex-row
              lg:items-end
            "
          >

            <div>

              <h1
                className="
                  font-display
                  text-4xl
                  font-semibold
                  leading-tight
                  tracking-[-0.035em]
                  text-white
                  sm:text-5xl
                "
              >
                Good to see you,{" "}
                <span
                  className="
                    bg-gradient-to-r
                    from-violet-300
                    to-cyan-300
                    bg-clip-text
                    text-transparent
                  "
                >
                  {firstName}.
                </span>
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
                Ready for your next challenge?
                Practice under realistic interview
                conditions and turn your answers into
                measurable progress.
              </p>

            </div>


            {/* System status */}

            <div
              className="
                flex
                w-fit
                items-center
                gap-2
                rounded-full
                border
                border-emerald-400/10
                bg-emerald-400/[0.035]
                px-3
                py-2
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

              <span
                className="
                  font-mono
                  text-[10px]
                  uppercase
                  tracking-[0.14em]
                  text-emerald-400/80
                "
              >
                Interview engine ready
              </span>

            </div>

          </div>

        </section>


        {/* ===================================================
            PRIMARY ACTION + PERFORMANCE
            =================================================== */}

        <section
          className="
            grid
            gap-5
            lg:grid-cols-[1.4fr_1fr]
          "
        >

          {/* Start interview */}

          <div
            className="
              group
              relative
              overflow-hidden
              rounded-3xl
              border
              border-violet-400/15
              bg-gradient-to-br
              from-violet-500/[0.13]
              via-white/[0.035]
              to-cyan-400/[0.04]
              p-8
              shadow-glow
              transition-all
              duration-500
              hover:border-violet-400/25
            "
          >

            {/* Ambient glow */}

            <div
              className="
                absolute
                right-[-100px]
                top-[-100px]
                h-72
                w-72
                rounded-full
                bg-violet-500/[0.08]
                blur-3xl
                transition-transform
                duration-700
                group-hover:scale-125
              "
            />


            <div className="relative">

              <div
                className="
                  inline-flex
                  items-center
                  gap-2
                  rounded-full
                  border
                  border-white/[0.08]
                  bg-black/10
                  px-3
                  py-1.5
                "
              >

                <span
                  className="
                    h-1.5
                    w-1.5
                    rounded-full
                    bg-violet-400
                    shadow-[0_0_10px_rgba(167,139,250,0.8)]
                  "
                />

                <span
                  className="
                    font-mono
                    text-[9px]
                    uppercase
                    tracking-[0.16em]
                    text-violet-300/80
                  "
                >
                  New session
                </span>

              </div>


              <h2
                className="
                  mt-7
                  max-w-xl
                  font-display
                  text-3xl
                  font-semibold
                  leading-tight
                  tracking-tight
                  text-white
                  sm:text-4xl
                "
              >
                Put your technical
                skills under pressure.
              </h2>


              <p
                className="
                  mt-4
                  max-w-lg
                  text-sm
                  leading-6
                  text-slate-400
                "
              >
                Choose a topic and starting difficulty.
                The AI interviewer will adapt the
                conversation based on how you perform.
              </p>


              <button
                onClick={() =>
                  navigate("/interviews/new")
                }
                className="
                  group/button
                  mt-8
                  inline-flex
                  items-center
                  gap-3
                  rounded-xl
                  bg-white
                  px-6
                  py-3.5
                  font-display
                  text-sm
                  font-semibold
                  text-slate-950
                  transition-all
                  duration-300
                  hover:-translate-y-0.5
                  hover:shadow-[0_15px_45px_rgba(139,92,246,0.25)]
                  active:translate-y-0
                "
              >

                Start new interview

                <span
                  className="
                    transition-transform
                    duration-300
                    group-hover/button:translate-x-1
                  "
                >
                  →
                </span>

              </button>


              {/* Interview metadata */}

              <div
                className="
                  mt-8
                  flex
                  flex-wrap
                  gap-x-7
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
                      text-[9px]
                      uppercase
                      tracking-[0.15em]
                      text-slate-600
                    "
                  >
                    Difficulty
                  </div>

                  <div className="mt-1 text-xs text-slate-300">
                    Adaptive
                  </div>

                </div>


                <div>

                  <div
                    className="
                      font-mono
                      text-[9px]
                      uppercase
                      tracking-[0.15em]
                      text-slate-600
                    "
                  >
                    Evaluation
                  </div>

                  <div className="mt-1 text-xs text-slate-300">
                    AI-powered
                  </div>

                </div>


                <div>

                  <div
                    className="
                      font-mono
                      text-[9px]
                      uppercase
                      tracking-[0.15em]
                      text-slate-600
                    "
                  >
                    Feedback
                  </div>

                  <div className="mt-1 text-xs text-slate-300">
                    Instant
                  </div>

                </div>

              </div>

            </div>

          </div>


          {/* Performance */}

          <div
            className="
              glass-panel
              rounded-3xl
              p-7
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
              Your performance
            </div>


            <div className="mt-7">

              <div
                className="
                  font-display
                  text-5xl
                  font-semibold
                  tracking-tight
                  text-white
                "
              >
                —
              </div>

              <div className="mt-2 text-sm text-slate-500">
                Average interview score
              </div>

            </div>


            <div className="mt-8 grid grid-cols-2 gap-3">

              <StatCard
                label="Completed"
                value="0"
                description="Finished sessions"
              />

              <StatCard
                label="In progress"
                value="0"
                description="Active sessions"
              />

            </div>

          </div>

        </section>


        {/* ===================================================
            QUICK ACTIONS
            =================================================== */}

        <section className="mt-8">

          <div
            className="
              mb-4
              font-mono
              text-[10px]
              uppercase
              tracking-[0.18em]
              text-slate-600
            "
          >
            Quick actions
          </div>


          <div className="grid gap-4 sm:grid-cols-2">

            {/* Performance */}

            <button
              onClick={() => navigate("/dashboard")}
              className="
                group
                rounded-2xl
                border
                border-white/[0.06]
                bg-white/[0.02]
                p-5
                text-left
                transition-all
                duration-300
                hover:-translate-y-0.5
                hover:border-violet-400/20
                hover:bg-white/[0.035]
              "
            >

              <div className="flex items-center justify-between">

                <div
                  className="
                    flex
                    h-10
                    w-10
                    items-center
                    justify-center
                    rounded-xl
                    border
                    border-violet-400/10
                    bg-violet-500/[0.06]
                  "
                >

                  <span className="font-mono text-xs text-violet-300">
                    ↗
                  </span>

                </div>


                <span
                  className="
                    text-slate-700
                    transition-transform
                    duration-300
                    group-hover:translate-x-1
                  "
                >
                  →
                </span>

              </div>


              <h3 className="mt-5 font-display text-base font-semibold text-white">
                Performance dashboard
              </h3>

              <p className="mt-2 text-xs leading-5 text-slate-600">
                Review your scores, progress, and
                interview history.
              </p>

            </button>


            {/* Profile */}

            <button
              className="
                group
                rounded-2xl
                border
                border-white/[0.06]
                bg-white/[0.02]
                p-5
                text-left
                transition-all
                duration-300
                hover:-translate-y-0.5
                hover:border-cyan-400/20
                hover:bg-white/[0.035]
              "
            >

              <div className="flex items-center justify-between">

                <div
                  className="
                    flex
                    h-10
                    w-10
                    items-center
                    justify-center
                    rounded-xl
                    border
                    border-cyan-400/10
                    bg-cyan-400/[0.05]
                  "
                >

                  <span className="font-mono text-xs text-cyan-300">
                    ID
                  </span>

                </div>


                <span
                  className="
                    text-slate-700
                    transition-transform
                    duration-300
                    group-hover:translate-x-1
                  "
                >
                  →
                </span>

              </div>


              <h3 className="mt-5 font-display text-base font-semibold text-white">
                Your profile
              </h3>

              <p className="mt-2 text-xs leading-5 text-slate-600">
                Manage your account information and
                preferences.
              </p>

            </button>

          </div>

        </section>


        {/* ===================================================
            INTERVIEW HISTORY
            =================================================== */}

        <section className="mt-8">

          <div
            className="
              glass-panel
              overflow-hidden
              rounded-3xl
            "
          >

            {/* Header */}

            <div
              className="
                flex
                flex-col
                gap-4
                border-b
                border-white/[0.06]
                p-7
                sm:flex-row
                sm:items-center
                sm:justify-between
              "
            >

              <div>

                <div
                  className="
                    font-mono
                    text-[10px]
                    uppercase
                    tracking-[0.18em]
                    text-violet-400
                  "
                >
                  Interview history
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
                  Recent interviews
                </h2>

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
                0 sessions
              </div>

            </div>


            {/* Empty state */}

            <div className="p-7">

              <div
                className="
                  flex
                  min-h-56
                  items-center
                  justify-center
                  rounded-2xl
                  border
                  border-dashed
                  border-white/[0.08]
                  bg-white/[0.012]
                "
              >

                <div className="max-w-sm text-center">

                  <div
                    className="
                      mx-auto
                      flex
                      h-14
                      w-14
                      items-center
                      justify-center
                      rounded-2xl
                      border
                      border-white/[0.07]
                      bg-white/[0.025]
                    "
                  >

                    <span
                      className="
                        font-mono
                        text-xs
                        tracking-widest
                        text-slate-600
                      "
                    >
                      01
                    </span>

                  </div>


                  <h3
                    className="
                      mt-5
                      font-display
                      text-base
                      font-semibold
                      text-slate-300
                    "
                  >
                    Your interview history is empty.
                  </h3>


                  <p
                    className="
                      mt-2
                      text-xs
                      leading-5
                      text-slate-600
                    "
                  >
                    Complete your first interview to
                    start tracking your technical
                    performance and growth.
                  </p>


                  <button
                    onClick={() =>
                      navigate("/interviews/new")
                    }
                    className="
                      mt-5
                      rounded-lg
                      border
                      border-violet-400/20
                      bg-violet-500/[0.07]
                      px-4
                      py-2.5
                      font-mono
                      text-[10px]
                      uppercase
                      tracking-[0.12em]
                      text-violet-300
                      transition
                      hover:bg-violet-500/[0.12]
                    "
                  >
                    Start your first interview
                  </button>

                </div>

              </div>

            </div>

          </div>

        </section>


        {/* ===================================================
            FOOTER
            =================================================== */}

        <footer
          className="
            mt-12
            border-t
            border-white/[0.05]
            py-7
          "
        >

          <div
            className="
              flex
              flex-col
              gap-2
              sm:flex-row
              sm:items-center
              sm:justify-between
            "
          >

            <div
              className="
                font-mono
                text-[9px]
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
                text-[9px]
                uppercase
                tracking-[0.15em]
                text-slate-700
              "
            >
              Intelligent practice · Better interviews
            </div>

          </div>

        </footer>

      </main>

    </div>
  );
}