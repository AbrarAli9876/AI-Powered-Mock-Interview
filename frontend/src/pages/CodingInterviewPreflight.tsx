import { useEffect, useMemo, useRef, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import {
  createCodingInterview,
  type CodingLanguage,
  type Difficulty,
} from "../lib/api";
import {
  getInterviewCameraStream,
  getInterviewDisplayStream,
  setInterviewCameraStream,
  setInterviewDisplayStream,
  stopInterviewSetupMedia,
} from "../lib/interviewMedia";

type Setup = {
  language: CodingLanguage;
  difficulty: Difficulty;
  questionCount: number;
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
    description: "Allow camera access and confirm that your live preview is working.",
  },
  screen: {
    number: "03 / 04",
    title: "Share your entire screen",
    description: "Select Entire Screen in the browser prompt. Window and tab sharing are not accepted when the browser identifies the source type.",
  },
  ready: {
    number: "04 / 04",
    title: "Verify and start",
    description: "All required checks are revalidated before your interview session is created.",
  },
};

function isLiveVideo(stream: MediaStream | null): boolean {
  return Boolean(stream?.getVideoTracks().some((track) => track.readyState === "live"));
}

function readSetup(): Setup | null {
  try {
    const raw = sessionStorage.getItem("codingInterviewSetup");
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Setup;
    if (
      !["python", "javascript", "java", "cpp", "sql"].includes(parsed.language) ||
      !["easy", "medium", "hard"].includes(parsed.difficulty) ||
      ![3, 5, 10].includes(parsed.questionCount)
    ) return null;
    return parsed;
  } catch {
    return null;
  }
}

export default function CodingInterviewPreflight() {
  const { step: routeStep } = useParams<{ step: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const cameraRef = useRef<HTMLVideoElement | null>(null);
  const screenRef = useRef<HTMLVideoElement | null>(null);
  const screenPickerOpenRef = useRef(false);
  const [error, setError] = useState<string | null>(null);
  const [cameraBusy, setCameraBusy] = useState(false);
  const [screenBusy, setScreenBusy] = useState(false);
  const [starting, setStarting] = useState(false);
  const [cameraReady, setCameraReady] = useState(isLiveVideo(getInterviewCameraStream()));
  const [screenReady, setScreenReady] = useState(isLiveVideo(getInterviewDisplayStream()));
  const [fullscreenReady, setFullscreenReady] = useState(Boolean(document.fullscreenElement));
  const [singleDisplayConfirmed, setSingleDisplayConfirmed] = useState(false);
  const [cameraDevices, setCameraDevices] = useState<CameraDevice[]>([]);
  const [selectedCameraId, setSelectedCameraId] = useState("");

  const step = useMemo<PreflightStep | null>(
    () => stepOrder.includes(routeStep as PreflightStep) ? routeStep as PreflightStep : null,
    [routeStep],
  );
  const setup = (location.state as { setup?: Setup } | null)?.setup ?? readSetup();

  const goTo = (next: PreflightStep) => {
    setError(null);
    sessionStorage.setItem("codingInterviewPreflightStage", next);
    navigate(`/coding-interview/preflight/${next}`, {
      replace: false,
      state: { setup: setup ?? undefined },
    });
  };

  useEffect(() => {
    if (!setup || !step) {
      navigate("/coding-interview/new", { replace: true });
      return;
    }

    const stage = sessionStorage.getItem("codingInterviewPreflightStage") as PreflightStep | null;
    const stageIndex = stage ? stepOrder.indexOf(stage) : -1;
    const requestedIndex = stepOrder.indexOf(step);

    // A candidate cannot jump ahead by manually entering a later URL.
    if (stageIndex < 0) {
      sessionStorage.setItem("codingInterviewPreflightStage", "fullscreen");
      navigate("/coding-interview/preflight/fullscreen", { replace: true, state: { setup } });
      return;
    }
    if (requestedIndex > stageIndex) {
      navigate(`/coding-interview/preflight/${stage}`, { replace: true, state: { setup } });
    }
  }, [setup, step, navigate]);

  useEffect(() => {
    const camera = getInterviewCameraStream();
    const display = getInterviewDisplayStream();
    setCameraReady(isLiveVideo(camera));
    setScreenReady(isLiveVideo(display));
    setFullscreenReady(Boolean(document.fullscreenElement));

    const attachPreview = async (element: HTMLVideoElement | null, stream: MediaStream | null) => {
      if (!element || !stream || !isLiveVideo(stream)) return;
      if (element.srcObject !== stream) element.srcObject = stream;
      element.muted = true;
      element.autoplay = true;
      element.playsInline = true;
      try {
        await element.play();
      } catch {
        // The candidate can interact with the page to resume playback if the browser blocks autoplay.
      }
    };
    void attachPreview(cameraRef.current, camera);
    void attachPreview(screenRef.current, display);
  }, [step, cameraReady, screenReady]);

  const refreshCameraDevices = async () => {
    if (!navigator.mediaDevices?.enumerateDevices) return;
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const cameras = devices
        .filter((device) => device.kind === "videoinput")
        .map((device, index) => ({
          deviceId: device.deviceId,
          label: device.label || `Camera ${index + 1}`,
        }));
      setCameraDevices(cameras);
      const activeId = getInterviewCameraStream()?.getVideoTracks()[0]?.getSettings().deviceId;
      setSelectedCameraId((current) => {
        if (current && cameras.some((camera) => camera.deviceId === current)) return current;
        if (activeId && cameras.some((camera) => camera.deviceId === activeId)) return activeId;
        return cameras[0]?.deviceId ?? "";
      });
    } catch {
      setCameraDevices([]);
    }
  };

  useEffect(() => {
    if (step === "camera") void refreshCameraDevices();
  }, [step]);

  useEffect(() => {
    const onFullscreenChange = () => {
      const active = Boolean(document.fullscreenElement);
      setFullscreenReady(active);

      // Do not navigate away when Chrome temporarily exits fullscreen while
      // opening/closing its native screen-share picker. Keep the candidate on
      // the current step; the final Start button remains disabled until
      // fullscreen is active again.
      if (!active && screenPickerOpenRef.current) return;

      // Do not force a route reset on fullscreenchange. Browsers can exit
      // fullscreen as part of screen sharing, and a site cannot prevent that.
      // The candidate can re-enter fullscreen using the explicit button.
    };
    document.addEventListener("fullscreenchange", onFullscreenChange);
    return () => document.removeEventListener("fullscreenchange", onFullscreenChange);
  }, [navigate, setup, step]);

  useEffect(() => {
    const camera = getInterviewCameraStream();
    const display = getInterviewDisplayStream();
    const onCameraEnded = () => {
      setCameraReady(false);
      setError("Camera access stopped. You must enable the camera again before continuing.");
      sessionStorage.setItem("codingInterviewPreflightStage", "camera");
      navigate("/coding-interview/preflight/camera", { replace: true, state: { setup: setup ?? undefined } });
    };
    const onDisplayEnded = () => {
      setScreenReady(false);
      setInterviewDisplayStream(null);
      setError("Screen sharing stopped. Share your entire screen again to continue.");
      sessionStorage.setItem("codingInterviewPreflightStage", "screen");
      navigate("/coding-interview/preflight/screen", { replace: true, state: { setup: setup ?? undefined } });
    };
    camera?.getVideoTracks().forEach((track) => track.addEventListener("ended", onCameraEnded));
    display?.getVideoTracks().forEach((track) => track.addEventListener("ended", onDisplayEnded));
    return () => {
      camera?.getVideoTracks().forEach((track) => track.removeEventListener("ended", onCameraEnded));
      display?.getVideoTracks().forEach((track) => track.removeEventListener("ended", onDisplayEnded));
    };
  }, [navigate, setup, step, cameraReady, screenReady]);

  const handleFullscreen = async () => {
    setError(null);
    if (!document.fullscreenEnabled) {
      setError("Fullscreen is unavailable in this browser. Please use a supported browser.");
      return;
    }
    try {
      if (!document.fullscreenElement) await document.documentElement.requestFullscreen();
      if (!document.fullscreenElement) throw new Error("Fullscreen could not be enabled.");
      setFullscreenReady(true);

      // Entering fullscreen from the first step should advance to camera.
      // Re-entering fullscreen from final verification must stay on that step.
      if (step === "fullscreen") {
        goTo("camera");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Fullscreen permission was not granted.");
    }
  };

  const handleCamera = async () => {
    setError(null);

    // The first click requests/starts the selected camera. Once a live stream
    // is already running for the selected device, this button confirms it and
    // advances to the screen-sharing step.
    const activeStream = getInterviewCameraStream();
    const activeTrack = activeStream?.getVideoTracks()[0];
    const activeDeviceId = activeTrack?.getSettings().deviceId;
    if (
      isLiveVideo(activeStream) &&
      (!selectedCameraId || !activeDeviceId || activeDeviceId === selectedCameraId)
    ) {
      goTo("screen");
      return;
    }

    setCameraBusy(true);
    try {
      if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error("Camera access requires a supported browser on HTTPS or localhost.");
      }
      const videoConstraint: MediaTrackConstraints = selectedCameraId
        ? { deviceId: { exact: selectedCameraId } }
        : {};
      const stream = await navigator.mediaDevices.getUserMedia({ video: videoConstraint, audio: false });
      if (!isLiveVideo(stream)) {
        stream.getTracks().forEach((track) => track.stop());
        throw new Error("No active camera was detected.");
      }
      const previous = getInterviewCameraStream();
      if (previous && previous !== stream) previous.getTracks().forEach((track) => track.stop());
      setInterviewCameraStream(stream);
      setCameraReady(true);
      if (cameraRef.current) {
        cameraRef.current.srcObject = stream;
        cameraRef.current.muted = true;
        cameraRef.current.playsInline = true;
        try {
          await cameraRef.current.play();
        } catch {
          throw new Error("The camera is detected, but its preview could not start. Click Allow camera again or check whether another app is using the camera.");
        }
      }
      await refreshCameraDevices();
      // Stay on the camera step so the candidate can see the live preview first.
      // Clicking the button again confirms the already-live stream and continues.
    } catch (err) {
      setError(err instanceof Error ? err.message : "Camera permission was denied or the camera is unavailable.");
    } finally {
      setCameraBusy(false);
    }
  };

  const handleScreenShare = async () => {
    setError(null);
    if (!isLiveVideo(getInterviewCameraStream())) {
      setError("Enable the camera first.");
      goTo("camera");
      return;
    }
    setScreenBusy(true);
    try {
      if (!navigator.mediaDevices?.getDisplayMedia) throw new Error("Screen sharing is unavailable in this browser.");
      // Keep the fullscreen-change handler from treating Chrome's screen-picker transition
      // as a candidate violation. The browser still owns the native picker UI.
      screenPickerOpenRef.current = true;
      const stream = await navigator.mediaDevices.getDisplayMedia({
          video: { displaySurface: "monitor" } as MediaTrackConstraints,
          audio: false,
          // Chromium may use these as hints; they do not disable tab/window choices.
          preferCurrentTab: false,
          selfBrowserSurface: "exclude",
          monitorTypeSurfaces: "include",
        } as DisplayMediaStreamOptions);
      const track = stream.getVideoTracks()[0];
      const settings = track?.getSettings() as (MediaTrackSettings & { displaySurface?: string }) | undefined;
      if (!track || track.readyState !== "live") {
        stream.getTracks().forEach((item) => item.stop());
        throw new Error("No active screen-sharing source was selected.");
      }
      if (settings?.displaySurface !== "monitor") {
        stream.getTracks().forEach((item) => item.stop());
        throw new Error(settings?.displaySurface
          ? "Window and tab sharing are not allowed. Please select Entire Screen and try again."
          : "This browser does not identify the selected screen source, so the app cannot verify entire-screen sharing. Please use a supported browser and try again.");
      }
      const previous = getInterviewDisplayStream();
      if (previous && previous !== stream) previous.getTracks().forEach((item) => item.stop());
      setInterviewDisplayStream(stream);
      setScreenReady(true);
      if (screenRef.current) {
        screenRef.current.srcObject = stream;
        await screenRef.current.play().catch(() => undefined);
      }

      // Chrome may leave fullscreen when its screen picker closes. Try to
      // restore it while the user is still completing this action. If the
      // browser blocks the request, remain on verification and let the
      // candidate use the explicit "Re-enter fullscreen" button.
      if (!document.fullscreenElement) {
        try {
          await document.documentElement.requestFullscreen();
        } catch {
          // Expected in some browsers because fullscreen requires a fresh
          // user gesture. The UI will show the re-entry button.
        }
      }

      goTo("ready");
    } catch (err) {
      setScreenReady(false);
      setError(err instanceof Error ? err.message : "Screen sharing was cancelled or failed.");
    } finally {
      screenPickerOpenRef.current = false;
      setFullscreenReady(Boolean(document.fullscreenElement));
      setScreenBusy(false);
    }
  };

  const startInterview = async () => {
    setError(null);
    if (!setup) {
      setError("Your interview configuration is missing. Please configure your interview again.");
      return;
    }
    const camera = getInterviewCameraStream();
    const display = getInterviewDisplayStream();
    const displayTrack = display?.getVideoTracks()[0];
    const displaySettings = displayTrack?.getSettings() as (MediaTrackSettings & { displaySurface?: string }) | undefined;
    const valid = Boolean(
      document.fullscreenElement &&
      isLiveVideo(camera) &&
      displayTrack?.readyState === "live" &&
      displaySettings?.displaySurface === "monitor" &&
      singleDisplayConfirmed
    );
    if (!valid) {
      if (!document.fullscreenElement) goTo("fullscreen");
      else if (!isLiveVideo(camera)) goTo("camera");
      else goTo("screen");
      setError("One or more security checks are incomplete. Complete each step before starting.");
      return;
    }
    if (starting) return;
    setStarting(true);
    try {
      const interview = await createCodingInterview(
        setup.language,
        setup.difficulty,
        setup.questionCount,
      );

      // Persist the session details before navigating. React Router location state
      // can be lost on refresh or during certain route transitions.
      sessionStorage.setItem("codingInterviewSessionId", String(interview.id));
      sessionStorage.setItem("codingInterviewPreflightVerified", "true");
      sessionStorage.removeItem("codingInterviewPreflightStage");

      navigate("/coding-interview", {
        replace: true,
        state: {
          sessionId: interview.id,
          language: setup.language,
          difficulty: setup.difficulty,
          questionCount: interview.total_questions,
          preflightChecksPassed: true,
        },
      });
    } catch (err) {
      sessionStorage.removeItem("codingInterviewPreflightVerified");
      setError(err instanceof Error ? err.message : "Unable to start the interview.");
    } finally {
      setStarting(false);
    }
  };

  if (!setup || !step) return null;
  const details = stepDetails[step];
  const checkRows = [
    ["Fullscreen", Boolean(document.fullscreenElement)],
    ["Camera", isLiveVideo(getInterviewCameraStream())],
    ["Entire screen", (() => {
      const track = getInterviewDisplayStream()?.getVideoTracks()[0];
      const settings = track?.getSettings() as (MediaTrackSettings & { displaySurface?: string }) | undefined;
      return track?.readyState === "live" && settings?.displaySurface === "monitor";
    })()],
  ] as const;

  return (
    <div className="app-background min-h-screen px-5 py-8 sm:px-8">
      <main className="mx-auto flex min-h-[85vh] w-full max-w-3xl items-center justify-center">
        <section className="glass-panel w-full rounded-3xl border border-white/[0.07] p-6 sm:p-9">
          <div className="flex items-center justify-between gap-2">
            <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-violet-400">Coding interview · Security check</p>
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
            <p className="mt-2 text-xs text-slate-500">Connect an external USB webcam before refreshing. Camera names may appear only after browser permission is granted.</p>
            <div className="mt-5 overflow-hidden rounded-2xl border border-white/[0.08] bg-black/30">
              <video ref={cameraRef} autoPlay muted playsInline onClick={() => { void cameraRef.current?.play().catch(() => setError("Camera preview could not start. Check browser camera permissions and close other apps using the camera.")); }} className="aspect-video max-h-[420px] w-full bg-slate-950 object-cover" aria-label="Camera preview" />
            </div>
            <p className="mt-3 text-xs text-slate-500">The camera must remain active throughout the interview. If it stops during the test, the interview will be terminated.</p>
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
            <div className="mt-7 grid gap-3 sm:grid-cols-3">
              {checkRows.map(([label, passed]) => <div key={label} className="flex items-center gap-3 rounded-2xl border border-white/[0.07] bg-black/10 p-4"><span className={`flex h-8 w-8 items-center justify-center rounded-full ${passed ? "bg-cyan-300/10 text-cyan-200" : "bg-rose-400/10 text-rose-200"}`}>{passed ? "✓" : "!"}</span><div><p className="text-sm font-medium text-white">{label}</p><p className={`mt-1 text-xs ${passed ? "text-cyan-200" : "text-rose-200"}`}>{passed ? "Ready" : "Required"}</p></div></div>)}
            </div>
            <label className="mt-5 flex cursor-pointer items-start gap-3 rounded-2xl border border-white/[0.07] bg-black/10 p-4 text-sm leading-6 text-slate-300"><input type="checkbox" checked={singleDisplayConfirmed} onChange={(event) => setSingleDisplayConfirmed(event.target.checked)} className="mt-1 accent-violet-400"/><span>I confirm that I am using only one display. Browsers cannot reliably count physical monitors, so this requirement needs candidate confirmation.</span></label>
            {!fullscreenReady && <button type="button" onClick={() => void handleFullscreen()} className="mt-5 w-full rounded-2xl border border-violet-300/30 px-5 py-3 text-sm font-semibold text-violet-200 hover:bg-violet-400/10">Re-enter fullscreen to continue</button>}
            <button type="button" disabled={starting || !fullscreenReady || !cameraReady || !screenReady || !singleDisplayConfirmed} onClick={() => void startInterview()} className="mt-6 w-full rounded-2xl bg-violet-400 px-5 py-4 text-sm font-semibold text-slate-950 transition hover:bg-violet-300 disabled:cursor-not-allowed disabled:opacity-40">{starting ? "Starting coding interview…" : "All checks complete — Start coding interview →"}</button>
          </>}
          <div className="mt-6 border-t border-white/[0.07] pt-5"><button type="button" onClick={() => {
            setError(null);
            if (step === "fullscreen") {
              stopInterviewSetupMedia();
              sessionStorage.removeItem("codingInterviewPreflightVerified");
              sessionStorage.removeItem("codingInterviewPreflightStage");
              navigate("/home", { replace: true });
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
