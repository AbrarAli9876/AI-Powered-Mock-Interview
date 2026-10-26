import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { requestPasswordReset } from "../api/auth";

export default function ForgotPassword() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setError("");
    setMessage("");
    setLoading(true);

    try {
      const result = await requestPasswordReset(
        email.trim()
      );

      setMessage(result.message);
    } catch (requestError: any) {
      setError(
        requestError?.response?.data?.detail ||
          "Unable to request a password reset right now. Please try again later."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 px-6 py-10">
      <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-8 shadow-2xl">
        <button
          type="button"
          onClick={() => navigate("/login")}
          className="mb-8 text-sm text-slate-400 hover:text-white"
        >
          ← Back to sign in
        </button>

        <h1 className="text-3xl font-bold text-white">
          Forgot password?
        </h1>

        <p className="mt-2 text-slate-400">
          Enter the email address associated with your
          account. If it exists, we’ll send you a
          password-reset link.
        </p>

        {error && (
          <div
            role="alert"
            className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300"
          >
            {error}
          </div>
        )}

        {message && (
          <div
            role="status"
            className="mt-6 rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-300"
          >
            {message}
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className="mt-6 space-y-5"
        >
          <div>
            <label
              htmlFor="reset-email"
              className="text-sm text-slate-300"
            >
              Email
            </label>

            <input
              id="reset-email"
              type="email"
              autoComplete="email"
              required
              maxLength={255}
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
              placeholder="you@example.com"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Sending..." : "Send reset link"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-400">
          Remembered your password?{" "}
          <Link
            to="/login"
            className="font-medium text-blue-400 hover:text-blue-300"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}