import type { Evaluation } from "../../lib/api";

interface EvaluationFeedbackProps {
  evaluation: Evaluation;
  onContinue: () => void;
  isContinuing: boolean;
}

function Score({
  label,
  value,
}: {
  label: string;
  value: number | null;
}) {
  return (
    <div className="rounded-2xl border border-white/[0.06] bg-white/[0.02] p-4">
      <div className="font-mono text-[9px] uppercase tracking-[0.14em] text-slate-600">
        {label}
      </div>

      <div className="mt-2 font-display text-2xl font-semibold text-white">
        {value !== null ? Math.round(value) : "—"}
      </div>
    </div>
  );
}

export default function EvaluationFeedback({
  evaluation,
  onContinue,
  isContinuing,
}: EvaluationFeedbackProps) {
  return (
    <section className="rounded-3xl border border-emerald-400/10 bg-emerald-400/[0.025] p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="font-mono text-[10px] uppercase tracking-[0.18em] text-emerald-400">
            AI evaluation
          </div>

          <h2 className="mt-2 font-display text-2xl font-semibold text-white">
            Your answer has been evaluated.
          </h2>
        </div>

        <div className="text-left sm:text-right">
          <div className="font-mono text-[9px] uppercase tracking-[0.14em] text-slate-600">
            Overall
          </div>

          <div className="font-display text-4xl font-semibold text-emerald-300">
            {evaluation.overall_score !== null
              ? Math.round(evaluation.overall_score)
              : "—"}
          </div>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-3 gap-3">
        <Score
          label="Technical"
          value={evaluation.technical_score}
        />

        <Score
          label="Communication"
          value={evaluation.communication_score}
        />

        <Score
          label="Relevance"
          value={evaluation.relevance_score}
        />
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-white/[0.05] bg-black/10 p-5">
          <div className="font-mono text-[9px] uppercase tracking-[0.14em] text-slate-600">
            Feedback
          </div>

          <p className="mt-3 text-sm leading-6 text-slate-300">
            {evaluation.feedback ||
              "No additional feedback provided."}
          </p>
        </div>

        <div className="rounded-2xl border border-white/[0.05] bg-black/10 p-5">
          <div className="font-mono text-[9px] uppercase tracking-[0.14em] text-emerald-400/70">
            Strengths
          </div>

          <p className="mt-3 text-sm leading-6 text-slate-300">
            {evaluation.strengths ||
              "No strengths provided."}
          </p>
        </div>

        <div className="rounded-2xl border border-white/[0.05] bg-black/10 p-5">
          <div className="font-mono text-[9px] uppercase tracking-[0.14em] text-amber-300/70">
            Improve
          </div>

          <p className="mt-3 text-sm leading-6 text-slate-300">
            {evaluation.improvements ||
              "No improvements provided."}
          </p>
        </div>
      </div>

      <button
        type="button"
        disabled={isContinuing}
        onClick={onContinue}
        className="mt-6 w-full rounded-xl bg-white px-6 py-3.5 font-display text-sm font-semibold text-slate-950 transition-all hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isContinuing
          ? "Loading next question..."
          : "Continue interview →"}
      </button>
    </section>
  );
}