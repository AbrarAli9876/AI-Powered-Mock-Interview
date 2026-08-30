interface AnswerInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  disabled: boolean;
}

export default function AnswerInput({
  value,
  onChange,
  onSubmit,
  disabled,
}: AnswerInputProps) {
  const wordCount = value.trim()
    ? value.trim().split(/\s+/).length
    : 0;

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLTextAreaElement>,
  ) => {
    if (
      event.key === "Enter" &&
      (event.ctrlKey || event.metaKey)
    ) {
      event.preventDefault();

      if (!disabled && value.trim()) {
        onSubmit();
      }
    }
  };

  return (
    <section className="rounded-3xl border border-white/[0.07] bg-white/[0.02] p-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="font-mono text-[10px] uppercase tracking-[0.18em] text-slate-600">
            Your response
          </div>

          <p className="mt-1 text-xs text-slate-600">
            Explain your thinking as if you were in a real
            interview.
          </p>
        </div>

        <div className="font-mono text-[9px] uppercase tracking-[0.12em] text-slate-700">
          {wordCount} words
        </div>
      </div>

      <textarea
        value={value}
        onChange={(event) =>
          onChange(event.target.value)
        }
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder="Start typing your answer..."
        aria-label="Interview answer"
        className="mt-5 min-h-52 w-full resize-none rounded-2xl border border-white/[0.07] bg-black/20 p-5 text-sm leading-7 text-slate-200 outline-none transition focus:border-violet-400/30 focus:ring-1 focus:ring-violet-400/10 disabled:cursor-not-allowed disabled:opacity-50"
      />

      <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <span className="font-mono text-[9px] uppercase tracking-[0.12em] text-slate-700">
          Ctrl / ⌘ + Enter to submit
        </span>

        <button
          type="button"
          disabled={disabled || !value.trim()}
          onClick={onSubmit}
          className="rounded-xl bg-white px-6 py-3 font-display text-sm font-semibold text-slate-950 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-[0_12px_35px_rgba(139,92,246,0.22)] disabled:cursor-not-allowed disabled:opacity-40"
        >
          {disabled
            ? "Evaluating..."
            : "Submit answer →"}
        </button>
      </div>
    </section>
  );
}