export type AuthStatus = "unknown" | "anonymous" | "authenticated";
export type RouteName = "login" | "feed" | "about" | "not-found";

export interface NavigationInput {
  routeName: RouteName;
  requiresAuth: boolean;
  authStatus: AuthStatus;
  fullPath: string;
}

export type NavigationDecision =
  | { action: "allow" }
  | { action: "resolve-auth" }
  | { action: "redirect"; name: RouteName; redirect?: string };

export function decideNavigation(input: NavigationInput): NavigationDecision {
  // TODO: mantieni la semantica della policy JavaScript della milestone 10.
  // 1. una route protetta o login con auth unknown richiede resolve-auth
  // 2. una route protetta anonima redirige a login preservando fullPath
  // 3. login da autenticato redirige a feed
  // 4. altrimenti allow
  void input;
  return { action: "allow" };
}
