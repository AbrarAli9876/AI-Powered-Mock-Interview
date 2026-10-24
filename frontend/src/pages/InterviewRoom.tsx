import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  abandonInterview,
  completeInterview,
  getInterview,
  getInterviewResult,
  getNextQuestion,
  submitAnswer,
  type Difficulty,
  type Evaluation,
  type Interview,
  type InterviewResult,
  type Question,
} from "../lib/api";
import AIOrb from "../components/interview/AIOrb";
import {
  getInterviewCameraStream,
  getInterviewDisplayStream,
  stopInterviewSetupMedia,
} from "../lib/interviewMedia";
import { usePresenceDetection } from "../hooks/usePresenceDetection";
type RoomState =
  | "loading"
  | "ready"
  | "submitting"
  | "evaluated"
  | "completing"
  | "error";
type SpeechRecognitionEventLike = Event & {
  results: SpeechRecognitionResultList;
};
interface SpeechRecognitionLike {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start: () => void;
  stop: () => void;
  abort: () => void;
  onstart: (() => void) | null;
  onend: (() => void) | null;
  onerror: ((event: Event) => void) | null;
  onresult: ((event: SpeechRecognitionEventLike) => void) | null;
}
interface SpeechRecognitionConstructor {
  new (): SpeechRecognitionLike;
}
declare global {
  interface Window {
    SpeechRecognition?: SpeechRecognitionConstructor;
    webkitSpeechRecognition?: SpeechRecognitionConstructor;
  }
}
const difficultyLabel: Record<Difficulty, string> = {
  easy: "Easy",
  medium: "Medium",
  hard: "Hard",
};
const difficultyDescription: Record<Difficulty, string> = {
  easy: "Fundamental concept",
  medium: "Intermediate concept",
  hard: "Advanced concept",
};
const MAX_ANSWER_LENGTH = 5000;
export default function InterviewRoom() {
  const navigate = useNavigate();
  const { sessionId } = useParams<{ sessionId: string }>();
  const numericSessionId = Number(sessionId);
  const [interview, setInterview] = useState<Interview | null>(null);
  const [question, setQuestion] = useState<Question | null>(null);
  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [roomState, setRoomState] = useState<RoomState>("loading");
  const [error, setError] = useState<string | null>(null);
  const [showExitConfirmation, setShowExitConfirmation] = useState(false);
  const [isFinishing, setIsFinishing] = useState(false);
  const [fullscreenWarningCount, setFullscreenWarningCount] = useState(0);
  const [showFullscreenWarning, setShowFullscreenWarning] = useState(false);
  const [showFullscreenGate, setShowFullscreenGate] = useState(false);
  const [isSecurityTerminated, setIsSecurityTerminated] = useState(false);
  const [fullscreenError, setFullscreenError] = useState<string | null>(null);
  const [securityTerminationMessage, setSecurityTerminationMessage] = useState<string | null>(null);
  const pendingTabChangeRef = useRef(false);
  const securityTerminationRef = useRef(false);
  const securityActiveRef = useRef(false);
  const interviewRef = useRef<Interview | null>(null);
  useEffect(() => {
    interviewRef.current = interview;
  }, [interview]);
  /*
   * ---------------------------------------------------------
   * Speech-to-text state
   * ---------------------------------------------------------
   */
  const [isListening, setIsListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(true);
  const [speechError, setSpeechError] = useState<string | null>(null);
  const recognitionRef = useRef<SpeechRecognitionLike | null>(null);
  const shouldKeepListeningRef = useRef(false);
  const speechBaseAnswerRef = useRef("");
  /*
   * ---------------------------------------------------------
   * Validate session ID.
   * ---------------------------------------------------------
   */
  useEffect(() => {
    if (!sessionId || !Number.isInteger(numericSessionId) || numericSessionId <= 0) {
      setError("Invalid interview session.");
      setRoomState("error");
    }
  }, [sessionId, numericSessionId]);
  /*
   * ---------------------------------------------------------
   * Initialize browser speech recognition.
   * ---------------------------------------------------------
   */
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSpeechSupported(false);
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";
    recognition.onstart = () => {
      setIsListening(true);
      setSpeechError(null);
    };
    recognition.onresult = (event: SpeechRecognitionEventLike) => {
      let transcript = "";
      for (let index = 0; index < event.results.length; index += 1) {
        transcript += event.results[index][0].transcript;
      }
      const cleanTranscript = transcript.trim();
      const baseAnswer = speechBaseAnswerRef.current.trim();
      const combinedAnswer = [baseAnswer, cleanTranscript].filter(Boolean).join(" ");
      setAnswer(combinedAnswer.slice(0, MAX_ANSWER_LENGTH));
    };
    recognition.onerror = () => {
      setIsListening(false);
      setSpeechError(
        "Unable to access speech recognition. Please check your microphone permissions.",
      );
      shouldKeepListeningRef.current = false;
    };
    recognition.onend = () => {
      setIsListening(false);
      // Some browsers stop recognition automatically after a short period.
      // Restart while the user still expects the microphone to be active.
      if (shouldKeepListeningRef.current && roomState === "ready") {
        try {
          recognition.start();
        } catch {
          shouldKeepListeningRef.current = false;
        }
      }
    };
    recognitionRef.current = recognition;
    return () => {
      shouldKeepListeningRef.current = false;
      try {
        recognition.stop();
      } catch {
        // Recognition may already be stopped.
      }
      recognitionRef.current = null;
    };
  }, [roomState]);
  /*
   * ---------------------------------------------------------
   * Start / stop speech recognition.
   * ---------------------------------------------------------
   */
  const handleStartListening = () => {
    if (!speechSupported) {
      setSpeechError("Speech-to-text is not supported in this browser.");
      return;
    }
    if (!recognitionRef.current) {
      setSpeechError("Speech recognition is unavailable.");
      return;
    }
    if (roomState !== "ready" || isListening) {
      return;
    }
    setSpeechError(null);
    // Save the text that existed before speaking. New speech is appended to this.
    speechBaseAnswerRef.current = answer.trim();
    shouldKeepListeningRef.current = true;
    try {
      recognitionRef.current.start();
    } catch {
      setSpeechError("Could not start the microphone. Please try again.");
      shouldKeepListeningRef.current = false;
      setIsListening(false);
    }
  };
  const handleStopListening = () => {
    shouldKeepListeningRef.current = false;
    if (!recognitionRef.current) {
      setIsListening(false);
      return;
    }
    try {
      recognitionRef.current.stop();
    } catch {
      // Recognition may already be stopped.
    }
    setIsListening(false);
  };
  /*
   * ---------------------------------------------------------
   * Load interview and first question.
   * ---------------------------------------------------------
   */
  useEffect(() => {
    if (!sessionId || !Number.isInteger(numericSessionId) || numericSessionId <= 0) {
      return;
    }
    const loadInterview = async () => {
      try {
        const cameraStream = getInterviewCameraStream();
        const displayStream = getInterviewDisplayStream();
        const cameraLive = Boolean(
          cameraStream?.getVideoTracks().some((track) => track.readyState === "live"),
        );
        const displayTrack = displayStream?.getVideoTracks()[0];
        const displaySettings = displayTrack?.getSettings() as
          | (MediaTrackSettings & { displaySurface?: string })
          | undefined;
        const preflightVerified =
          sessionStorage.getItem("technicalInterviewPreflightVerified") === "true";
        if (
          !preflightVerified ||
          !cameraLive ||
          displayTrack?.readyState !== "live" ||
          displaySettings?.displaySurface !== "monitor"
        ) {
          sessionStorage.removeItem("technicalInterviewPreflightVerified");
          sessionStorage.removeItem("technicalInterviewPreflightStage");
          navigate("/interviews/new", { replace: true });
          return;
        }
        securityActiveRef.current = true;
        setShowFullscreenGate(false);
        setRoomState("loading");
        setError(null);
        const interviewData = await getInterview(numericSessionId);
        setInterview(interviewData);
        if (interviewData.status !== "in_progress") {
          navigate(`/interviews/${numericSessionId}/result`, { replace: true });
          return;
        }
        const questionData = await getNextQuestion(numericSessionId);
        setQuestion(questionData);
        setRoomState("ready");
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to load the interview.");
        setRoomState("error");
      }
    };
    void loadInterview();
  }, [sessionId, numericSessionId, navigate]);
  /*
   * ---------------------------------------------------------
   * Submit candidate answer.
   * ---------------------------------------------------------
   */
  const handleSubmitAnswer = async () => {
    if (!question || !interview) {
      return;
    }
    const trimmedAnswer = answer.trim();
    if (!trimmedAnswer) {
      setError("Please enter an answer before submitting.");
      return;
    }
    if (isListening) {
      handleStopListening();
    }
    try {
      setError(null);
      setSpeechError(null);
      setRoomState("submitting");
      const result = await submitAnswer(interview.id, question.id, trimmedAnswer);
      setEvaluation(result);
      setRoomState("evaluated");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to evaluate your answer.");
      setRoomState("ready");
    }
  };
  /*
   * ---------------------------------------------------------
   * Complete interview.
   * ---------------------------------------------------------
   */
  const handleCompleteInterview = async () => {
    if (!interview) {
      return;
    }
    handleStopListening();
    try {
      setIsFinishing(true);
      setRoomState("completing");
      setError(null);
      await completeInterview(interview.id);
      securityActiveRef.current = false;
      sessionStorage.removeItem("technicalInterviewPreflightVerified");
      sessionStorage.removeItem("technicalInterviewPreflightStage");
      stopInterviewSetupMedia();
      if (document.fullscreenElement) {
        try {
          await document.exitFullscreen();
        } catch {
          // Browser may already have exited fullscreen.
        }
      }
      try {
        // The backend may need a moment to generate the final AI report.
        await getInterviewResult(interview.id);
      } catch {
        // The result page handles a report that is not ready yet.
      }
      navigate(`/interviews/${interview.id}/result`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to complete the interview.");
      setRoomState("evaluated");
    } finally {
      setIsFinishing(false);
    }
  };
  /*
   * ---------------------------------------------------------
   * Load next question.
   * ---------------------------------------------------------
   */
  const handleNextQuestion = async () => {
    if (!interview) {
      return;
    }
    handleStopListening();
    try {
      setError(null);
      setSpeechError(null);
      setEvaluation(null);
      setAnswer("");
      speechBaseAnswerRef.current = "";
      setRoomState("loading");
      const updatedInterview = await getInterview(interview.id);
      setInterview(updatedInterview);
      // The interview may have become complete after the previous answer.
      if (updatedInterview.status !== "in_progress") {
        await handleCompleteInterview();
        return;
      }
      const nextQuestion = await getNextQuestion(interview.id);
      setQuestion(nextQuestion);
      setRoomState("ready");
    } catch (err) {
      const message = err instanceof Error ? err.message : "";
      // If there are no remaining questions, complete the interview.
      if (
        message.toLowerCase().includes("no more") ||
        message.toLowerCase().includes("question")
      ) {
        await handleCompleteInterview();
        return;
      }
      setError(message || "Unable to load the next question.");
      setRoomState("evaluated");
    }
  };
  /*
   * ---------------------------------------------------------
   * Fullscreen helpers and security termination.
   * ---------------------------------------------------------
   */
  const enterInterviewFullscreen = useCallback(async () => {
    if (!document.fullscreenEnabled) {
      setFullscreenError(
        "Fullscreen mode is not available in this browser. Please use a supported browser to continue.",
      );
      return false;
    }
    try {
      if (!document.fullscreenElement) {
        await document.documentElement.requestFullscreen();
      }
      if (!document.fullscreenElement) {
        securityActiveRef.current = false;
        setFullscreenError("Fullscreen mode could not be entered. Please try again.");
        return false;
      }
      securityActiveRef.current = true;
      setShowFullscreenGate(false);
      setShowFullscreenWarning(false);
      setFullscreenError(null);
      return true;
    } catch {
      securityActiveRef.current = false;
      setFullscreenError(
        "Fullscreen permission was not granted. Please click the button again and allow fullscreen mode.",
      );
      return false;
    }
  }, []);
  const handleFullscreenWarningReturn = useCallback(async () => {
    await enterInterviewFullscreen();
  }, [enterInterviewFullscreen]);
  const terminateForSecurityViolation = useCallback(
    async (reason: string) => {
      const currentInterview = interviewRef.current;
      if (!currentInterview || securityTerminationRef.current) {
        return;
      }
      securityTerminationRef.current = true;
      securityActiveRef.current = false;
      setIsSecurityTerminated(true);
      setError(reason);
      setRoomState("completing");
      try {
        await abandonInterview(currentInterview.id);
      } catch {
        // The local security state still prevents the candidate from continuing
        // even if the termination request fails.
      }
      sessionStorage.removeItem("technicalInterviewPreflightVerified");
      stopInterviewSetupMedia();
      if (document.fullscreenElement) {
        try {
          await document.exitFullscreen();
        } catch {
          // Browser may already have exited fullscreen.
        }
      }
      // The reason is passed along so Home can show why the interview ended.
      navigate("/home", { replace: true, state: { terminationReason: reason } });
    },
    [navigate],
  );
  /*
   * ---------------------------------------------------------
   * Abandon current interview.
   * ---------------------------------------------------------
   */
  const handleAbandonInterview = async () => {
    if (!interview) {
      return;
    }
    handleStopListening();
    try {
      setError(null);
      await abandonInterview(interview.id);
      securityActiveRef.current = false;
      sessionStorage.removeItem("technicalInterviewPreflightVerified");
      sessionStorage.removeItem("technicalInterviewPreflightStage");
      stopInterviewSetupMedia();
      if (document.fullscreenElement) {
        try {
          await document.exitFullscreen();
        } catch {
          // Browser may already have exited fullscreen.
        }
      }
      navigate("/home");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to abandon the interview.");
      setShowExitConfirmation(false);
    }
  };
  /*
   * ---------------------------------------------------------
   * Fullscreen exit (3 strikes) and tab/window switching.
   * ---------------------------------------------------------
   */
  useEffect(() => {
    if (!interview || interview.status !== "in_progress" || isSecurityTerminated) {
      return;
    }
    const handleFullscreenChange = () => {
      // Ignore fullscreen changes until the candidate has started securely.
      // A tab switch can also exit fullscreen; handle that as a tab violation
      // only after the candidate returns to this page.
      if (!securityActiveRef.current || document.visibilityState === "hidden") {
        return;
      }
      if (document.fullscreenElement) {
        setShowFullscreenWarning(false);
        return;
      }
      setFullscreenWarningCount((previousCount) => {
        const nextCount = previousCount + 1;
        if (nextCount >= 3) {
          setShowFullscreenWarning(false);
          setSecurityTerminationMessage(
            "Your interview is terminated because you have closed the full screen for the 3rd time.",
          );
        } else {
          setShowFullscreenWarning(true);
        }
        return nextCount;
      });
    };
    const handleVisibilityChange = () => {
      if (!securityActiveRef.current) return;

      // Wait until the candidate returns to this website before showing the
      // termination message. The interview is terminated after confirmation.
      if (document.visibilityState === "hidden") {
        pendingTabChangeRef.current = true;
        return;
      }

      if (
        document.visibilityState === "visible" &&
        pendingTabChangeRef.current
      ) {
        pendingTabChangeRef.current = false;
        setShowFullscreenWarning(false);
        setSecurityTerminationMessage(
          "Your interview is terminated because you have changed the tab.",
        );
      }
    };
    document.addEventListener("fullscreenchange", handleFullscreenChange);
    document.addEventListener("visibilitychange", handleVisibilityChange);
    return () => {
      document.removeEventListener("fullscreenchange", handleFullscreenChange);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [interview, isSecurityTerminated, terminateForSecurityViolation]);
  /*
   * ---------------------------------------------------------
   * Camera and screen-sharing enforcement.
   * Either track ending terminates the active interview.
   * ---------------------------------------------------------
   */
  useEffect(() => {
    if (!interview || interview.status !== "in_progress" || isSecurityTerminated) {
      return;
    }
    const cameraStream = getInterviewCameraStream();
    const displayStream = getInterviewDisplayStream();
    const cameraTrack = cameraStream?.getVideoTracks()[0];
    const displayTrack = displayStream?.getVideoTracks()[0];
    if (!cameraStream || !cameraTrack || cameraTrack.readyState !== "live") {
      void terminateForSecurityViolation(
        "The interview was terminated because camera access was not active.",
      );
      return;
    }
    if (!displayStream || !displayTrack || displayTrack.readyState !== "live") {
      void terminateForSecurityViolation(
        "The interview was terminated because screen sharing was not active.",
      );
      return;
    }
    const onCameraEnded = () => {
      void terminateForSecurityViolation(
        "The interview was terminated because the camera was turned off or disconnected.",
      );
    };
    const onCameraMuted = () => {
      void terminateForSecurityViolation(
        "The interview was terminated because the camera stopped providing video.",
      );
    };
    const onDisplayEnded = () => {
      void terminateForSecurityViolation(
        "The interview was terminated because entire-screen sharing stopped.",
      );
    };
    const onDisplayMuted = () => {
      void terminateForSecurityViolation(
        "The interview was terminated because screen sharing stopped providing video.",
      );
    };
    const onCameraInactive = () => {
      if (cameraStream.active === false) onCameraEnded();
    };
    const onDisplayInactive = () => {
      if (displayStream.active === false) onDisplayEnded();
    };
    cameraTrack.addEventListener("ended", onCameraEnded);
    cameraTrack.addEventListener("mute", onCameraMuted);
    displayTrack.addEventListener("ended", onDisplayEnded);
    displayTrack.addEventListener("mute", onDisplayMuted);
    cameraStream.addEventListener("inactive", onCameraInactive);
    displayStream.addEventListener("inactive", onDisplayInactive);
    // Also catch tracks that are disabled without firing an ended event.
    const mediaHealthCheck = window.setInterval(() => {
      if (
        cameraTrack.readyState !== "live" ||
        !cameraTrack.enabled ||
        cameraStream.active === false
      ) {
        onCameraEnded();
        return;
      }
      if (
        displayTrack.readyState !== "live" ||
        !displayTrack.enabled ||
        displayStream.active === false
      ) {
        onDisplayEnded();
      }
    }, 1000);
    return () => {
      window.clearInterval(mediaHealthCheck);
      cameraTrack.removeEventListener("ended", onCameraEnded);
      cameraTrack.removeEventListener("mute", onCameraMuted);
      displayTrack.removeEventListener("ended", onDisplayEnded);
      displayTrack.removeEventListener("mute", onDisplayMuted);
      cameraStream.removeEventListener("inactive", onCameraInactive);
      displayStream.removeEventListener("inactive", onDisplayInactive);
    };
  }, [interview, isSecurityTerminated, terminateForSecurityViolation]);
  /*
   * ---------------------------------------------------------
   * Face presence: alert right away, terminate after 5 continuous
   * seconds without a detected face.
   * ---------------------------------------------------------
   */
  const presence = usePresenceDetection({
    enabled:
      interview?.status === "in_progress" &&
      !isSecurityTerminated &&
      roomState !== "error" &&
      roomState !== "completing",
    graceMs: 5000,
    onTerminate: () => {
      void terminateForSecurityViolation(
        "The interview was ended because your face was not detected for 5 seconds.",
      );
    },
    onError: (e) => console.error("Face detection unavailable:", e),
  });
  /*
   * ---------------------------------------------------------
   * Keyboard shortcut: Ctrl/Cmd + Enter submits the answer.
   * ---------------------------------------------------------
   */
  useEffect(() => {
    const handleKeyboard = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter" && roomState === "ready") {
        event.preventDefault();
        void handleSubmitAnswer();
      }
    };
    window.addEventListener("keydown", handleKeyboard);
    return () => window.removeEventListener("keydown", handleKeyboard);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [roomState, answer, question, interview]);
  /*
   * ---------------------------------------------------------
   * Loading screen.
   * ---------------------------------------------------------
   */
  if (roomState === "loading") {
    return (
      <div className="app-background flex min-h-screen items-center justify-center px-6">
        <div className="text-center">
          <AIOrb state="thinking" />
          <p className="mt-7 font-mono text-[10px] uppercase tracking-[0.2em] text-slate-500">
            Preparing your interview
          </p>
        </div>
      </div>
    );
  }
  /*
   * ---------------------------------------------------------
   * Error screen.
   * ---------------------------------------------------------
   */
  if (roomState === "error") {
    return (
      <div className="app-background flex min-h-screen items-center justify-center px-6">
        <div className="w-full max-w-md rounded-3xl border border-red-400/20 bg-white/[0.025] p-8 text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-red-400/10 text-xl text-red-300">
            !
          </div>
          <h1 className="mt-5 font-display text-2xl font-semibold text-white">
            Something went wrong
          </h1>
          <p className="mt-3 text-sm leading-6 text-slate-500">
            {error || "Unable to load this interview."}
          </p>
          <button
            type="button"
            onClick={() => navigate("/home")}
            className="mt-7 rounded-2xl bg-white px-6 py-3 text-sm font-semibold text-slate-950 transition hover:-translate-y-0.5"
          >
            Return Home
          </button>
        </div>
      </div>
    );
  }
  if (!interview || !question) {
    return null;
  }
  const progress =
    interview.total_questions > 0
      ? Math.min((interview.current_question_number / interview.total_questions) * 100, 100)
      : 0;
  const isSubmitting = roomState === "submitting";
  const isEvaluated = roomState === "evaluated";
  const isCompleting = roomState === "completing";
  const currentDifficulty = question.difficulty;
  const canEditAnswer = roomState === "ready";
  return (
    <div className="app-background min-h-screen">
      {/* Ambient background */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden" aria-hidden="true">
        <div className="absolute left-1/2 top-[-300px] h-[600px] w-[600px] -translate-x-1/2 rounded-full bg-violet-500/[0.06] blur-[120px]" />
        <div className="absolute bottom-[-250px] right-[-150px] h-[500px] w-[500px] rounded-full bg-blue-500/[0.04] blur-[120px]" />
      </div>
      <main className="relative mx-auto min-h-screen w-full max-w-6xl px-5 py-6 sm:px-8 lg:px-10">
        {/* =====================================================
            TOP BAR
        ====================================================== */}
        <header className="flex items-center justify-between border-b border-white/[0.06] pb-5">
          <div>
            <div className="font-mono text-[9px] uppercase tracking-[0.2em] text-violet-400">
              Live interview
            </div>
            <h1 className="mt-1 font-display text-lg font-semibold text-white">Interview Room</h1>
          </div>
          <button
            type="button"
            onClick={() => setShowExitConfirmation(true)}
            disabled={isCompleting}
            className="rounded-xl border border-white/[0.08] px-4 py-2 text-xs font-medium text-slate-400 transition hover:border-red-400/20 hover:text-red-300 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Exit interview
          </button>
        </header>
        {/* =====================================================
            PROGRESS
        ====================================================== */}
        <section className="mt-7">
          <div className="flex items-center justify-between">
            <span className="font-mono text-[9px] uppercase tracking-[0.16em] text-slate-600">
              Progress
            </span>
            <span className="font-mono text-[10px] text-slate-500">
              {Math.min(interview.current_question_number, interview.total_questions)} /{" "}
              {interview.total_questions}
            </span>
          </div>
          <div className="mt-3 h-1 overflow-hidden rounded-full bg-white/[0.06]">
            <div
              className="h-full rounded-full bg-violet-400 transition-all duration-700 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
        </section>
        {/* =====================================================
            MAIN INTERVIEW GRID
        ====================================================== */}
        <div className="mt-8 grid gap-6 lg:grid-cols-[0.8fr_1.6fr]">
          {/* ===================================================
              AI INTERVIEWER
          ==================================================== */}
          <aside className="rounded-3xl border border-white/[0.06] bg-white/[0.025] p-6 lg:p-8">
            <div className="flex flex-col items-center text-center">
              <AIOrb state={isSubmitting ? "thinking" : isEvaluated ? "idle" : "speaking"} />
              <div className="mt-7">
                <div className="font-mono text-[9px] uppercase tracking-[0.18em] text-slate-600">
                  AI Interviewer
                </div>
                <h2 className="mt-2 font-display text-xl font-semibold text-white">
                  {isSubmitting
                    ? "Evaluating your answer"
                    : isEvaluated
                      ? "Evaluation ready"
                      : isListening
                        ? "Listening to you"
                        : "Your turn"}
                </h2>
                <p className="mx-auto mt-2 max-w-xs text-xs leading-5 text-slate-500">
                  {isSubmitting
                    ? "Analyzing technical accuracy, relevance and communication."
                    : isEvaluated
                      ? "Review your feedback before continuing."
                      : isListening
                        ? "Speak naturally. Your answer is being converted to text."
                        : "Take your time and explain your reasoning clearly."}
                </p>
              </div>
              {/* Difficulty */}
              <div className="mt-8 w-full rounded-2xl border border-white/[0.06] bg-black/10 p-4 text-left">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-[9px] uppercase tracking-[0.14em] text-slate-600">
                    Difficulty
                  </span>
                  <span className="rounded-full bg-violet-400/10 px-2.5 py-1 font-mono text-[9px] uppercase tracking-wider text-violet-300">
                    {difficultyLabel[currentDifficulty]}
                  </span>
                </div>
                <p className="mt-3 text-xs text-slate-500">
                  {difficultyDescription[currentDifficulty]}
                </p>
              </div>
              {/* Adaptive indicator */}
              <div className="mt-5 flex items-center gap-2">
                <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
                <span className="font-mono text-[9px] uppercase tracking-[0.12em] text-slate-600">
                  Adaptive difficulty enabled
                </span>
              </div>
            </div>
          </aside>
          {/* ===================================================
              QUESTION / ANSWER
          ==================================================== */}
          <section>
            {/* Question */}
            <div className="rounded-3xl border border-white/[0.06] bg-white/[0.025] p-6 sm:p-8">
              <div className="flex items-center justify-between">
                <div className="font-mono text-[9px] uppercase tracking-[0.18em] text-slate-600">
                  Question {interview.current_question_number}
                </div>
                <span className="rounded-full border border-white/[0.07] px-3 py-1 font-mono text-[9px] uppercase tracking-wider text-slate-500">
                  {difficultyLabel[currentDifficulty]}
                </span>
              </div>
              <h2 className="mt-6 font-display text-2xl font-semibold leading-tight tracking-tight text-white sm:text-3xl">
                {question.question_text}
              </h2>
            </div>
            {/* Answer */}
            <div className="mt-6 rounded-3xl border border-white/[0.06] bg-white/[0.025] p-6 sm:p-8">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-mono text-[9px] uppercase tracking-[0.18em] text-slate-600">
                    Your answer
                  </div>
                  <p className="mt-1 text-xs text-slate-600">Ctrl + Enter to submit</p>
                </div>
                <span className="font-mono text-[9px] text-slate-600">
                  {answer.length} characters
                </span>
              </div>
              {/* Speech-to-text status */}
              {isListening && (
                <div
                  className="mt-5 flex items-center gap-3 rounded-2xl border border-violet-400/20 bg-violet-400/[0.06] px-4 py-3"
                  role="status"
                  aria-live="polite"
                >
                  <span className="relative flex h-3 w-3">
                    <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-violet-400 opacity-60" />
                    <span className="relative inline-flex h-3 w-3 rounded-full bg-violet-400" />
                  </span>
                  <span className="font-mono text-[9px] uppercase tracking-[0.15em] text-violet-300">
                    Listening...
                  </span>
                  {/* Simple waveform */}
                  <div className="ml-auto flex h-5 items-center gap-1" aria-hidden="true">
                    <span className="h-2 w-1 animate-pulse rounded-full bg-violet-400" />
                    <span className="h-4 w-1 animate-pulse rounded-full bg-violet-400 [animation-delay:100ms]" />
                    <span className="h-5 w-1 animate-pulse rounded-full bg-violet-400 [animation-delay:200ms]" />
                    <span className="h-3 w-1 animate-pulse rounded-full bg-violet-400 [animation-delay:300ms]" />
                    <span className="h-4 w-1 animate-pulse rounded-full bg-violet-400 [animation-delay:400ms]" />
                  </div>
                </div>
              )}
              {/* Browser support message */}
              {!speechSupported && (
                <div
                  className="mt-5 rounded-2xl border border-amber-400/20 bg-amber-400/[0.05] px-4 py-3 text-xs leading-5 text-amber-200/70"
                  role="status"
                >
                  Speech-to-text is not supported by this browser. You can still type your answer
                  normally.
                </div>
              )}
              {/* Speech error */}
              {speechError && (
                <div
                  className="mt-5 rounded-2xl border border-red-400/20 bg-red-400/[0.05] px-4 py-3 text-xs leading-5 text-red-200/70"
                  role="alert"
                >
                  {speechError}
                </div>
              )}
              <textarea
                value={answer}
                onChange={(event) => setAnswer(event.target.value.slice(0, MAX_ANSWER_LENGTH))}
                disabled={!canEditAnswer}
                maxLength={MAX_ANSWER_LENGTH}
                aria-label="Your interview answer"
                placeholder={
                  isListening
                    ? "Listening... speak your answer naturally."
                    : "Explain your answer clearly. Include examples or reasoning where appropriate..."
                }
                className="mt-5 min-h-[240px] w-full resize-y rounded-2xl border border-white/[0.06] bg-black/20 p-5 text-sm leading-7 text-slate-200 outline-none placeholder:text-slate-700 transition focus:border-violet-400/30 focus:ring-2 focus:ring-violet-400/10 disabled:cursor-not-allowed disabled:opacity-60"
              />
              {/* Speech controls */}
              {canEditAnswer && (
                <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    {isListening ? (
                      <button
                        type="button"
                        onClick={handleStopListening}
                        className="inline-flex items-center gap-3 rounded-2xl border border-red-400/20 bg-red-400/[0.06] px-5 py-3 text-xs font-semibold text-red-200 transition hover:-translate-y-0.5 hover:border-red-400/30 hover:bg-red-400/[0.1] active:translate-y-0"
                        aria-label="Stop speech recognition"
                      >
                        <span className="flex h-7 w-7 items-center justify-center rounded-full bg-red-400/10">
                          <span className="h-2.5 w-2.5 rounded-sm bg-red-300" />
                        </span>
                        Stop speaking
                      </button>
                    ) : (
                      <button
                        type="button"
                        onClick={handleStartListening}
                        disabled={!speechSupported || isSubmitting}
                        className="inline-flex items-center gap-3 rounded-2xl border border-violet-400/20 bg-violet-400/[0.06] px-5 py-3 text-xs font-semibold text-violet-200 transition hover:-translate-y-0.5 hover:border-violet-400/30 hover:bg-violet-400/[0.1] active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-40"
                        aria-label="Start speech recognition"
                      >
                        <span className="flex h-7 w-7 items-center justify-center rounded-full bg-violet-400/10">
                          <svg
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1.8"
                            className="h-4 w-4"
                            aria-hidden="true"
                          >
                            <path d="M12 14a3 3 0 0 0 3-3V6a3 3 0 1 0-6 0v5a3 3 0 0 0 3 3Z" />
                            <path d="M19 11a7 7 0 0 1-14 0" />
                            <path d="M12 18v4" />
                            <path d="M8 22h8" />
                          </svg>
                        </span>
                        Start speaking
                      </button>
                    )}
                  </div>
                  <span className="text-xs text-slate-600">
                    Speak naturally — your words will appear above.
                  </span>
                </div>
              )}
              {/* Submit */}
              <button
                type="button"
                onClick={() => void handleSubmitAnswer()}
                disabled={isSubmitting || isEvaluated || isCompleting || !answer.trim()}
                className="mt-5 flex w-full items-center justify-center gap-3 rounded-2xl bg-white px-6 py-4 text-sm font-semibold text-slate-950 transition hover:-translate-y-0.5 hover:bg-slate-100 active:translate-y-0 disabled:cursor-not-allowed disabled:bg-white/40 disabled:text-slate-800"
              >
                {isSubmitting ? (
                  <>
                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-900/20 border-t-slate-900" />
                    Evaluating answer...
                  </>
                ) : (
                  <>
                    Submit Answer
                    <span aria-hidden="true">→</span>
                  </>
                )}
              </button>
              {error && roomState === "ready" && (
                <p className="mt-4 text-center text-xs text-red-300" role="alert">
                  {error}
                </p>
              )}
            </div>
            {/* =================================================
                EVALUATION
            ================================================== */}
            {isEvaluated && evaluation && (
              <div className="mt-6 rounded-3xl border border-white/[0.06] bg-white/[0.025] p-6 sm:p-8">
                <div className="flex items-start justify-between gap-5">
                  <div>
                    <div className="font-mono text-[9px] uppercase tracking-[0.18em] text-violet-400">
                      AI Evaluation
                    </div>
                    <h2 className="mt-2 font-display text-xl font-semibold text-white">
                      Your feedback
                    </h2>
                  </div>
                  <div className="rounded-2xl border border-white/[0.07] bg-black/10 px-4 py-3 text-center">
                    <div className="font-display text-2xl font-bold text-white">
                      {Math.round(evaluation.overall_score ?? 0)}
                    </div>
                    <div className="font-mono text-[8px] uppercase tracking-wider text-slate-600">
                      Score
                    </div>
                  </div>
                </div>
                {/* Scores */}
                <div className="mt-6 grid gap-3 sm:grid-cols-3">
                  <div className="rounded-2xl border border-white/[0.06] bg-black/10 p-4">
                    <div className="font-mono text-[8px] uppercase tracking-wider text-slate-600">
                      Technical
                    </div>
                    <div className="mt-2 text-xl font-semibold text-white">
                      {Math.round(evaluation.technical_score ?? 0)}
                    </div>
                  </div>
                  <div className="rounded-2xl border border-white/[0.06] bg-black/10 p-4">
                    <div className="font-mono text-[8px] uppercase tracking-wider text-slate-600">
                      Communication
                    </div>
                    <div className="mt-2 text-xl font-semibold text-white">
                      {Math.round(evaluation.communication_score ?? 0)}
                    </div>
                  </div>
                  <div className="rounded-2xl border border-white/[0.06] bg-black/10 p-4">
                    <div className="font-mono text-[8px] uppercase tracking-wider text-slate-600">
                      Relevance
                    </div>
                    <div className="mt-2 text-xl font-semibold text-white">
                      {Math.round(evaluation.relevance_score ?? 0)}
                    </div>
                  </div>
                </div>
                {/* Feedback */}
                <div className="mt-6 border-t border-white/[0.06] pt-6">
                  <div className="font-mono text-[8px] uppercase tracking-[0.16em] text-slate-600">
                    Feedback
                  </div>
                  <p className="mt-3 text-sm leading-7 text-slate-400">{evaluation.feedback}</p>
                </div>
                {/* Strengths */}
                <div className="mt-6 border-t border-white/[0.06] pt-6">
                  <div className="font-mono text-[8px] uppercase tracking-[0.16em] text-slate-600">
                    Strengths
                  </div>
                  <p className="mt-3 text-sm leading-7 text-slate-400">{evaluation.strengths}</p>
                </div>
                {/* Improvements */}
                <div className="mt-6 border-t border-white/[0.06] pt-6">
                  <div className="font-mono text-[8px] uppercase tracking-[0.16em] text-slate-600">
                    Improvements
                  </div>
                  <p className="mt-3 text-sm leading-7 text-slate-400">
                    {evaluation.improvements}
                  </p>
                </div>
                {/* Continue */}
                <button
                  type="button"
                  onClick={() => void handleNextQuestion()}
                  disabled={isFinishing}
                  className="mt-7 flex w-full items-center justify-center gap-3 rounded-2xl bg-violet-400 px-6 py-4 text-sm font-semibold text-slate-950 transition hover:-translate-y-0.5 hover:bg-violet-300 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  Continue to next question
                  <span aria-hidden="true">→</span>
                </button>
              </div>
            )}
            {/* Completing */}
            {isCompleting && (
              <div className="mt-6 rounded-3xl border border-white/[0.06] bg-white/[0.025] p-8 text-center">
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full border border-violet-400/20 bg-violet-400/[0.06]">
                  <span className="h-5 w-5 animate-spin rounded-full border-2 border-violet-400/20 border-t-violet-300" />
                </div>
                <h3 className="mt-5 font-display text-lg font-semibold text-white">
                  Preparing your final report
                </h3>
                <p className="mx-auto mt-2 max-w-md text-xs leading-5 text-slate-500">
                  We're analyzing your interview performance and preparing your personalized
                  feedback.
                </p>
              </div>
            )}
          </section>
        </div>
      </main>
      {/* =======================================================
          FACE NOT DETECTED ALERT
      ======================================================== */}
      {presence.status === "no-face" && !isSecurityTerminated && (
        <div
          role="alert"
          aria-live="assertive"
          className="fixed inset-x-0 top-6 z-[80] mx-auto w-fit max-w-[90vw] rounded-2xl border border-rose-400/30 bg-rose-950/95 px-6 py-4 text-center shadow-2xl backdrop-blur"
        >
          <p className="text-sm font-medium text-rose-100">
            Face not detected. Move back into the camera view.
          </p>
          <p className="mt-1 font-display text-2xl font-semibold text-white">
            Interview ends in {presence.secondsLeft}s
          </p>
        </div>
      )}
      {/* =======================================================
          FULLSCREEN START GATE
      ======================================================== */}
      {showFullscreenGate && !isSecurityTerminated && (
        <div
          className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/95 px-5 backdrop-blur-md"
          role="dialog"
          aria-modal="true"
          aria-labelledby="fullscreen-gate-title"
        >
          <div className="w-full max-w-lg rounded-3xl border border-white/[0.08] bg-white/[0.035] p-8 text-center shadow-2xl">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-violet-400/[0.10] text-violet-300">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.7"
                className="h-7 w-7"
                aria-hidden="true"
              >
                <path d="M8 3H5a2 2 0 0 0-2 2v3" />
                <path d="M16 3h3a2 2 0 0 1 2 2v3" />
                <path d="M8 21H5a2 2 0 0 1-2-2v-3" />
                <path d="M16 21h3a2 2 0 0 0 2-2v-3" />
              </svg>
            </div>
            <div className="mt-6 font-mono text-[9px] uppercase tracking-[0.2em] text-violet-400">
              Secure interview
            </div>
            <h2
              id="fullscreen-gate-title"
              className="mt-2 font-display text-2xl font-semibold text-white"
            >
              Enter fullscreen to begin
            </h2>
            <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-slate-500">
              Fullscreen mode is required for the interview. Switching to another tab or window
              will immediately end the interview.
            </p>
            {fullscreenError && (
              <p
                className="mt-5 rounded-2xl border border-red-400/20 bg-red-400/[0.05] px-4 py-3 text-xs leading-5 text-red-200/80"
                role="alert"
              >
                {fullscreenError}
              </p>
            )}
            <button
              type="button"
              onClick={() => void enterInterviewFullscreen()}
              className="mt-7 w-full rounded-2xl bg-violet-400 px-6 py-4 text-sm font-semibold text-slate-950 transition hover:-translate-y-0.5 hover:bg-violet-300"
            >
              Start Interview →
            </button>
          </div>
        </div>
      )}
      {/* =======================================================
          SECURITY TERMINATION CONFIRMATION
      ======================================================== */}
      {securityTerminationMessage && !isSecurityTerminated && (
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 px-5 backdrop-blur-sm"
          role="alertdialog"
          aria-modal="true"
          aria-labelledby="security-termination-title"
          aria-describedby="security-termination-description"
        >
          <div className="w-full max-w-md rounded-3xl border border-red-400/30 bg-slate-950 p-7 text-center shadow-2xl">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-red-400/[0.10] text-red-300">
              !
            </div>
            <h2
              id="security-termination-title"
              className="mt-5 font-display text-xl font-semibold text-white"
            >
              Interview terminated
            </h2>
            <p
              id="security-termination-description"
              className="mt-3 text-sm leading-6 text-slate-300"
            >
              {securityTerminationMessage}
            </p>
            <button
              type="button"
              onClick={() => {
                void terminateForSecurityViolation(securityTerminationMessage);
              }}
              className="mt-6 w-full rounded-2xl bg-red-400 px-6 py-4 text-sm font-semibold text-slate-950 transition hover:bg-red-300"
            >
              End interview
            </button>
          </div>
        </div>
      )}
      {/* =======================================================
          FULLSCREEN WARNING
      ======================================================== */}
      {showFullscreenWarning && !isSecurityTerminated && !securityTerminationMessage && (
        <div
          className="fixed inset-0 z-[55] flex items-center justify-center bg-black/75 px-5 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-labelledby="fullscreen-warning-title"
        >
          <div className="w-full max-w-md rounded-3xl border border-amber-400/20 bg-slate-950 p-7 text-center shadow-2xl">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-400/[0.08] text-amber-300">
              !
            </div>
            <h2
              id="fullscreen-warning-title"
              className="mt-5 font-display text-xl font-semibold text-white"
            >
              Fullscreen required
            </h2>
            <p className="mt-3 text-sm leading-6 text-slate-500">
              You exited fullscreen. This is warning {fullscreenWarningCount} of 3. The third
              fullscreen exit will end the interview.
            </p>
            {fullscreenError && (
              <p
                className="mt-4 rounded-2xl border border-red-400/20 bg-red-400/[0.05] px-4 py-3 text-xs leading-5 text-red-200/80"
                role="alert"
              >
                {fullscreenError}
              </p>
            )}
            <button
              type="button"
              onClick={() => void handleFullscreenWarningReturn()}
              className="mt-6 w-full rounded-2xl bg-violet-400 px-6 py-4 text-sm font-semibold text-slate-950 transition hover:-translate-y-0.5 hover:bg-violet-300"
            >
              Return to fullscreen →
            </button>
          </div>
        </div>
      )}
      {/* =======================================================
          EXIT CONFIRMATION
      ======================================================== */}
      {showExitConfirmation && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-5 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-labelledby="exit-interview-title"
        >
          <div className="w-full max-w-md rounded-3xl border border-white/[0.08] bg-slate-950 p-7 shadow-2xl">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-red-400/[0.08] text-red-300">
              !
            </div>
            <h2
              id="exit-interview-title"
              className="mt-5 font-display text-xl font-semibold text-white"
            >
              Exit interview?
            </h2>
            <p className="mt-3 text-sm leading-6 text-slate-500">
              Your current interview will be abandoned and you will return to the home page.
            </p>
            <div className="mt-7 flex gap-3">
              <button
                type="button"
                onClick={() => setShowExitConfirmation(false)}
                className="flex-1 rounded-2xl border border-white/[0.08] px-5 py-3 text-sm font-medium text-slate-300 transition hover:border-white/[0.15] hover:bg-white/[0.03]"
              >
                Continue interview
              </button>
              <button
                type="button"
                onClick={() => void handleAbandonInterview()}
                className="flex-1 rounded-2xl bg-red-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-red-300"
              >
                Exit interview
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
