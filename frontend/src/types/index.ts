export type UserRole = "admin" | "user";

export type QuestionDifficulty =
  | "easy"
  | "medium"
  | "hard";

export type InterviewStatus =
  | "in_progress"
  | "completed"
  | "abandoned";


// ============================================================
// USER
// ============================================================

export interface User {
  id: number;
  full_name: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}


// ============================================================
// AUTHENTICATION
// ============================================================

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}


// ============================================================
// TOPIC
// ============================================================

export interface Topic {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface TopicCreate {
  name: string;
  description?: string | null;
}

export interface TopicUpdate {
  name?: string;
  description?: string | null;
  is_active?: boolean;
}


// ============================================================
// QUESTION
// ============================================================

export interface Question {
  id: number;
  topic_id: number;
  difficulty: QuestionDifficulty;
  question_text: string;
  expected_answer: string;
  created_at: string;
  updated_at: string;
}

export interface QuestionCreate {
  topic_id: number;
  difficulty: QuestionDifficulty;
  question_text: string;
  expected_answer: string;
}

export interface QuestionUpdate {
  topic_id?: number;
  difficulty?: QuestionDifficulty;
  question_text?: string;
  expected_answer?: string;
}


// ============================================================
// INTERVIEW
// ============================================================

export interface InterviewCreate {
  topic_id: number;
  starting_difficulty: QuestionDifficulty;
}

export interface InterviewUpdate {
  status?: InterviewStatus;
}

export interface Interview {
  id: number;
  user_id: number;
  topic_id: number;

  starting_difficulty: QuestionDifficulty;
  current_difficulty: QuestionDifficulty;

  status: InterviewStatus;

  total_questions: number;
  current_question_number: number;

  poor_streak: number;
  strong_streak: number;

  overall_score: number | null;

  created_at: string;
  updated_at: string;
}


// ============================================================
// INTERVIEW ANSWER
// ============================================================

export interface InterviewAnswerCreate {
  session_id: number;
  question_id: number;
  answer_text: string;
}

export interface InterviewEvaluation {
  overall_score: number;
  technical_score: number;
  communication_score: number;
  relevance_score: number;

  feedback: string;
  strengths: string;
  improvements: string;
}


// ============================================================
// INTERVIEW QUESTION / CURRENT QUESTION
// ============================================================

export interface InterviewQuestion {
  id: number;
  topic_id: number;
  difficulty: QuestionDifficulty;
  question_text: string;
  expected_answer?: string;
  created_at: string;
  updated_at: string;
}


// ============================================================
// QUESTION-BY-QUESTION RESULT
// ============================================================

export interface InterviewResultAnswer {
  question_id: number;
  question_text: string;
  difficulty: QuestionDifficulty;

  answer_text: string;

  overall_score: number | null;
  technical_score: number | null;
  communication_score: number | null;
  relevance_score: number | null;

  feedback: string | null;
  strengths: string | null;
  improvements: string | null;
}


// ============================================================
// FINAL INTERVIEW RESULT
// ============================================================

export interface InterviewResult {
  session_id: number;
  user_id: number;
  topic_id: number;

  starting_difficulty: QuestionDifficulty;
  final_difficulty: QuestionDifficulty;

  status: InterviewStatus;

  total_questions: number;
  current_question_number: number;

  overall_score: number | null;

  created_at: string;
  updated_at: string;

  difficulty_progression: QuestionDifficulty[];

  final_summary: string | null;
  final_strengths: string | null;
  final_weaknesses: string | null;

  technical_assessment: string | null;
  communication_assessment: string | null;
  problem_solving_assessment: string | null;

  final_recommendations: string | null;

  answers: InterviewResultAnswer[];
}


// ============================================================
// ADMIN DASHBOARD
// ============================================================

export interface AdminDashboardStats {
  total_users: number;
  total_interviews: number;
  completed_interviews: number;
  in_progress_interviews: number;
  abandoned_interviews: number;
  average_interview_score: number | null;
}


// ============================================================
// ADMIN USER
// ============================================================

export interface AdminUser {
  id: number;
  full_name: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AdminUserStatusUpdate {
  is_active: boolean;
}


// ============================================================
// ADMIN INTERVIEW
// ============================================================

export interface AdminInterview {
  session_id: number;

  user_id: number;
  user_name: string;
  user_email: string;

  topic_id: number;
  topic_name: string;

  starting_difficulty: QuestionDifficulty;
  final_difficulty: QuestionDifficulty;

  status: InterviewStatus;

  total_questions: number;
  current_question_number: number;

  overall_score: number | null;

  created_at: string;
  updated_at: string;
}


// ============================================================
// ADMIN INTERVIEW ANSWER
// ============================================================

export interface AdminInterviewAnswer {
  question_id: number;
  question_text: string;
  difficulty: QuestionDifficulty;

  answer_text: string;

  overall_score: number | null;
  technical_score: number | null;
  communication_score: number | null;
  relevance_score: number | null;

  feedback: string | null;
  strengths: string | null;
  improvements: string | null;
}


// ============================================================
// ADMIN INTERVIEW DETAIL
// ============================================================

export interface AdminInterviewDetail {
  session_id: number;

  user_id: number;
  user_name: string;
  user_email: string;

  topic_id: number;
  topic_name: string;

  starting_difficulty: QuestionDifficulty;
  final_difficulty: QuestionDifficulty;

  status: InterviewStatus;

  total_questions: number;
  current_question_number: number;

  overall_score: number | null;

  created_at: string;
  updated_at: string;

  difficulty_progression: QuestionDifficulty[];

  final_summary: string | null;
  final_strengths: string | null;
  final_weaknesses: string | null;

  technical_assessment: string | null;
  communication_assessment: string | null;
  problem_solving_assessment: string | null;

  final_recommendations: string | null;

  answers: AdminInterviewAnswer[];
}