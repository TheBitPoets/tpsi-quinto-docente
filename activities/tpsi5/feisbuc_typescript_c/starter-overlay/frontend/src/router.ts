import { createRouter, createWebHistory } from "vue-router";
import type { RouteMeta } from "vue-router";
import { decideNavigation } from "./navigation-policy";
import { session } from "./session";
import type { RouteName } from "./domain";

declare module "vue-router" {
  interface RouteMeta { requiresAuth?: boolean; }
}

function normalizeRouteName(value: unknown): RouteName {
  if (value === "login" || value === "feed" || value === "about" || value === "not-found") return value;
  return "not-found";
}

export const routes = [
  { path: "/", redirect: { name: "feed" } },
  { path: "/login", name: "login", component: () => import("./views/LoginView.vue") },
  { path: "/feed", name: "feed", component: () => import("./views/FeedView.vue"), meta: { requiresAuth: true } satisfies RouteMeta },
  { path: "/about", name: "about", component: () => import("./views/AboutView.vue") },
  { path: "/:pathMatch(.*)", name: "not-found", component: () => import("./views/NotFoundView.vue") },
];

export const router = createRouter({ history: createWebHistory(import.meta.env.BASE_URL), routes });

router.beforeEach(async (to) => {
  const input = () => ({
    routeName: normalizeRouteName(to.name),
    requiresAuth: Boolean(to.meta.requiresAuth),
    authStatus: session.status.value,
    fullPath: to.fullPath,
  });
  let decision = decideNavigation(input());
  if (decision.action === "resolve-auth") {
    await session.ensureKnown();
    decision = decideNavigation(input());
  }
  if (decision.action === "redirect") {
    return { name: decision.name, ...(decision.redirect ? { query: { redirect: decision.redirect } } : {}), replace: true };
  }
  return true;
});
