import { FormEvent, useState } from "react";
import {
  Link,
  useNavigate,
  useSearchParams,
} from "react-router-dom";

import { resetPassword } from "../api/auth";

export default function ResetPassword() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const token = searchParams.get("token") ?? "";

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setError("");
    setSuccess("");

    if (!token) {
      setError(
        "This reset link is missing its token. Request a new password-reset link."
      );
      return;
    }

    if (password !== confirmPassword) {
      setError("The passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      const result = await resetPassword(
        token,
        password
      );

      setSuccess(result.message);
      setPassword("");
      setConfirmPassword("");
    } catch (requestError: any) {
      setError(
        requestError?.response?.data?.detail ||
          "Unable to reset your password. Request a new link and try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 px-6 py-10">
      <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-8 shadow-2xl">
        <Link
          to="/login"
          className="mb-8 inline-block text-sm text-slate-400 hover:text-white"
        >
          ← Back to sign in
        </Link>

        <h1 className="text-3xl font-bold text-white">
          Set a new password
        </h1>

        <p className="mt-2 text-slate-400">
          Choose a strong password with at least 8
          characters.
        </p>

        {error && (
          <div
            role="alert"
            className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300"
          >
            {error}
          </div>
        )}

        {success && (
          <div
            role="status"
            className="mt-6 rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-300"
          >
            {success}

            <button
              type="button"
              onClick={() =>
                navigate("/login", { replace: true })
              }
              className="mt-3 block font-semibold text-emerald-200 underline"
            >
              Continue to sign in
            </button>
          </div>
        )}

        {!success && (
          <form
            onSubmit={handleSubmit}
            className="mt-6 space-y-5"
          >
            <div>
              <label
                htmlFor="new-password"
                className="text-sm text-slate-300"
              >
                New password
              </label>

              <input
                id="new-password"
                type="password"
                autoComplete="new-password"
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

            <div>
              <label
                htmlFor="confirm-password"
                className="text-sm text-slate-300"
              >
                Confirm new password
              </label>

              <input
                id="confirm-password"
                type="password"
                autoComplete="new-password"
                required
                minLength={8}
                maxLength={128}
                value={confirmPassword}
                onChange={(event) =>
                  setConfirmPassword(event.target.value)
                }
                className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
                placeholder="Enter the password again"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-blue-600 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading
                ? "Updating password..."
                : "Reset password"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}