import { createRouter, createWebHistory } from "vue-router";
import { decideNavigation } from "./navigation-policy.js";
import { session } from "./session.js";

// TODO: route / redirect, login, feed protetto, about e catch-all not-found.
export const routes = [];

export const router = createRouter({
  // TODO: usa import.meta.env.BASE_URL.
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  // TODO: costruisci l'input per decideNavigation(), risolvi `unknown`
  // con session.ensureKnown(), poi traduci la decisione in allow/redirect.
  void to; void decideNavigation; void session;
  return true;
});
