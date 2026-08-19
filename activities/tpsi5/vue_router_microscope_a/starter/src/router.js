import { createRouter, createWebHistory } from "vue-router";
import HomeView from "./views/HomeView.vue";
import FeedView from "./views/FeedView.vue";
import NotFoundView from "./views/NotFoundView.vue";

export const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/feed", name: "feed", component: FeedView },
  { path: "/:pathMatch(.*)", name: "not-found", component: NotFoundView },
];

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});
