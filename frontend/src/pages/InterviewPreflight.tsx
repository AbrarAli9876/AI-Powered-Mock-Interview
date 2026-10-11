import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { createInterview, type Difficulty } from "../lib/api";
import {
  getInterviewCameraStream,
  getInterviewDisplayStream,
  setInterviewCameraStream,
  setInterviewDisplayStream,
  stopInterviewSetupMedia,
} from "../lib/interviewMedia";
import {
  getIsExtended,
  inspectDisplayStream,
  isCameraLive,
  isVirtualCameraLabel,
  subscribeScreenChange,
  verifyEnvironment,
  waitForVideoFrame,
  type CheckId,
} from "../lib/proctoring";

type Setup = {
  topicId: number;
  startingDifficulty: Difficulty;
  questionCount: 10 | 15 | 20;
};

type PreflightStep = "fullscreen" | "camera" | "screen" | "ready";
type CameraDevice = { deviceId: string; label: string };

const stepOrder: PreflightStep[] = ["fullscreen", "camera", "screen", "ready"];
const stepDetails: Record<PreflightStep, { number: string; title: string; description: string }> = {
  fullscreen: {
    number: "01 / 04",
    title: "Enter fullscreen",
    description: "Fullscreen is required before the camera and screen-sharing checks.",
  },
  camera: {
    number: "02 / 04",
    title: "Enable your camera",
    description: "Allow camera access and confirm that your live preview is working. Virtual cameras are not accepted.",
  },
  screen: {
    number: "03 / 04",
    title: "Share your entire screen",
    description: "Select Entire Screen in the browser prompt. Window and tab sharing are rejected, and you can't switch sources once sharing starts.",
  },
  ready: {
    number: "04 / 04",
    title: "Verify and start",
    description: "Every check is run again right before your interview session is created.",
  },
};

function readSetup(): Setup | null {
  try {
    const raw = sessionStorage.getItem("technicalInterviewSetup");
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Setup;
    if (
      !Number.isInteger(parsed.topicId) ||
      !["easy", "medium", "hard"].includes(parsed.startingDifficulty) ||
      ![10, 15, 20].includes(parsed.questionCount)
    ) return null;
    return parsed;
  } catch {
    return null;
  }
}

/**
 * Which step the candidate may be on, derived from the REAL state of the media streams.
 * There is no stored "stage" flag to edit in DevTools: if the streams aren't valid, you can't be ahead.
 */
function furthestAllowedStep(): PreflightStep {
  const cameraOk = isCameraLive(getInterviewCameraStream());
  const screenOk = !inspectDisplayStream(getInterviewDisplayStream());
  if (cameraOk && screenOk) return "ready"; // fullscreen can be re-entered on this step
  if (cameraOk) return "screen";
  return document.fullscreenElement ? "camera" : "fullscreen";
}

function stepForFailure(id: CheckId): PreflightStep {
  if (id === "fullscreen") return "fullscreen";
  if (id === "camera" || id === "virtual-camera") return "camera";
  return "screen";
}

export default function InterviewPreflight() {
  const { step: routeStep } = useParams<{ step: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const cameraRef = useRef<HTMLVideoElement | null>(null);
  const screenRef = useRef<HTMLVideoElement | null>(null);
  const screenPickerOpenRef = useRef(false);
  const startedRef = useRef(false);
  const [error, setError] = useState<string | null>(null);
  const [cameraBusy, setCameraBusy] = useState(false);
  const [screenBusy, setScreenBusy] = useState(false);
  const [starting, setStarting] = useState(false);
  const [singleDisplayConfirmed, setSingleDisplayConfirmed] = useState(false);
  const [cameraDevices, setCameraDevices] = useState<CameraDevice[]>([]);
  const [selectedCameraId, setSelectedCameraId] = useState("");
  const [tick, setTick] = useState(0);
  const bump = useCallback(() => setTick((value) => value + 1), []);

  const step = useMemo<PreflightStep | null>(
    () => (stepOrder.includes(routeStep as PreflightStep) ? (routeStep as PreflightStep) : null),
    [routeStep],
  );
  const setup = useMemo<Setup | null>(
    () => (location.state as { setup?: Setup } | null)?.setup ?? readSetup(),
    [location.state],
  );

  // Derived on every render from the live streams, never from cached booleans.
  const env = verifyEnvironment({ requireFullscreen: true });
  const cameraReady = isCameraLive(getInterviewCameraStream());
  const screenReady = !inspectDisplayStream(getInterviewDisplayStream());
  const fullscreenReady = Boolean(document.fullscreenElement);
  const displayUnverifiable = getIsExtended() === undefined;

  const goTo = (next: PreflightStep) => {
    setError(null);
    navigate(`/interviews/preflight/${next}`, { replace: false, state: { setup: setup ?? undefined } });
  };

  // Re-render on anything that can change the verification result.
  useEffect(() => {
    const interval = window.setInterval(bump, 1000);
    document.addEventListener("fullscreenchange", bump);
    const unsubscribeScreen = subscribeScreenChange(bump);
    return () => {
      window.clearInterval(interval);
      document.removeEventListener("fullscreenchange", bump);
      unsubscribeScreen();
    };
  }, [bump]);

  // Gate: a candidate can't be on a step the real state doesn't support.
  useEffect(() => {
    if (!setup || !step) {
      navigate("/interviews/new", { replace: true });
      return;
    }
    if (screenPickerOpenRef.current || starting) return;
    const allowed = furthestAllowedStep();
    if (stepOrder.indexOf(step) > stepOrder.indexOf(allowed)) {
      navigate(`/interviews/preflight/${allowed}`, { replace: true, state: { setup } });
    }
  }, [setup, step, tick, starting, navigate]);

  // Release the camera/screen if the candidate leaves without starting.
  useEffect(() => () => {
    if (!startedRef.current) stopInterviewSetupMedia();
  }, []);

  // Attach previews.
  useEffect(() => {
    const attach = async (element: HTMLVideoElement | null, stream: MediaStream | null) => {
      if (!element || !stream) return;
      if (element.srcObject !== stream) element.srcObject = stream;
      element.muted = true;
      element.playsInline = true;
      try { await element.play(); } catch { /* the candidate can click the preview to resume */ }
    };
    void attach(cameraRef.current, getInterviewCameraStream());
    void attach(screenRef.current, getInterviewDisplayStream());
  }, [step, cameraReady, screenReady]);

  // React instantly when a track ends.
  useEffect(() => {
    const camera = getInterviewCameraStream();
    const display = getInterviewDisplayStream();
    const onCameraEnded = () => {
      setError("Camera access stopped. Enable the camera again before continuing.");
      bump();
    };
    const onCameraMuted = () => bump();
    const onDisplayEnded = () => {
      setInterviewDisplayStream(null);
      setError("Screen sharing stopped. Share your entire screen again to continue.");
      bump();
    };
    camera?.getVideoTracks().forEach((t) => {
      t.addEventListener("ended", onCameraEnded);
      t.addEventListener("mute", onCameraMuted);
      t.addEventListener("unmute", onCameraMuted);
    });
    display?.getVideoTracks().forEach((t) => t.addEventListener("ended", onDisplayEnded));
    return () => {
      camera?.getVideoTracks().forEach((t) => {
        t.removeEventListener("ended", onCameraEnded);
        t.removeEventListener("mute", onCameraMuted);
        t.removeEventListener("unmute", onCameraMuted);
      });
      display?.getVideoTracks().forEach((t) => t.removeEventListener("ended", onDisplayEnded));
    };
  }, [bump, cameraReady, screenReady]);

  const refreshCameraDevices = async () => {
    if (!navigator.mediaDevices?.enumerateDevices) return;
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const cameras = devices
        .filter((device) => device.kind === "videoinput" && !isVirtualCameraLabel(device.label))
        .map((device, index) => ({ deviceId: device.deviceId, label: device.label || `Camera ${index + 1}` }));
      setCameraDevices(cameras);
      const activeId = getInterviewCameraStream()?.getVideoTracks()[0]?.getSettings().deviceId;
      setSelectedCameraId((current) => {
        if (current && cameras.some((c) => c.deviceId === current)) return current;
        if (activeId && cameras.some((c) => c.deviceId === activeId)) return activeId;
        return cameras[0]?.deviceId ?? "";
      });
    } catch {
      setCameraDevices([]);
    }
  };

  useEffect(() => {
    if (step === "camera") void refreshCameraDevices();
  }, [step]);

  const handleFullscreen = async () => {
    setError(null);
    if (!document.fullscreenEnabled) {
      setError("Fullscreen is unavailable in this browser. Please use Chrome or Edge.");
      return;
    }
    try {
      if (!document.fullscreenElement) await document.documentElement.requestFullscreen({ navigationUI: "hide" });
      if (!document.fullscreenElement) throw new Error("Fullscreen could not be enabled.");
      bump();
      if (step === "fullscreen") goTo("camera");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Fullscreen permission was not granted.");
    }
  };

  const handleCamera = async () => {
    setError(null);

    // Already live on the selected device: confirm and continue.
    const activeStream = getInterviewCameraStream();
    const activeDeviceId = activeStream?.getVideoTracks()[0]?.getSettings().deviceId;
    if (
      isCameraLive(activeStream) &&
      !isVirtualCameraLabel(activeStream?.getVideoTracks()[0]?.label) &&
      (!selectedCameraId || !activeDeviceId || activeDeviceId === selectedCameraId)
    ) {
      goTo("screen");
      return;
    }

    setCameraBusy(true);
    let candidate: MediaStream | null = null;
    try {
      if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error("Camera access requires a supported browser on HTTPS or localhost.");
      }
      const video: MediaTrackConstraints = selectedCameraId ? { deviceId: { exact: selectedCameraId } } : {};
      candidate = await navigator.mediaDevices.getUserMedia({ video, audio: false });
      const track = candidate.getVideoTracks()[0];
      if (!track || track.readyState !== "live") throw new Error("No active camera was detected.");
      if (isVirtualCameraLabel(track.label)) {
        throw new Error(`"${track.label}" looks like a virtual camera. Select a physical camera.`);
      }

      const element = cameraRef.current;
      if (!element) throw new Error("Camera preview is unavailable. Reload the page and try again.");
      element.srcObject = candidate;
      element.muted = true;
      element.playsInline = true;
      try { await element.play(); } catch {
        throw new Error("The camera was detected, but its preview could not start. Close other apps using the camera and try again.");
      }
      if (!(await waitForVideoFrame(element))) {
        throw new Error("The camera isn't sending video. Check that it isn't covered or in use by another app.");
      }

      const previous = getInterviewCameraStream();
      if (previous && previous !== candidate) previous.getTracks().forEach((t) => t.stop());
      setInterviewCameraStream(candidate);
      candidate = null; // ownership moved to the store
      await refreshCameraDevices(); // labels are available now, so virtual devices get filtered out
      bump();
    } catch (err) {
      candidate?.getTracks().forEach((t) => t.stop());
      if (cameraRef.current && cameraRef.current.srcObject === candidate) cameraRef.current.srcObject = null;
      setError(err instanceof Error ? err.message : "Camera permission was denied or the camera is unavailable.");
    } finally {
      setCameraBusy(false);
    }
  };

  const handleScreenShare = async () => {
    setError(null);
    if (!isCameraLive(getInterviewCameraStream())) {
      setError("Enable the camera first.");
      goTo("camera");
      return;
    }
    if (getIsExtended() === true) {
      setError("More than one display is connected. Disconnect the extra monitors, then share your screen.");
      return;
    }
    setScreenBusy(true);
    let stream: MediaStream | null = null;
    try {
      if (!navigator.mediaDevices?.getDisplayMedia) throw new Error("Screen sharing is unavailable in this browser.");
      // Chrome drops fullscreen while its picker is open. That is expected, not a violation.
      screenPickerOpenRef.current = true;
      stream = await navigator.mediaDevices.getDisplayMedia({
        video: { displaySurface: "monitor" } as MediaTrackConstraints,
        audio: false,
        preferCurrentTab: false,
        selfBrowserSurface: "exclude",
        // Stops the candidate switching the shared source to a window/tab after approval.
        surfaceSwitching: "exclude",
        monitorTypeSurfaces: "include",
      } as DisplayMediaStreamOptions);

      const failure = inspectDisplayStream(stream);
      if (failure) throw new Error(failure.message);

      const previous = getInterviewDisplayStream();
      if (previous && previous !== stream) previous.getTracks().forEach((t) => t.stop());
      setInterviewDisplayStream(stream);
      stream = null; // ownership moved to the store

      if (screenRef.current) {
        screenRef.current.srcObject = getInterviewDisplayStream();
        await screenRef.current.play().catch(() => undefined);
      }
      if (!document.fullscreenElement) {
        try { await document.documentElement.requestFullscreen({ navigationUI: "hide" }); } catch { /* the Ready step offers a re-enter button */ }
      }
      goTo("ready");
    } catch (err) {
      stream?.getTracks().forEach((t) => t.stop());
      setError(err instanceof Error ? err.message : "Screen sharing was cancelled or failed.");
    } finally {
      screenPickerOpenRef.current = false;
      setScreenBusy(false);
      bump();
    }
  };

  const startInterview = async () => {
    setError(null);
    if (starting) return;
    if (!setup) {
      setError("Your interview configuration is missing. Please configure your interview again.");
      return;
    }

    // Final, independent re-verification of every requirement.
    const result = verifyEnvironment({ requireFullscreen: true });
    if (!result.ok) {
      const first = result.failures[0];
      goTo(stepForFailure(first.id));
      setError(first.message);
      return;
    }
    if (displayUnverifiable && !singleDisplayConfirmed) {
      setError("Confirm that you are using only one display.");
      return;
    }

    setStarting(true);
    try {
      const evidence = { ...result.evidence, singleDisplayAttested: displayUnverifiable ? singleDisplayConfirmed : undefined };
      // The server must treat this as a claim to cross-check, never as proof.
      const interview = await createInterview(setup.topicId, setup.startingDifficulty, setup.questionCount, evidence);
      startedRef.current = true;
      sessionStorage.setItem("technicalInterviewPreflightVerified", "true");
      navigate(`/interviews/${interview.id}`, { replace: true, state: { preflightChecksPassed: true } });
    } catch (err) {
      sessionStorage.removeItem("technicalInterviewPreflightVerified");
      setError(err instanceof Error ? err.message : "Unable to start the interview.");
    } finally {
      setStarting(false);
    }
  };

  if (!setup || !step) return null;
  const details = stepDetails[step];

  const rows: [string, CheckId[]][] = [
    ["Fullscreen", ["fullscreen"]],
    ["Camera", ["camera", "virtual-camera"]],
    ["Entire screen", ["screen-ended", "screen-surface"]],
    ["Single display", ["multi-display"]],
  ];
  const rowPassed = (ids: CheckId[]) => {
    const clear = !env.failures.some((f) => ids.includes(f.id));
    return ids.includes("multi-display") && displayUnverifiable ? clear && singleDisplayConfirmed : clear;
  };
  const canStart = env.ok && (!displayUnverifiable || singleDisplayConfirmed) && !starting;

  return (
    <div className="app-background min-h-screen px-5 py-8 sm:px-8">
      <main className="mx-auto flex min-h-[85vh] w-full max-w-3xl items-center justify-center">
        <section className="glass-panel w-full rounded-3xl border border-white/[0.07] p-6 sm:p-9">
          <div className="flex items-center justify-between gap-2">
            <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-violet-400">Technical interview · Security check</p>
            <span className="text-xs text-slate-500">{details.number}</span>
          </div>
          <div className="mt-5 grid grid-cols-4 gap-2" aria-label="Pre-interview progress">
            {stepOrder.map((item, index) => {
              const current = item === step;
              const complete = stepOrder.indexOf(step) > index;
              return <div key={item} className={`h-1.5 rounded-full ${current ? "bg-violet-400" : complete ? "bg-cyan-300" : "bg-white/10"}`} />;
            })}
          </div>
          <h1 className="mt-7 font-display text-3xl font-semibold tracking-tight text-white sm:text-4xl">{details.title}</h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">{details.description}</p>
          {error && <div role="alert" className="mt-5 rounded-2xl border border-rose-400/20 bg-rose-400/[0.06] px-4 py-3 text-sm leading-6 text-rose-200">{error}</div>}

          {step === "fullscreen" && <>
            <div className="mt-7 rounded-2xl border border-white/[0.07] bg-black/20 p-8 text-center">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-violet-400/10 text-violet-300"><span className="text-3xl">⛶</span></div>
              <p className="mt-4 text-sm font-medium text-white">Fullscreen is mandatory</p>
              <p className="mt-2 text-xs leading-5 text-slate-500">Click the button below and allow the browser to enter fullscreen. You cannot continue until fullscreen is active.</p>
            </div>
            <button type="button" onClick={() => void handleFullscreen()} className="mt-6 w-full rounded-2xl bg-violet-400 px-5 py-4 text-sm font-semibold text-slate-950 transition hover:bg-violet-300">Enter fullscreen →</button>
          </>}

          {step === "camera" && <>
            <div className="mt-7 flex flex-col gap-3 sm:flex-row">
              <label className="flex-1 text-sm font-medium text-slate-300" htmlFor="interview-camera-device">Select camera
                <select id="interview-camera-device" value={selectedCameraId} onChange={(event) => setSelectedCameraId(event.target.value)} className="mt-2 w-full rounded-2xl border border-white/[0.12] bg-slate-950 px-4 py-4 text-sm text-white outline-none focus:border-violet-400" disabled={cameraBusy}>
                  {cameraDevices.length === 0 && <option value="">Default camera</option>}
                  {cameraDevices.map((camera) => <option key={camera.deviceId} value={camera.deviceId}>{camera.label}</option>)}
                </select>
              </label>
              <button type="button" onClick={() => void refreshCameraDevices()} className="self-end rounded-2xl border border-white/[0.12] px-4 py-4 text-sm text-slate-300 hover:text-white" disabled={cameraBusy}>Refresh cameras</button>
            </div>
            <p className="mt-2 text-xs text-slate-500">Camera names may appear only after browser permission is granted. Virtual cameras are hidden and rejected.</p>
            <div className="mt-5 overflow-hidden rounded-2xl border border-white/[0.08] bg-black/30">
              <video ref={cameraRef} autoPlay muted playsInline onClick={() => { void cameraRef.current?.play().catch(() => setError("Camera preview could not start. Check browser camera permissions and close other apps using the camera.")); }} className="aspect-video max-h-[420px] w-full bg-slate-950 object-cover" aria-label="Camera preview" />
            </div>
            <p className="mt-3 text-xs text-slate-500">The camera must stay active for the whole interview. If it stops, the interview ends.</p>
            <button type="button" disabled={cameraBusy} onClick={() => void handleCamera()} className="mt-6 w-full rounded-2xl bg-violet-400 px-5 py-4 text-sm font-semibold text-slate-950 transition hover:bg-violet-300 disabled:opacity-50">{cameraBusy ? "Requesting camera…" : cameraReady ? "Confirm camera and continue →" : "Allow camera →"}</button>
          </>}

          {step === "screen" && <>
            <div className="mt-7 grid gap-3 sm:grid-cols-3">
              <div className="rounded-2xl border border-cyan-300/30 bg-cyan-300/[0.06] p-4 text-center"><div className="text-xl text-cyan-200">▣</div><p className="mt-2 text-sm font-semibold text-white">Entire screen</p><p className="mt-1 text-xs text-cyan-200">Required</p></div>
              <div className="rounded-2xl border border-white/[0.06] bg-black/10 p-4 text-center opacity-50"><div className="text-xl text-slate-400">▤</div><p className="mt-2 text-sm font-semibold text-white">Window</p><p className="mt-1 text-xs text-slate-500">Not allowed</p></div>
              <div className="rounded-2xl border border-white/[0.06] bg-black/10 p-4 text-center opacity-50"><div className="text-xl text-slate-400">▱</div><p className="mt-2 text-sm font-semibold text-white">Browser tab</p><p className="mt-1 text-xs text-slate-500">Not allowed</p></div>
            </div>
            <div className="mt-5 overflow-hidden rounded-2xl border border-white/[0.08] bg-black/30"><video ref={screenRef} autoPlay muted playsInline className="aspect-video max-h-[360px] w-full bg-slate-950 object-contain" aria-label="Screen share preview" /></div>
            <button type="button" disabled={screenBusy || !cameraReady} onClick={() => void handleScreenShare()} className="mt-6 w-full rounded-2xl bg-violet-400 px-5 py-4 text-sm font-semibold text-slate-950 transition hover:bg-violet-300 disabled:opacity-50">{screenBusy ? "Opening browser picker…" : screenReady ? "Share entire screen again →" : "Share entire screen →"}</button>
          </>}

          {step === "ready" && <>
            <div className="mt-7 grid gap-3 sm:grid-cols-2">
              {rows.map(([label, ids]) => {
                const passed = rowPassed(ids);
                return <div key={label} className="flex items-center gap-3 rounded-2xl border border-white/[0.07] bg-black/10 p-4"><span className={`flex h-8 w-8 items-center justify-center rounded-full ${passed ? "bg-cyan-300/10 text-cyan-200" : "bg-rose-400/10 text-rose-200"}`}>{passed ? "✓" : "!"}</span><div><p className="text-sm font-medium text-white">{label}</p><p className={`mt-1 text-xs ${passed ? "text-cyan-200" : "text-rose-200"}`}>{passed ? "Ready" : "Required"}</p></div></div>;
              })}
            </div>
            {env.failures.length > 0 && (
              <ul className="mt-4 space-y-1 text-xs leading-5 text-rose-200">
                {env.failures.map((f) => <li key={f.id}>{f.message}</li>)}
              </ul>
            )}
            {displayUnverifiable && (
              <label className="mt-5 flex cursor-pointer items-start gap-3 rounded-2xl border border-white/[0.07] bg-black/10 p-4 text-sm leading-6 text-slate-300"><input type="checkbox" checked={singleDisplayConfirmed} onChange={(event) => setSingleDisplayConfirmed(event.target.checked)} className="mt-1 accent-violet-400" /><span>This browser can't count displays. I confirm that I am using only one display.</span></label>
            )}
            {!fullscreenReady && <button type="button" onClick={() => void handleFullscreen()} className="mt-5 w-full rounded-2xl border border-violet-300/30 px-5 py-3 text-sm font-semibold text-violet-200 hover:bg-violet-400/10">Re-enter fullscreen to continue</button>}
            <button type="button" disabled={!canStart} onClick={() => void startInterview()} className="mt-6 w-full rounded-2xl bg-violet-400 px-5 py-4 text-sm font-semibold text-slate-950 transition hover:bg-violet-300 disabled:cursor-not-allowed disabled:opacity-40">{starting ? "Starting interview…" : "All checks complete — Start interview →"}</button>
          </>}

          <div className="mt-6 border-t border-white/[0.07] pt-5"><button type="button" onClick={() => {
            setError(null);
            if (step === "fullscreen") {
              stopInterviewSetupMedia();
              sessionStorage.removeItem("technicalInterviewPreflightVerified");
              navigate("/interviews/new");
            } else {
              const previous = stepOrder[stepOrder.indexOf(step) - 1];
              if (previous) goTo(previous);
            }
          }} className="rounded-xl border border-white/[0.08] px-4 py-2.5 text-sm text-slate-400 transition hover:text-white">← {step === "fullscreen" ? "Back to configuration" : "Previous step"}</button></div>
        </section>
      </main>
    </div>
  );
} 