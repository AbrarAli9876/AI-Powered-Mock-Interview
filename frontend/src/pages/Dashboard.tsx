import { useNavigate } from "react-router-dom";

import { logout } from "../api/auth";

export default function Dashboard() {
  const navigate = useNavigate();

  const userData = localStorage.getItem("user");
  const user = userData
    ? JSON.parse(userData)
    : null;

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <nav className="border-b border-slate-800">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <h1 className="font-bold">
            AI Mock Interview
          </h1>

          <button
            onClick={handleLogout}
            className="text-sm text-slate-400 hover:text-white"
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="mx-auto max-w-7xl px-6 py-12">
        <p className="text-slate-400">
          Welcome back,
        </p>

        <h2 className="mt-1 text-4xl font-bold">
          {user?.full_name}
        </h2>

        <div className="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h3 className="text-xl font-semibold">
              Start Interview
            </h3>

            <p className="mt-2 text-sm text-slate-400">
              Begin a new AI-powered technical interview.
            </p>

            <button
              onClick={() => navigate("/interview")}
              className="mt-6 rounded-lg bg-blue-600 px-5 py-3 font-medium hover:bg-blue-700"
            >
              Start Interview
            </button>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
            <h3 className="text-xl font-semibold">
              Interview History
            </h3>

            <p className="mt-2 text-sm text-slate-400">
              View your previous interviews and results.
            </p>

            <button
              className="mt-6 rounded-lg border border-slate-700 px-5 py-3 font-medium hover:bg-slate-800"
            >
              View History
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}