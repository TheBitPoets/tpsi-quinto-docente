import process from "node:process";

export function decideNavigation({ routeName, requiresAuth, authStatus, fullPath }) {
  const needsAuthKnowledge = requiresAuth || routeName === "login";
  if (needsAuthKnowledge && authStatus === "unknown") {
    return { action: "resolve-auth" };
  }
  if (requiresAuth && authStatus !== "authenticated") {
    return { action: "redirect", name: "login", redirect: fullPath };
  }
  if (routeName === "login" && authStatus === "authenticated") {
    return { action: "redirect", name: "feed" };
  }
  return { action: "allow" };
}

const raw = await new Promise((resolve) => {
  let data = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", (chunk) => { data += chunk; });
  process.stdin.on("end", () => resolve(data));
});

const input = JSON.parse(raw);
process.stdout.write(JSON.stringify(decideNavigation(input)));
