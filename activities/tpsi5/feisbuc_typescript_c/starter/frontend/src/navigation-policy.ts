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
  // TODO: riporta la semantica della Activity B senza allargare i tipi a string/any.
  void input;
  return { action: "allow" };
}
