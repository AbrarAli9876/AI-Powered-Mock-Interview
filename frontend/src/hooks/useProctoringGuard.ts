import { useEffect, useRef, useState } from "react";
import { subscribeScreenChange, verifyEnvironment, type CheckId } from "../lib/proctoring";

export type ViolationType =
  | "fullscreen-exit"
  | "camera-stopped"
  | "virtual-camera"
  | "screen-stopped"
  | "screen-not-monitor"
  | "multi-display"
  | "tab-hidden"
  | "window-blur"
  | "clipboard"
  | "devtools-shortcut";

export interface Violation {
  type: ViolationType;
  severity: "warning" | "fatal";
  at: string;
  detail?: string;
}

/** Fatal = the interview cannot continue fairly. Warning = counted, shown to the candidate. */
const SEVERITY: Record<ViolationType, Violation["severity"]> = {
  "fullscreen-exit": "warning",
  "tab-hidden": "warning",
  "window-blur": "warning",
  clipboard: "warning",
  "devtools-shortcut": "warning",
  "camera-stopped": "fatal",
  "virtual-camera": "fatal",
  "screen-stopped": "fatal",
  "screen-not-monitor": "fatal",
  "multi-display": "fatal",
};

const CHECK_TO_VIOLATION: Record<CheckId, ViolationType> = {
  fullscreen: "fullscreen-exit",
  camera: "camera-stopped",
  "virtual-camera": "virtual-camera",
  "screen-ended": "screen-stopped",
  "screen-surface": "screen-not-monitor",
  "multi-display": "multi-display",
};

interface Options {
  enabled: boolean;
  /** Called for every violation. Send it to the server and decide whether to end the interview. */
  onViolation: (violation: Violation) => void;
  /** Block copy / cut / paste / right-click. Turn off if your interview needs pasting. */
  blockClipboard?: boolean;
  heartbeatMs?: number;
}

export function useProctoringGuard({
  enabled,
  onViolation,
  blockClipboard = true,
  heartbeatMs = 2000,
}: Options) {
  const handlerRef = useRef(onViolation);
  handlerRef.current = onViolation;
  const [violations, setViolations] = useState<Violation[]>([]);

  useEffect(() => {
    if (!enabled) return;

    const active = new Set<ViolationType>();
    let blurTimer: number | undefined;

    const report = (type: ViolationType, detail?: string) => {
      const violation: Violation = { type, severity: SEVERITY[type], at: new Date().toISOString(), detail };
      setViolations((previous) => [...previous, violation]);
      handlerRef.current(violation);
    };

    // State-based checks: reported once when they start failing, again only after they recover.
    const heartbeat = () => {
      const failing = new Set<ViolationType>();
      for (const failure of verifyEnvironment({ requireFullscreen: true }).failures) {
        const type = CHECK_TO_VIOLATION[failure.id];
        failing.add(type);
        if (!active.has(type)) {
          active.add(type);
          report(type, failure.message);
        }
      }
      for (const type of [...active]) if (!failing.has(type)) active.delete(type);
    };

    const onVisibility = () => {
      if (document.visibilityState === "hidden") report("tab-hidden");
    };
    const onBlur = () => {
      window.clearTimeout(blurTimer);
      blurTimer = window.setTimeout(() => {
        if (!document.hasFocus()) report("window-blur");
      }, 400);
    };
    const onFocus = () => window.clearTimeout(blurTimer);

    const onClipboard = (event: Event) => {
      event.preventDefault();
      report("clipboard", event.type);
    };
    const onKeyDown = (event: KeyboardEvent) => {
      const key = event.key.toLowerCase();
      const mod = event.ctrlKey || event.metaKey;
      const devtools =
        event.key === "F12" ||
        (mod && event.shiftKey && ["i", "j", "c"].includes(key)) ||
        (mod && key === "u") ||
        (event.metaKey && event.altKey && ["i", "j", "c", "u"].includes(key));
      if (devtools) {
        event.preventDefault();
        report("devtools-shortcut", event.key);
      }
    };
    const onBeforeUnload = (event: BeforeUnloadEvent) => {
      event.preventDefault();
      event.returnValue = "";
    };

    const interval = window.setInterval(heartbeat, heartbeatMs);
    heartbeat();

    document.addEventListener("fullscreenchange", heartbeat);
    const unsubscribeScreen = subscribeScreenChange(heartbeat); // fires when a monitor is plugged in (Chromium)
    navigator.mediaDevices?.addEventListener?.("devicechange", heartbeat);
    document.addEventListener("visibilitychange", onVisibility);
    window.addEventListener("blur", onBlur);
    window.addEventListener("focus", onFocus);
    window.addEventListener("keydown", onKeyDown, true);
    window.addEventListener("beforeunload", onBeforeUnload);
    if (blockClipboard) {
      for (const name of ["copy", "cut", "paste", "contextmenu"]) document.addEventListener(name, onClipboard);
    }

    return () => {
      window.clearInterval(interval);
      window.clearTimeout(blurTimer);
      document.removeEventListener("fullscreenchange", heartbeat);
      unsubscribeScreen();
      navigator.mediaDevices?.removeEventListener?.("devicechange", heartbeat);
      document.removeEventListener("visibilitychange", onVisibility);
      window.removeEventListener("blur", onBlur);
      window.removeEventListener("focus", onFocus);
      window.removeEventListener("keydown", onKeyDown, true);
      window.removeEventListener("beforeunload", onBeforeUnload);
      for (const name of ["copy", "cut", "paste", "contextmenu"]) document.removeEventListener(name, onClipboard);
    };
  }, [enabled, blockClipboard, heartbeatMs]);

  return {
    violations,
    warningCount: violations.filter((v) => v.severity === "warning").length,
  };
}