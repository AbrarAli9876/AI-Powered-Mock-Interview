
import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  FaceDetector,
  FilesetResolver,
} from "@mediapipe/tasks-vision";
import CodingInterview from "./CodingInterview";
import { abandonCodingInterview } from "../lib/api";
import {
  getInterviewCameraStream,
  getInterviewDisplayStream,
  stopInterviewSetupMedia,
} from "../lib/interviewMedia";

const FACE_TIMEOUT_MS = 5000;

export default function CodingInterviewRoom() {
  const navigate = useNavigate();
  const location = useLocation();
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const terminatedRef = useRef(false);
  const fullscreenExitCountRef = useRef(0);
  const pendingTabChangeRef = useRef(false);
  const terminateRef = useRef<(reason: string) => void>(
    () => undefined
  );

  const [fullscreenWarning, setFullscreenWarning] =
    useState<string | null>(null);
  const [terminationMessage, setTerminationMessage] =
    useState<string | null>(null);
  const [faceCountdown, setFaceCountdown] =
    useState<number | null>(null);

  const state = location.state as {
    sessionId?: number | string;
    preflightChecksPassed?: boolean;
  } | null;

  // Use router state first, then the sessionStorage fallback written by preflight.
  const storedSessionId = sessionStorage.getItem("codingInterviewSessionId");
  const rawSessionId = state?.sessionId ?? storedSessionId;
  const sessionId =
    rawSessionId !== undefined && rawSessionId !== null && String(rawSessionId).trim() !== ""
      ? String(rawSessionId)
      : null;

  const preflightChecksPassed =
    state?.preflightChecksPassed === true ||
    sessionStorage.getItem("codingInterviewPreflightVerified") === "true";

  useEffect(() => {
    if (!sessionId || !preflightChecksPassed) {
      sessionStorage.removeItem("codingInterviewPreflightVerified");
      sessionStorage.removeItem("codingInterviewPreflightStage");
      sessionStorage.removeItem("codingInterviewSessionId");
      navigate("/coding-interview/new", { replace: true });
      return;
    }

    const camera = getInterviewCameraStream();
    const display = getInterviewDisplayStream();

    const cameraTrack = camera
      ?.getVideoTracks()
      .find((track) => track.readyState === "live");

    const displayTrack = display
      ?.getVideoTracks()
      .find((track) => track.readyState === "live");

    let disposed = false;
    let faceDetector: FaceDetector | null = null;
    let rafId = 0;
    let noFaceSince: number | null = null;
    let lastDetectionAt = 0;
    let detectionBusy = false;

    const terminate = async (reason: string) => {
      if (terminatedRef.current || disposed) return;

      terminatedRef.current = true;
      setFaceCountdown(null);
      setFullscreenWarning(null);
      setTerminationMessage(null);

      sessionStorage.removeItem("codingInterviewPreflightVerified");
      sessionStorage.removeItem("codingInterviewPreflightStage");
      sessionStorage.removeItem("codingInterviewSessionId");

      try {
        await abandonCodingInterview(Number(sessionId));
      } catch {
        // Continue termination even if saving fails.
      } finally {
        stopInterviewSetupMedia();

        try {
          if (document.fullscreenElement) {
            await document.exitFullscreen();
          }
        } catch {
          // The browser may already have exited fullscreen.
        }

        navigate("/home", {
          replace: true,
          state: {
            codingInterviewEnded: true,
            reason,
          },
        });
      }
    };

    terminateRef.current = (reason: string) => {
      void terminate(reason);
    };

    const onVisibilityChange = () => {
      if (document.visibilityState === "hidden") {
        pendingTabChangeRef.current = true;
        return;
      }

      if (
        document.visibilityState === "visible" &&
        pendingTabChangeRef.current
      ) {
        pendingTabChangeRef.current = false;

        setFullscreenWarning(null);
        setTerminationMessage(
          "Your interview is terminated because you have changed the tab."
        );
      }
    };

    const onFullscreenChange = () => {
      if (
        terminatedRef.current ||
        disposed ||
        document.fullscreenElement
      ) {
        return;
      }

      fullscreenExitCountRef.current += 1;
      const count = fullscreenExitCountRef.current;

      if (count >= 3) {
        setFullscreenWarning(null);
        setTerminationMessage(
          "Your interview is terminated because you have closed the full screen for the 3rd time."
        );
      } else {
        setFullscreenWarning(
          `Warning ${count} of 2: You exited fullscreen. Return to fullscreen to continue. A third exit will end the interview.`
        );
      }
    };

    const onDisplayEnded = () => {
      void terminate(
        "The interview ended because screen sharing was stopped."
      );
    };

    const onCameraEnded = () => {
      void terminate(
        "The interview ended because the camera was stopped."
      );
    };

    if (!cameraTrack || !displayTrack) {
      void terminate(
        "The required camera or screen-sharing stream was unavailable."
      );

      return () => {
        disposed = true;
        terminateRef.current = () => undefined;

        try {
          camera?.getTracks().forEach((track) => track.stop());
          display?.getTracks().forEach((track) => track.stop());
        } catch {
          // Continue cleanup if streams are already stopped.
        }

        stopInterviewSetupMedia();
      };
    }

    cameraTrack.addEventListener("ended", onCameraEnded);
    displayTrack.addEventListener("ended", onDisplayEnded);

    document.addEventListener(
      "visibilitychange",
      onVisibilityChange
    );
    document.addEventListener(
      "fullscreenchange",
      onFullscreenChange
    );

    const video = videoRef.current;

    if (video && camera) {
      video.srcObject = camera;
      video.muted = true;
      video.playsInline = true;
      void video.play().catch(() => undefined);
    }

    const runDetection = async (
      now: number
    ): Promise<void> => {
      if (disposed || terminatedRef.current) return;

      const target = videoRef.current;

      if (
        target &&
        faceDetector &&
        target.readyState >=
          HTMLMediaElement.HAVE_CURRENT_DATA &&
        !detectionBusy &&
        now - lastDetectionAt >= 200
      ) {
        detectionBusy = true;
        lastDetectionAt = now;

        try {
          const result = faceDetector.detectForVideo(
            target,
            now
          );

          if (result.detections.length > 0) {
            noFaceSince = null;
            setFaceCountdown(null);
          } else {
            if (noFaceSince === null) {
              noFaceSince = now;
            }

            const elapsed = now - noFaceSince;
            const remainingMs = Math.max(
              0,
              FACE_TIMEOUT_MS - elapsed
            );
            const remainingSeconds = Math.ceil(
              remainingMs / 1000
            );

            setFaceCountdown(remainingSeconds);

            if (remainingMs <= 0) {
              setFaceCountdown(null);

              void terminate(
                "The interview ended because no face was detected for 5 consecutive seconds."
              );
            }
          }
        } catch {
          // Ignore temporary detection or frame errors.
        } finally {
          detectionBusy = false;
        }
      }

      if (!disposed && !terminatedRef.current) {
        rafId = window.requestAnimationFrame((time) => {
          void runDetection(time);
        });
      }
    };

    const initialiseDetector = async () => {
      try {
        const vision = await FilesetResolver.forVisionTasks(
          "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.1.0/wasm"
        );

        if (disposed || terminatedRef.current) return;

        faceDetector = await FaceDetector.createFromOptions(
          vision,
          {
            baseOptions: {
              modelAssetPath:
                "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite",
            },
            runningMode: "VIDEO",
            minDetectionConfidence: 0.5,
          }
        );

        if (!disposed && !terminatedRef.current) {
          rafId = window.requestAnimationFrame((time) => {
            void runDetection(time);
          });
        }
      } catch {
        void terminate(
          "Face detection could not start. Check your internet connection and restart the interview."
        );
      }
    };

    void initialiseDetector();

    return () => {
      disposed = true;

      window.cancelAnimationFrame(rafId);
      faceDetector?.close();

      cameraTrack.removeEventListener(
        "ended",
        onCameraEnded
      );
      displayTrack.removeEventListener(
        "ended",
        onDisplayEnded
      );

      document.removeEventListener(
        "visibilitychange",
        onVisibilityChange
      );
      document.removeEventListener(
        "fullscreenchange",
        onFullscreenChange
      );

      // Do not stop camera/display streams in effect cleanup. React StrictMode
      // intentionally runs an extra setup/cleanup cycle in development; stopping
      // streams here would invalidate the next setup and incorrectly end the interview.
      // Media is stopped by terminate() when the interview actually ends.

      const currentVideo = videoRef.current;

      if (currentVideo) {
        currentVideo.pause();
        currentVideo.srcObject = null;
      }

      terminateRef.current = () => undefined;
    };
  }, [
    navigate,
    sessionId,
    state?.preflightChecksPassed,
  ]);

  return (
    <>
      <video
        ref={videoRef}
        className="pointer-events-none fixed h-px w-px opacity-0"
        autoPlay
        muted
        playsInline
        aria-hidden="true"
      />

      {faceCountdown !== null && !terminationMessage && (
        <div
          role="alert"
          aria-live="assertive"
          className="fixed left-1/2 top-3 z-[120] w-[calc(100%-2rem)] max-w-lg -translate-x-1/2 rounded-[20px] border border-rose-400/40 bg-[#4b071b] px-5 py-5 text-center text-white shadow-2xl"
        >
          <p className="text-sm font-semibold sm:text-base">
            Face not detected. Move back into the camera view.
          </p>

          <p className="mt-2 text-2xl font-bold sm:text-3xl">
            Interview ends in {faceCountdown}s
          </p>
        </div>
      )}

      {terminationMessage && (
        <div
          role="alertdialog"
          aria-modal="true"
          className="fixed inset-0 z-[130] flex items-center justify-center bg-black/80 p-5"
        >
          <div className="w-full max-w-md rounded-2xl border border-red-400/40 bg-slate-950 p-6 shadow-2xl">
            <h2 className="text-lg font-semibold text-red-300">
              Interview terminated
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-200">
              {terminationMessage}
            </p>

            <button
              type="button"
              onClick={() =>
                terminateRef.current(terminationMessage)
              }
              className="mt-5 w-full rounded-xl bg-red-500 px-4 py-3 text-sm font-semibold text-white hover:bg-red-400"
            >
              End interview
            </button>
          </div>
        </div>
      )}

      {fullscreenWarning && !terminationMessage && (
        <div
          role="alertdialog"
          aria-modal="true"
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 p-5"
        >
          <div className="w-full max-w-md rounded-2xl border border-amber-300/30 bg-slate-950 p-6 shadow-2xl">
            <h2 className="text-lg font-semibold text-amber-200">
              Fullscreen warning
            </h2>

            <p className="mt-3 text-sm leading-6 text-slate-300">
              {fullscreenWarning}
            </p>

            <button
              type="button"
              onClick={async () => {
                try {
                  if (!document.fullscreenElement) {
                    await document.documentElement.requestFullscreen();
                  }
                } catch {
                  // The browser may refuse the fullscreen request.
                }

                setFullscreenWarning(null);
              }}
              className="mt-5 w-full rounded-xl bg-violet-400 px-4 py-3 text-sm font-semibold text-slate-950 hover:bg-violet-300"
            >
              Return to interview
            </button>
          </div>
        </div>
      )}

      <CodingInterview />
    </>
  );
}
