import { useEffect, useRef, useState } from "react";
import { FaceDetector, FilesetResolver } from "@mediapipe/tasks-vision";
import { getInterviewCameraStream } from "../lib/interviewMedia";

export type PresenceStatus = "loading" | "ok" | "no-face" | "terminated" | "error";

// For production, copy these files into /public/mediapipe/ and point the URLs there
// so the interview doesn't depend on a third-party CDN.
const WASM_BASE = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm";
const MODEL_URL =
  "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite";

let detectorPromise: Promise<FaceDetector> | null = null;

/** Loads the model once. Call it early (e.g. on the preflight page) so the interview starts instantly. */
export function preloadFaceDetector(): Promise<FaceDetector> {
  if (!detectorPromise) {
    detectorPromise = (async () => {
      const vision = await FilesetResolver.forVisionTasks(WASM_BASE);
      const create = (delegate: "GPU" | "CPU") =>
        FaceDetector.createFromOptions(vision, {
          baseOptions: { modelAssetPath: MODEL_URL, delegate },
          runningMode: "VIDEO",
          minDetectionConfidence: 0.5,
        });
      try {
        return await create("GPU");
      } catch {
        return await create("CPU");
      }
    })();
    detectorPromise.catch(() => {
      detectorPromise = null; // allow a retry on the next mount
    });
  }
  return detectorPromise;
}

interface Options {
  enabled: boolean;
  /** Continuous time without a face before the interview is terminated. */
  graceMs?: number;
  /** A short miss (blink, glance down) is ignored; the alert appears after this long. */
  alertAfterMs?: number;
  intervalMs?: number;
  onTerminate: () => void;
  onError?: (error: Error) => void;
}

export function usePresenceDetection({
  enabled,
  graceMs = 5000,
  alertAfterMs = 700,
  intervalMs = 250,
  onTerminate,
  onError,
}: Options) {
  const terminateRef = useRef(onTerminate);
  terminateRef.current = onTerminate;
  const errorRef = useRef(onError);
  errorRef.current = onError;

  const [status, setStatus] = useState<PresenceStatus>("loading");
  const [secondsLeft, setSecondsLeft] = useState<number | null>(null);
  const [faceCount, setFaceCount] = useState(0);

  useEffect(() => {
    if (!enabled) return;

    let cancelled = false;
    let timer: number | undefined;
    let noFaceSince: number | null = null; // wall-clock, so background-tab throttling can't stretch the 5 s

    const video = document.createElement("video");
    video.muted = true;
    video.playsInline = true;

    const run = async () => {
      try {
        const stream = getInterviewCameraStream();
        if (!stream) throw new Error("Camera stream is not available.");
        video.srcObject = stream;
        await video.play();
        const detector = await preloadFaceDetector();
        if (cancelled) return;
        setStatus("ok");

        timer = window.setInterval(() => {
          if (video.readyState < 2 || video.videoWidth === 0) return;
          const now = Date.now();
          const count = detector.detectForVideo(video, performance.now()).detections.length;
          setFaceCount(count);

          if (count > 0) {
            noFaceSince = null;
            setStatus("ok");
            setSecondsLeft(null);
            return;
          }

          if (noFaceSince === null) noFaceSince = now;
          const elapsed = now - noFaceSince;

          if (elapsed >= graceMs) {
            window.clearInterval(timer);
            setStatus("terminated");
            setSecondsLeft(0);
            terminateRef.current();
            return;
          }
          if (elapsed >= alertAfterMs) {
            setStatus("no-face");
            setSecondsLeft(Math.ceil((graceMs - elapsed) / 1000));
          }
        }, intervalMs);
      } catch (err) {
        if (cancelled) return;
        setStatus("error");
        errorRef.current?.(err instanceof Error ? err : new Error(String(err)));
      }
    };

    void run();

    return () => {
      cancelled = true;
      window.clearInterval(timer);
      video.pause();
      video.srcObject = null;
    };
  }, [enabled, graceMs, alertAfterMs, intervalMs]);

  return { status, secondsLeft, faceCount };
}