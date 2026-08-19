import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";

import { register } from "../api/auth";

export default function Register() {
  const navigate = useNavigate();

  const [fullName, setFullName] = useState("");
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
      await register({
        full_name: fullName,
        email,
        password,
      });

      navigate("/login");
    } catch (error: any) {
      setError(
        error?.response?.data?.detail ||
          "Unable to create your account."
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
          Create account
        </h1>

        <p className="mt-2 text-slate-400">
          Start practicing for your technical interviews.
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
              Full Name
            </label>

            <input
              type="text"
              required
              minLength={3}
              maxLength={100}
              value={fullName}
              onChange={(event) =>
                setFullName(event.target.value)
              }
              className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
              placeholder="Abrar Ahmed"
            />
          </div>

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
              minLength={8}
              maxLength={128}
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
              placeholder="Minimum 8 characters"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {loading
              ? "Creating account..."
              : "Create Account"}
          </button>
        </form>

        <button
          onClick={() => navigate("/login")}
          className="mt-6 w-full text-sm text-slate-400 hover:text-white"
        >
          Already have an account? Sign in
        </button>
      </div>
    </div>
  );
}