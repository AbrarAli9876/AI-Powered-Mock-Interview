import type { PreflightEvidence } from "./proctoring";
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";
interface ApiError {
  detail?: string;
}
async function request<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const token =
    localStorage.getItem("access_token");
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Content-Type":
          "application/json",
        ...(token
          ? {
              Authorization:
                `Bearer ${token}`,
            }
          : {}),
        ...(options.headers || {}),
      },
    },
  );
  if (!response.ok) {
    let message =
      "Something went wrong.";
    try {
      const error: ApiError =
        await response.json();
      message =
        error.detail ||
        message;
    } catch {
      // Keep default error message.
    }
    throw new Error(message);
  }
  return response.json();
}
/* =========================================================
   TOPIC
   ========================================================= */
export interface Topic {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
/* =========================================================
   DIFFICULTY
   ========================================================= */
export type Difficulty =
  | "easy"
  | "medium"
  | "hard";
/* =========================================================
   CODING LANGUAGE
   ========================================================= */
export type CodingLanguage =
  | "python"
  | "javascript"
  | "java"
  | "cpp";
/* =========================================================
   INTERVIEW
   ========================================================= */
export interface Interview {
  id: number;
  user_id: number;
  topic_id: number;
  starting_difficulty:
    Difficulty;
  current_difficulty:
    Difficulty;
  status:
    | "in_progress"
    | "completed"
    | "abandoned";
  total_questions: number;
  current_question_number: number;
  poor_streak: number;
  strong_streak: number;
  overall_score: number | null;
  created_at: string;
  updated_at: string;
}
/* =========================================================
   QUESTION
   ========================================================= */
export interface Question {
  id: number;
  topic_id: number;
  difficulty: Difficulty;
  question_text: string;
  expected_answer: string;
  companies: string[] | null;
  created_at: string;
  updated_at: string;
}
/* =========================================================
   EVALUATION
   ========================================================= */
export interface Evaluation {
  id: number;
  session_id: number;
  question_id: number;
  answer_text: string;
  overall_score:
    number | null;
  technical_score:
    number | null;
  communication_score:
    number | null;
  relevance_score:
    number | null;
  feedback: string | null;
  strengths: string | null;
  improvements: string | null;
  created_at: string;
  updated_at: string;
}
/* =========================================================
   INTERVIEW RESULT
   ========================================================= */
export interface InterviewResultAnswer {
  question_id: number;
  question_text: string;
  difficulty: Difficulty;
  answer_text: string;
  overall_score:
    number | null;
  technical_score:
    number | null;
  communication_score:
    number | null;
  relevance_score:
    number | null;
  feedback: string | null;
  strengths: string | null;
  improvements: string | null;
}
export interface InterviewResult {
  session_id: number;
  user_id: number;
  topic_id: number;
  starting_difficulty:
    Difficulty;
  final_difficulty:
    Difficulty;
  status:
    | "in_progress"
    | "completed"
    | "abandoned";
  total_questions: number;
  current_question_number:
    number;
  overall_score:
    number | null;
  created_at: string;
  updated_at: string;
  difficulty_progression:
    Difficulty[];
  final_summary:
    string | null;
  final_strengths:
    string | null;
  final_weaknesses:
    string | null;
  technical_assessment:
    string | null;
  communication_assessment:
    string | null;
  problem_solving_assessment:
    string | null;
  final_recommendations:
    string | null;
  answers:
    InterviewResultAnswer[];
}
export interface CodingTestCase {
  id: number;
  input_data: string;
  expected_output: string;
  is_hidden: boolean;
  execution_order: number;
}
export interface CodingQuestion {
  id: number;
  topic_id: number;
  language: CodingLanguage;
  difficulty: Difficulty;
  title: string;
  problem_statement: string;
  input_format: string;
  output_format: string;
  constraints: string;
  examples: string;
  starter_code: string;
  hint_1: string;
  hint_2: string;
  test_cases: CodingTestCase[];
  created_at: string;
  updated_at: string;
}
/* =========================================================
   CODE EXECUTION
   ========================================================= */
export interface CodeExecutionRequest {
  coding_question_id: number;
  code: string;
}
export interface TestCaseResult {
  test_case_number: number;
  passed: boolean;
  input_data: string;
  expected_output: string;
  actual_output: string;
  error: string | null;
  execution_time_ms:
    number | null;
}
export interface CodeExecutionResponse {
  success: boolean;
  language: string;
  total_test_cases: number;
  passed_test_cases: number;
  failed_test_cases: number;
  results: TestCaseResult[];
}
/* =========================================================
   TOPIC API
   ========================================================= */
export async function getTopics():
  Promise<Topic[]> {
  return request<Topic[]>(
    "/topics",
  );
}
/* =========================================================
   INTERVIEW API
   ========================================================= */
export async function createInterview(
  topicId: number,
  startingDifficulty: Difficulty,
  questionCount: 10 | 15 | 20 = 10,
  preflight?: PreflightEvidence,
): Promise<Interview> {
  return request<Interview>(
    "/interviews",
    {
      method: "POST",
      body: JSON.stringify({
        topic_id:
          topicId,
        starting_difficulty:
          startingDifficulty,
        question_count:
          questionCount,
        preflight,
      }),
    },
  );
}
export async function getInterviews():
  Promise<Interview[]> {
  return request<Interview[]>(
    "/interviews",
  );
}
export async function getInterview(
  sessionId: number,
): Promise<Interview> {
  return request<Interview>(
    `/interviews/${sessionId}`,
  );
}
export async function getNextQuestion(
  sessionId: number,
): Promise<Question> {
  return request<Question>(
    `/interviews/${sessionId}/next-question`,
  );
}
export async function completeInterview(
  sessionId: number,
): Promise<Interview> {
  return request<Interview>(
    `/interviews/${sessionId}/complete`,
    {
      method: "POST",
    },
  );
}
export async function abandonInterview(
  sessionId: number,
): Promise<Interview> {
  return request<Interview>(
    `/interviews/${sessionId}/abandon`,
    {
      method: "POST",
    },
  );
}
/* =========================================================
   ANSWER API
   ========================================================= */
export async function submitAnswer(
  sessionId: number,
  questionId: number,
  answerText: string,
): Promise<Evaluation> {
  return request<Evaluation>(
    "/interview-answers",
    {
      method: "POST",
      body: JSON.stringify({
        session_id:
          sessionId,
        question_id:
          questionId,
        answer_text:
          answerText,
      }),
    },
  );
}
/* =========================================================
   RESULT API
   ========================================================= */
export async function getInterviewResult(
  sessionId: number,
): Promise<InterviewResult> {
  return request<InterviewResult>(
    `/interviews/${sessionId}/result`,
  );
}
/* =========================================================
   CODING QUESTION API
   ========================================================= */
export async function getCodingQuestions(
  language?: CodingLanguage,
  difficulty?: Difficulty,
): Promise<CodingQuestion[]> {
  const params =
    new URLSearchParams();
  if (language !== undefined) {
    params.append(
      "language",
      language,
    );
  }
  if (difficulty !== undefined) {
    params.append(
      "difficulty",
      difficulty,
    );
  }
  const queryString =
    params.toString();
  return request<CodingQuestion[]>(
    `/coding-questions${
      queryString
        ? `?${queryString}`
        : ""
    }`,
  );
}
/* =========================================================
   SINGLE CODING QUESTION
   ========================================================= */
export async function getCodingQuestion(
  questionId: number,
): Promise<CodingQuestion> {
  return request<CodingQuestion>(
    `/coding-questions/${questionId}`,
  );
}
/* =========================================================
   CODE EXECUTION API
   ========================================================= */
export async function runCode(
  codingQuestionId: number,
  code: string,
): Promise<CodeExecutionResponse> {
  return request<CodeExecutionResponse>(
    "/code-execution/run",
    {
      method: "POST",
      body: JSON.stringify({
        coding_question_id:
          codingQuestionId,
        code,
      }),
    },
  );
}
/* =========================================================
   CODING INTERVIEW API
   ========================================================= */
export async function createCodingInterview(
  language: CodingLanguage,
  difficulty: Difficulty,
  totalQuestions: number,
): Promise<CodingInterview> {
  return request<CodingInterview>(
    "/coding-interviews",
    {
      method: "POST",
      body: JSON.stringify({
        language,
        difficulty,
        total_questions: totalQuestions,
      }),
    },
  );
}
export async function getCodingInterview(
  sessionId: number,
): Promise<CodingInterview> {
  return request<CodingInterview>(
    `/coding-interviews/${sessionId}`,
  );
}
export async function getCurrentCodingQuestion(
  sessionId: number,
): Promise<CodingInterviewQuestionResponse> {
  return request<CodingInterviewQuestionResponse>(
    `/coding-interviews/${sessionId}/current-question`,
  );
}
export async function submitCodingAnswer(
  sessionId: number,
  code: string,
): Promise<CodingInterviewSubmitResponse> {
  return request<CodingInterviewSubmitResponse>(
    `/coding-interviews/${sessionId}/submit`,
    {
      method: "POST",
      body: JSON.stringify({
        code,
      }),
    },
  );
}
export async function getNextCodingQuestion(
  sessionId: number,
): Promise<CodingInterviewQuestionResponse> {
  return request<CodingInterviewQuestionResponse>(
    `/coding-interviews/${sessionId}/next-question`,
    {
      method: "POST",
    },
  );
}
export async function completeCodingInterview(
  sessionId: number,
): Promise<CodingInterview> {
  return request<CodingInterview>(
    `/coding-interviews/${sessionId}/complete`,
    {
      method: "POST",
    },
  );
}
export async function abandonCodingInterview(
  sessionId: number,
): Promise<CodingInterview> {
  return request<CodingInterview>(
    `/coding-interviews/${sessionId}/abandon`,
    {
      method: "POST",
    },
  );
}
export async function getCodingInterviewResult(
  sessionId: number,
): Promise<CodingInterviewResult> {
  return request<CodingInterviewResult>(
    `/coding-interviews/${sessionId}/result`,
  );
}
/* =========================================================
   CODING INTERVIEW
   ========================================================= */
export interface CodingInterviewCreate {
  language: CodingLanguage;
  difficulty: Difficulty;
  total_questions: number;
}
export interface CodingInterview {
  id: number;
  user_id: number;
  language: CodingLanguage;
  difficulty: Difficulty;
  total_questions: number;
  current_question_number: number;
  status:
    | "in_progress"
    | "completed"
    | "abandoned";
  created_at: string;
  updated_at: string;
}
export interface CodingInterviewQuestionResponse {
  question_number: number;
  total_questions: number;
  question: CodingQuestion;
}
export interface CodingInterviewSubmitRequest {
  code: string;
}
export interface CodingInterviewSubmitResponse {
  answer_id: number;
  session_id: number;
  question_number: number;
  success: boolean;
  total_test_cases: number;
  passed_test_cases: number;
  failed_test_cases: number;
  score: number;
  feedback: string;
  is_last_question: boolean;
}
export interface CodingInterviewResultAnswer {
  question_number: number;
  coding_question_id: number;
  title: string;
  language: string;
  difficulty: string;
  code: string;
  success: boolean;
  total_test_cases: number;
  passed_test_cases: number;
  failed_test_cases: number;
  score: number | null;
  feedback: string | null;
}
export interface CodingInterviewResult {
  session_id: number;
  language: string;
  difficulty: string;
  status: string;
  total_questions: number;
  attempted_questions: number;
  total_test_cases: number;
  passed_test_cases: number;
  failed_test_cases: number;
  overall_score: number;
  answers: CodingInterviewResultAnswer[];
}
