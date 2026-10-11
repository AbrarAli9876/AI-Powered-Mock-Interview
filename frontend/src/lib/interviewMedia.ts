/**
 * Shared browser media streams for the Technical Interview preflight and room.
 * Keep these functions declared only in this module to avoid duplicate exports
 * and Vite React Fast Refresh warnings.
 */

let cameraStream: MediaStream | null = null;
let displayStream: MediaStream | null = null;

export function getInterviewCameraStream(): MediaStream | null {
  return cameraStream;
}

export function setInterviewCameraStream(stream: MediaStream | null): void {
  cameraStream = stream;
}

export function getInterviewDisplayStream(): MediaStream | null {
  return displayStream;
}

export function setInterviewDisplayStream(stream: MediaStream | null): void {
  displayStream = stream;
}

export function stopInterviewSetupMedia(): void {
  const streams = [cameraStream, displayStream];
  cameraStream = null;
  displayStream = null;

  streams.forEach((stream) => {
    stream?.getTracks().forEach((track) => {
      try {
        track.stop();
      } catch {
        // Continue stopping remaining tracks if a browser track throws.
      }
    });
  });
}
