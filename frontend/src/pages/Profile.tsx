import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getInterviews,
  type Interview,
} from "../lib/api";


interface CurrentUser {
  id: number;
  full_name: string;
  email: string;
  role: "user" | "admin";
  is_active: boolean;
}


export default function Profile() {
  const navigate = useNavigate();

  const [user, setUser] =
    useState<CurrentUser | null>(null);

  const [interviews, setInterviews] =
    useState<Interview[]>([]);

  const [isLoading, setIsLoading] =
    useState(true);


  useEffect(() => {
    async function loadProfile() {
      const storedToken =
        localStorage.getItem("access_token");

      const storedUser =
        localStorage.getItem("user");


      if (!storedToken || !storedUser) {
        navigate("/login", {
          replace: true,
        });

        return;
      }


      try {
        const parsedUser: CurrentUser =
          JSON.parse(storedUser);

        setUser(parsedUser);


        const interviewData =
          await getInterviews();

        setInterviews(interviewData);

      } catch {
        localStorage.removeItem(
          "access_token",
        );

        localStorage.removeItem("user");

        navigate("/login", {
          replace: true,
        });

        return;
      } finally {
        setIsLoading(false);
      }
    }


    loadProfile();
  }, [navigate]);


  const handleLogout = () => {
    localStorage.removeItem(
      "access_token",
    );

    localStorage.removeItem("user");

    navigate("/login", {
      replace: true,
    });
  };


  if (isLoading) {
    return (
      <div className="app-background min-h-screen">
        <div className="app-grid" />

        <div className="flex min-h-screen items-center justify-center">
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
              Loading profile
            </p>

          </div>
        </div>
      </div>
    );
  }


  if (!user) {
    return null;
  }


  const completedInterviews =
    interviews.filter(
      (interview) =>
        interview.status === "completed",
    );


  const inProgressInterviews =
    interviews.filter(
      (interview) =>
        interview.status === "in_progress",
    );


  const scores =
    completedInterviews
      .map(
        (interview) =>
          interview.overall_score,
      )
      .filter(
        (
          score,
        ): score is number =>
          score !== null,
      );


  const averageScore =
    scores.length > 0
      ? scores.reduce(
          (sum, score) =>
            sum + score,
          0,
        ) / scores.length
      : null;


  const bestScore =
    scores.length > 0
      ? Math.max(...scores)
      : null;


  const initials =
    user.full_name
      .trim()
      .split(/\s+/)
      .map(
        (name) =>
          name.charAt(0),
      )
      .slice(0, 2)
      .join("")
      .toUpperCase();


  return (
    <div className="app-background min-h-screen">

      {/* =====================================================
          BACKGROUND
      ====================================================== */}

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
      ====================================================== */}

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

          <button
            onClick={() =>
              navigate("/home")
            }
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
                Candidate workspace
              </div>

            </div>

          </button>


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

      </header>


      {/* =====================================================
          MAIN
      ====================================================== */}

      <main
        className="
          relative
          z-10
          mx-auto
          max-w-5xl
          px-6
          py-10
          lg:px-10
          lg:py-14
        "
      >

        {/* Back */}

        <button
          onClick={() =>
            navigate("/home")
          }
          className="
            mb-8
            font-mono
            text-[10px]
            uppercase
            tracking-[0.14em]
            text-slate-600
            transition
            hover:text-slate-300
          "
        >
          ← Back to home
        </button>


        {/* =================================================
            TITLE
        ================================================== */}

        <section className="mb-10">

          <div
            className="
              font-mono
              text-[10px]
              uppercase
              tracking-[0.2em]
              text-cyan-400
            "
          >
            Account
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
            Your profile
          </h1>

          <p
            className="
              mt-4
              max-w-2xl
              text-sm
              leading-7
              text-slate-500
            "
          >
            Manage your account information
            and review your interview
            activity.
          </p>

        </section>


        {/* =================================================
            PROFILE CARD
        ================================================== */}

        <section
          className="
            glass-panel
            rounded-3xl
            p-7
            sm:p-9
          "
        >

          <div
            className="
              flex
              flex-col
              gap-6
              sm:flex-row
              sm:items-center
            "
          >

            {/* Avatar */}

            <div
              className="
                flex
                h-20
                w-20
                shrink-0
                items-center
                justify-center
                rounded-2xl
                border
                border-violet-400/20
                bg-violet-500/[0.08]
                shadow-glow
              "
            >
              <span
                className="
                  font-display
                  text-xl
                  font-semibold
                  text-violet-300
                "
              >
                {initials}
              </span>
            </div>


            <div className="flex-1">

              <div
                className="
                  font-mono
                  text-[9px]
                  uppercase
                  tracking-[0.16em]
                  text-violet-400
                "
              >
                Candidate profile
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
                {user.full_name}
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                {user.email}
              </p>

            </div>


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
                "
              />

              <span
                className="
                  font-mono
                  text-[9px]
                  uppercase
                  tracking-[0.14em]
                  text-emerald-400/80
                "
              >
                {user.is_active
                  ? "Active account"
                  : "Inactive account"}
              </span>

            </div>

          </div>

        </section>


        {/* =================================================
            ACCOUNT INFORMATION
        ================================================== */}

        <section className="mt-6">

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
            Account information
          </div>


          <div
            className="
              grid
              gap-4
              sm:grid-cols-2
            "
          >

            <div
              className="
                rounded-2xl
                border
                border-white/[0.06]
                bg-white/[0.02]
                p-6
              "
            >

              <div
                className="
                  font-mono
                  text-[9px]
                  uppercase
                  tracking-[0.14em]
                  text-slate-600
                "
              >
                Full name
              </div>

              <div
                className="
                  mt-3
                  text-sm
                  font-medium
                  text-slate-200
                "
              >
                {user.full_name}
              </div>

            </div>


            <div
              className="
                rounded-2xl
                border
                border-white/[0.06]
                bg-white/[0.02]
                p-6
              "
            >

              <div
                className="
                  font-mono
                  text-[9px]
                  uppercase
                  tracking-[0.14em]
                  text-slate-600
                "
              >
                Email address
              </div>

              <div
                className="
                  mt-3
                  break-all
                  text-sm
                  font-medium
                  text-slate-200
                "
              >
                {user.email}
              </div>

            </div>


            <div
              className="
                rounded-2xl
                border
                border-white/[0.06]
                bg-white/[0.02]
                p-6
              "
            >

              <div
                className="
                  font-mono
                  text-[9px]
                  uppercase
                  tracking-[0.14em]
                  text-slate-600
                "
              >
                User ID
              </div>

              <div
                className="
                  mt-3
                  font-mono
                  text-sm
                  font-medium
                  text-slate-200
                "
              >
                #{user.id}
              </div>

            </div>


            <div
              className="
                rounded-2xl
                border
                border-white/[0.06]
                bg-white/[0.02]
                p-6
              "
            >

              <div
                className="
                  font-mono
                  text-[9px]
                  uppercase
                  tracking-[0.14em]
                  text-slate-600
                "
              >
                Account role
              </div>

              <div
                className="
                  mt-3
                  text-sm
                  font-medium
                  capitalize
                  text-slate-200
                "
              >
                {user.role}
              </div>

            </div>

          </div>

        </section>


        {/* =================================================
            INTERVIEW STATISTICS
        ================================================== */}

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
            Interview activity
          </div>


          <div
            className="
              grid
              gap-4
              sm:grid-cols-2
              lg:grid-cols-4
            "
          >

            <div
              className="
                rounded-2xl
                border
                border-white/[0.06]
                bg-white/[0.02]
                p-5
              "
            >

              <div className="text-xs text-slate-600">
                Total interviews
              </div>

              <div
                className="
                  mt-3
                  font-display
                  text-3xl
                  font-semibold
                  text-white
                "
              >
                {interviews.length}
              </div>

            </div>


            <div
              className="
                rounded-2xl
                border
                border-white/[0.06]
                bg-white/[0.02]
                p-5
              "
            >

              <div className="text-xs text-slate-600">
                Completed
              </div>

              <div
                className="
                  mt-3
                  font-display
                  text-3xl
                  font-semibold
                  text-white
                "
              >
                {completedInterviews.length}
              </div>

            </div>


            <div
              className="
                rounded-2xl
                border
                border-white/[0.06]
                bg-white/[0.02]
                p-5
              "
            >

              <div className="text-xs text-slate-600">
                Average score
              </div>

              <div
                className="
                  mt-3
                  font-display
                  text-3xl
                  font-semibold
                  text-white
                "
              >
                {averageScore !== null
                  ? averageScore.toFixed(0)
                  : "—"}
              </div>

            </div>


            <div
              className="
                rounded-2xl
                border
                border-white/[0.06]
                bg-white/[0.02]
                p-5
              "
            >

              <div className="text-xs text-slate-600">
                Best score
              </div>

              <div
                className="
                  mt-3
                  font-display
                  text-3xl
                  font-semibold
                  text-white
                "
              >
                {bestScore !== null
                  ? bestScore.toFixed(0)
                  : "—"}
              </div>

            </div>

          </div>


          {inProgressInterviews.length >
            0 && (
            <div
              className="
                mt-4
                rounded-2xl
                border
                border-amber-400/10
                bg-amber-400/[0.025]
                p-5
              "
            >

              <div
                className="
                  font-mono
                  text-[9px]
                  uppercase
                  tracking-[0.14em]
                  text-amber-400/70
                "
              >
                Active session
              </div>

              <p
                className="
                  mt-2
                  text-sm
                  text-slate-400
                "
              >
                You have{" "}
                {inProgressInterviews.length}{" "}
                interview session
                {inProgressInterviews.length !==
                1
                  ? "s"
                  : ""}{" "}
                currently in progress.
              </p>

            </div>
          )}

        </section>

        {/* =================================================
            FOOTER
        ================================================== */}

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