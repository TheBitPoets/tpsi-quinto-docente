import type { AuthStatus, RouteName } from "./domain";

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
  const needsAuthKnowledge = input.requiresAuth || input.routeName === "login";
  if (needsAuthKnowledge && input.authStatus === "unknown") return { action: "resolve-auth" };
  if (input.requiresAuth && input.authStatus !== "authenticated") {
    return { action: "redirect", name: "login", redirect: input.fullPath };
  }
  if (input.routeName === "login" && input.authStatus === "authenticated") {
    return { action: "redirect", name: "feed" };
  }
  return { action: "allow" };
}
