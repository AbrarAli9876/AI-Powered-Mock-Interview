
/**
 * Shared media streams for the Technical Interview.
 *
 * These streams are created during InterviewSetup.tsx and reused
 * by InterviewRoom.tsx after navigation.
 *
 * Keep these functions in this module only. Do not redeclare
 * them inside InterviewSetup.tsx or InterviewRoom.tsx.
 */

let cameraStream: MediaStream | null = null;
let displayStream: MediaStream | null = null;

/**
 * Return the camera stream currently used by the interview.
 */
export function getInterviewCameraStream(): MediaStream | null {
  return cameraStream;
}

/**
 * Save or replace the camera stream.
 */
export function setInterviewCameraStream(
  stream: MediaStream | null,
): void {
  cameraStream = stream;
}

/**
 * Return the screen-sharing stream currently used by the interview.
 */
export function getInterviewDisplayStream(): MediaStream | null {
  return displayStream;
}

/**
 * Save or replace the screen-sharing stream.
 */
export function setInterviewDisplayStream(
  stream: MediaStream | null,
): void {
  displayStream = stream;
}

/**
 * Stop all tracks and clear the shared streams.
 */
export function stopInterviewSetupMedia(): void {
  if (cameraStream) {
    cameraStream.getTracks().forEach((track) => {
      track.stop();
    });

    cameraStream = null;
  }

  if (displayStream) {
    displayStream.getTracks().forEach((track) => {
      track.stop();
    });

    displayStream = null;
  }
}
