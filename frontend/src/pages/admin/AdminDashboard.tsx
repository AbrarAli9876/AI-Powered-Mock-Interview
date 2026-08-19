import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../../api/axios";
import { logout } from "../../api/auth";

interface DashboardStats {
  total_users: number;
  total_interviews: number;
  completed_interviews: number;
  in_progress_interviews: number;
  abandoned_interviews: number;
  average_interview_score: number | null;
}

export default function AdminDashboard() {
  const navigate = useNavigate();

  const [stats, setStats] =
    useState<DashboardStats | null>(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const response =
          await api.get<DashboardStats>(
            "/admin/dashboard"
          );

        setStats(response.data);
      } catch (error) {
        console.error(
          "Failed to load admin dashboard:",
          error
        );
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const cards = [
    {
      title: "Total Users",
      value: stats?.total_users ?? 0,
    },
    {
      title: "Total Interviews",
      value: stats?.total_interviews ?? 0,
    },
    {
      title: "Completed",
      value: stats?.completed_interviews ?? 0,
    },
    {
      title: "In Progress",
      value: stats?.in_progress_interviews ?? 0,
    },
    {
      title: "Abandoned",
      value: stats?.abandoned_interviews ?? 0,
    },
    {
      title: "Average Score",
      value:
        stats?.average_interview_score !== null &&
        stats?.average_interview_score !== undefined
          ? `${stats.average_interview_score}/100`
          : "—",
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <nav className="border-b border-slate-800">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="font-bold">
              AI Mock Interview
            </h1>

            <p className="text-xs text-slate-500">
              Administrator
            </p>
          </div>

          <button
            onClick={handleLogout}
            className="text-sm text-slate-400 hover:text-white"
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="mx-auto max-w-7xl px-6 py-10">
        <h2 className="text-4xl font-bold">
          Admin Dashboard
        </h2>

        <p className="mt-2 text-slate-400">
          Overview of the interview platform.
        </p>

        {loading ? (
          <p className="mt-10 text-slate-400">
            Loading dashboard...
          </p>
        ) : (
          <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {cards.map((card) => (
              <div
                key={card.title}
                className="rounded-2xl border border-slate-800 bg-slate-900 p-6"
              >
                <p className="text-sm text-slate-400">
                  {card.title}
                </p>

                <p className="mt-3 text-3xl font-bold">
                  {card.value}
                </p>
              </div>
            ))}
          </div>
        )}

        <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
          <button
            onClick={() =>
              navigate("/admin/users")
            }
            className="rounded-xl border border-slate-800 bg-slate-900 p-5 text-left hover:border-blue-500"
          >
            <h3 className="font-semibold">
              Users
            </h3>
            <p className="mt-1 text-sm text-slate-400">
              Manage application users.
            </p>
          </button>

          <button
            onClick={() =>
              navigate("/admin/topics")
            }
            className="rounded-xl border border-slate-800 bg-slate-900 p-5 text-left hover:border-blue-500"
          >
            <h3 className="font-semibold">
              Topics
            </h3>
            <p className="mt-1 text-sm text-slate-400">
              Manage interview topics.
            </p>
          </button>

          <button
            onClick={() =>
              navigate("/admin/questions")
            }
            className="rounded-xl border border-slate-800 bg-slate-900 p-5 text-left hover:border-blue-500"
          >
            <h3 className="font-semibold">
              Questions
            </h3>
            <p className="mt-1 text-sm text-slate-400">
              Manage interview questions.
            </p>
          </button>

          <button
            onClick={() =>
              navigate("/admin/interviews")
            }
            className="rounded-xl border border-slate-800 bg-slate-900 p-5 text-left hover:border-blue-500"
          >
            <h3 className="font-semibold">
              Interviews
            </h3>
            <p className="mt-1 text-sm text-slate-400">
              Review candidate interviews.
            </p>
          </button>
        </div>
      </main>
    </div>
  );
}