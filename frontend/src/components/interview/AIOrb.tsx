interface AIOrbProps {
  state?: "idle" | "speaking" | "thinking";
}

export default function AIOrb({
  state = "idle",
}: AIOrbProps) {
  const isThinking =
    state === "thinking";

  const isSpeaking =
    state === "speaking";

  return (
    <div
      className="
        relative
        flex
        h-40
        w-40
        items-center
        justify-center
      "
      aria-label={
        isThinking
          ? "AI is thinking"
          : isSpeaking
            ? "AI is speaking"
            : "AI interviewer"
      }
      role="img"
    >
      {/* Outer pulse */}
      <div
        className={`
          absolute
          inset-0
          rounded-full
          border
          border-violet-400/10
          ${
            isThinking ||
            isSpeaking
              ? "animate-ping"
              : ""
          }
        `}
      />

      {/* Middle ring */}
      <div
        className={`
          absolute
          inset-5
          rounded-full
          border
          border-violet-400/20
          ${
            isThinking
              ? "animate-pulse"
              : ""
          }
        `}
      />

      {/* Glow */}
      <div
        className="
          absolute
          h-24
          w-24
          rounded-full
          bg-violet-500/20
          blur-2xl
        "
      />

      {/* Core */}
      <div
        className={`
          relative
          flex
          h-20
          w-20
          items-center
          justify-center
          rounded-full
          border
          border-violet-300/30
          bg-slate-900
          shadow-[0_0_60px_rgba(139,92,246,0.25)]
          ${
            isSpeaking
              ? "animate-pulse"
              : ""
          }
        `}
      >
        <div
          className="
            h-3
            w-3
            rounded-full
            bg-violet-300
            shadow-[0_0_20px_rgba(196,181,253,0.8)]
          "
        />
      </div>
    </div>
  );
}