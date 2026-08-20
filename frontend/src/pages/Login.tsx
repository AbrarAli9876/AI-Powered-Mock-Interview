import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getCurrentUser,
  login,
} from "../api/auth";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const token = await login({
        email,
        password,
      });

      localStorage.setItem(
        "access_token",
        token.access_token
      );

      const user = await getCurrentUser();

      localStorage.setItem(
        "user",
        JSON.stringify(user)
      );

      if (user.role === "admin") {
        navigate("/admin");
      } else {
        navigate("/home", { replace: true });
      }
    } catch (error: any) {
      setError(
        error?.response?.data?.detail ||
          "Unable to login. Please check your credentials."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 px-6">
      <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-8 shadow-2xl">
        <button
          onClick={() => navigate("/")}
          className="mb-8 text-sm text-slate-400 hover:text-white"
        >
          ← Back to home
        </button>

        <h1 className="text-3xl font-bold text-white">
          Welcome back
        </h1>

        <p className="mt-2 text-slate-400">
          Sign in to your account.
        </p>

        {error && (
          <div className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-400">
            {error}
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className="mt-6 space-y-5"
        >
          <div>
            <label className="text-sm text-slate-300">
              Email
            </label>

            <input
              type="email"
              required
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label className="text-sm text-slate-300">
              Password
            </label>

            <input
              type="password"
              required
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-400">
          Don't have an account?
        </p>

        <button
          onClick={() => navigate("/register")}
          className="mt-2 w-full text-sm font-medium text-blue-400 hover:text-blue-300"
        >
          Create an account
        </button>
      </div>
    </div>
  );
}