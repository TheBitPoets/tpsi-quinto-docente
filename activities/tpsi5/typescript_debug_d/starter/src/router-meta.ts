import type { RouteMeta } from "vue-router";

declare module "vue-router" {
  interface RouteMeta { requiresAuth?: boolean; }
}

// Bug 5: typo che TypeScript deve rendere visibile.
export const protectedMeta = { requireAuth: true } satisfies RouteMeta;
