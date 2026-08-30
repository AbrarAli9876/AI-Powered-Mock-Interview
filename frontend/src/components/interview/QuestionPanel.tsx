import type { Difficulty, Question } from "../../lib/api";

interface QuestionPanelProps {
  question: Question;
  questionNumber: number;
  totalQuestions: number;
  difficulty: Difficulty;
}

export default function QuestionPanel({
  question,
  questionNumber,
  totalQuestions,
  difficulty,
}: QuestionPanelProps) {
  const progress =
    totalQuestions > 0
      ? Math.min(
          (questionNumber / totalQuestions) * 100,
          100,
        )
      : 0;

  return (
    <section className="rounded-3xl border border-white/[0.07] bg-white/[0.025] p-7 shadow-[0_20px_80px_rgba(0,0,0,0.18)]">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="font-mono text-[10px] uppercase tracking-[0.18em] text-violet-400">
          Question{" "}
          {questionNumber > 0
            ? String(questionNumber).padStart(2, "0")
            : "01"}
        </div>

        <div className="rounded-full border border-cyan-400/15 bg-cyan-400/[0.04] px-3 py-1.5 font-mono text-[9px] uppercase tracking-[0.14em] text-cyan-300">
          {difficulty}
        </div>
      </div>

      <div className="mt-5 h-1 overflow-hidden rounded-full bg-white/[0.05]">
        <div
          className="h-full rounded-full bg-gradient-to-r from-violet-400 to-cyan-300 transition-all duration-700"
          style={{
            width: `${progress}%`,
          }}
        />
      </div>

      <div className="mt-10">
        <p className="max-w-4xl font-display text-2xl font-medium leading-relaxed tracking-tight text-white sm:text-3xl">
          {question.question_text}
        </p>
      </div>

      <div className="mt-8 flex items-center justify-between border-t border-white/[0.06] pt-5">
        <span className="font-mono text-[9px] uppercase tracking-[0.14em] text-slate-700">
          Answer naturally
        </span>

        <span className="font-mono text-[9px] uppercase tracking-[0.14em] text-slate-700">
          {totalQuestions > 0
            ? `${questionNumber} / ${totalQuestions}`
            : "Adaptive"}
        </span>
      </div>
    </section>
  );
}