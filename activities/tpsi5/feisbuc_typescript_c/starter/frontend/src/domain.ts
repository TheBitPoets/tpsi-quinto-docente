// Completa i contratti partendo dalle representation API gia note.
export interface User {
  id: string;
  email: string;
  displayName: string;
}

export interface Post {
  id: string;
  authorId: string;
  author: string;
  text: string;
  liked: boolean;
  likes: number;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegistrationCredentials extends LoginCredentials {
  displayName: string;
}

export type AuthStatus = "unknown" | "anonymous" | "authenticated";
export type RouteName = "login" | "feed" | "about" | "not-found";
