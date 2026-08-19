import api from "./axios";

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

export interface User {
  id: number;
  full_name: string;
  email: string;
  role: "admin" | "user";
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export async function login(
  data: LoginRequest
): Promise<TokenResponse> {
  const response = await api.post<TokenResponse>(
    "/auth/login",
    data
  );

  return response.data;
}

export async function register(
  data: RegisterRequest
): Promise<User> {
  const response = await api.post<User>(
    "/auth/register",
    data
  );

  return response.data;
}

export async function getCurrentUser(): Promise<User> {
  const response = await api.get<User>("/auth/me");

  return response.data;
}

export function logout(): void {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user");
}