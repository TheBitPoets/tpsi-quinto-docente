import type { RouteMeta } from "vue-router";

declare module "vue-router" {
  interface RouteMeta { requiresAuth?: boolean; }
}

export const protectedMeta = { requiresAuth: true } satisfies RouteMeta;
