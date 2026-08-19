import { createRouter, createWebHistory } from "vue-router";
import { session } from "./session.js";
import LoginView from "./LoginView.vue";
import FeedView from "./FeedView.vue";
import AboutView from "./AboutView.vue";

export const router=createRouter({
  history:createWebHistory(), // BUG: app buildata sotto /vue/
  routes:[
    {path:"/login",name:"login",component:LoginView},
    {path:"/feed",name:"feed",component:FeedView,meta:{requireAuth:true}}, // BUG: typo
    {path:"/about",name:"about",component:AboutView},
    // BUG: manca catch-all client
  ],
});

router.beforeEach(async(to)=>{
  await session.ensureKnown();
  // BUG: redirige anche /login e tutte le route pubbliche quando anonimo.
  if(session.status.value!=="authenticated") return {name:"login"};
  return true;
});
