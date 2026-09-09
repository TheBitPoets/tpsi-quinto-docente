export function decideNavigation({ routeName, requiresAuth, authStatus, fullPath }) {
  const needsAuthKnowledge = requiresAuth || routeName === "login";
  if (needsAuthKnowledge && authStatus === "unknown") return { action: "resolve-auth" };
  if (requiresAuth && authStatus !== "authenticated") {
    return { action: "redirect", name: "login", redirect: fullPath };
  }
  if (routeName === "login" && authStatus === "authenticated") {
    return { action: "redirect", name: "feed" };
  }
  return { action: "allow" };
}
