import { getInterviewCameraStream, getInterviewDisplayStream } from "./interviewMedia";

export type CheckId =
  | "fullscreen"
  | "camera"
  | "virtual-camera"
  | "screen-ended"
  | "screen-surface"
  | "multi-display";

export interface CheckFailure {
  id: CheckId;
  message: string;
}

export interface PreflightEvidence {
  collectedAt: string;
  userAgent: string;
  fullscreen: boolean;
  displaySurface: string | null;
  capture: { width: number | null; height: number | null };
  screen: { width: number; height: number; devicePixelRatio: number; isExtended: boolean | null };
  camera: { label: string | null; deviceId: string | null };
  /** Only set when the browser could not report the display count itself. */
  singleDisplayAttested?: boolean;
}

type DisplaySettings = MediaTrackSettings & { displaySurface?: string };

// Heuristic only: labels are spoofable, but this blocks the common virtual-camera apps.
const VIRTUAL_CAMERA_PATTERN =
  /\bobs\b|virtual|manycam|snap camera|xsplit|droidcam|iriun|epoccam|ivcam|vcam|splitcam|youcam|nvidia broadcast|mmhmm|\bcamo\b|chromacam|loopback|fake/i;

export function isVirtualCameraLabel(label?: string | null): boolean {
  return Boolean(label && VIRTUAL_CAMERA_PATTERN.test(label));
}

export function isLiveVideo(stream: MediaStream | null | undefined): boolean {
  return Boolean(stream?.getVideoTracks().some((track) => track.readyState === "live"));
}

/** Camera must be live, enabled and actually delivering frames (not muted by the OS/driver). */
export function isCameraLive(stream: MediaStream | null | undefined): boolean {
  return Boolean(
    stream?.getVideoTracks().some((t) => t.readyState === "live" && t.enabled && !t.muted),
  );
}

/** true / false in Chromium (no permission needed); undefined where the browser can't tell. */
export function getIsExtended(): boolean | undefined {
  return (window.screen as Screen & { isExtended?: boolean }).isExtended;
}

/**
 * Fires when a monitor is plugged in or removed (Chromium). TypeScript's DOM types
 * don't declare events on `Screen`, so it is cast to EventTarget here, in one place.
 * Returns an unsubscribe function.
 */
export function subscribeScreenChange(handler: () => void): () => void {
  const target = window.screen as unknown as EventTarget;
  target.addEventListener?.("change", handler);
  return () => target.removeEventListener?.("change", handler);
}

/** Resolves true once the video element is rendering real frames. */
export function waitForVideoFrame(video: HTMLVideoElement, timeoutMs = 4000): Promise<boolean> {
  return new Promise((resolve) => {
    if (video.videoWidth > 0 && video.readyState >= 2) {
      resolve(true);
      return;
    }
    const finish = () => {
      window.clearTimeout(timer);
      video.removeEventListener("loadeddata", finish);
      resolve(video.videoWidth > 0);
    };
    const timer = window.setTimeout(finish, timeoutMs);
    video.addEventListener("loadeddata", finish);
  });
}

/** Returns a failure if the stream is not a live, entire-screen share of this display. */
export function inspectDisplayStream(stream: MediaStream | null): CheckFailure | null {
  const track = stream?.getVideoTracks()[0];
  if (!track || track.readyState !== "live") {
    return { id: "screen-ended", message: "Screen sharing is not active. Share your entire screen again." };
  }
  const settings = track.getSettings() as DisplaySettings;
  if (settings.displaySurface !== "monitor") {
    return {
      id: "screen-surface",
      message: settings.displaySurface
        ? "Window and tab sharing are not allowed. Share your entire screen."
        : "This browser doesn't report which source was shared, so it can't be verified. Use Chrome or Edge.",
    };
  }
  if (settings.width && settings.height) {
    const shared = settings.width / settings.height;
    const own = window.screen.width / window.screen.height;
    if (Math.abs(shared - own) / own > 0.05) {
      return {
        id: "screen-surface",
        message: "The shared screen doesn't match the display this page is on. Share the display showing this window.",
      };
    }
  }
  return null;
}

export function collectEvidence(): PreflightEvidence {
  const cameraTrack = getInterviewCameraStream()?.getVideoTracks()[0];
  const displayTrack = getInterviewDisplayStream()?.getVideoTracks()[0];
  const displaySettings = displayTrack?.getSettings() as DisplaySettings | undefined;
  return {
    collectedAt: new Date().toISOString(),
    userAgent: navigator.userAgent,
    fullscreen: Boolean(document.fullscreenElement),
    displaySurface: displaySettings?.displaySurface ?? null,
    capture: { width: displaySettings?.width ?? null, height: displaySettings?.height ?? null },
    screen: {
      width: window.screen.width,
      height: window.screen.height,
      devicePixelRatio: window.devicePixelRatio,
      isExtended: getIsExtended() ?? null,
    },
    camera: {
      label: cameraTrack?.label ?? null,
      deviceId: cameraTrack?.getSettings().deviceId ?? null,
    },
  };
}

/** Single source of truth used by the preflight page AND the in-interview guard. */
export function verifyEnvironment({ requireFullscreen = true } = {}) {
  const failures: CheckFailure[] = [];

  if (requireFullscreen && !document.fullscreenElement) {
    failures.push({ id: "fullscreen", message: "Fullscreen is required. Re-enter fullscreen to continue." });
  }

  const camera = getInterviewCameraStream();
  if (!isCameraLive(camera)) {
    failures.push({ id: "camera", message: "Your camera is off or not sending video. Enable it again." });
  } else if (isVirtualCameraLabel(camera?.getVideoTracks()[0]?.label)) {
    failures.push({ id: "virtual-camera", message: "A virtual camera was detected. Use a physical camera." });
  }

  const displayFailure = inspectDisplayStream(getInterviewDisplayStream());
  if (displayFailure) failures.push(displayFailure);

  if (getIsExtended() === true) {
    failures.push({ id: "multi-display", message: "More than one display is connected. Disconnect extra monitors." });
  }

  return { ok: failures.length === 0, failures, evidence: collectEvidence() };
}