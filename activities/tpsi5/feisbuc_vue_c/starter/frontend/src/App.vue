<script setup>
import { computed, onMounted, ref } from "vue";
import { api, ApiError } from "./api.js";
import AuthPanel from "./components/AuthPanel.vue";
import PostComposer from "./components/PostComposer.vue";
import PostCard from "./components/PostCard.vue";

const user = ref(null);
const posts = ref([]);
const loading = ref(false);
const error = ref("");
const loggedIn = computed(() => Boolean(user.value));
const postCount = computed(() => posts.value.length);
const likedCount = computed(() => posts.value.filter(post => post.liked).length);

// TODO C: completa bootstrap, auth e CRUD mantenendo App owner dello state.
async function bootstrap() {}
async function login(credentials) {}
async function register(credentials) {}
async function logout() {}
async function createPost(text) {}
async function toggleLike(id) {}
async function deletePost(id) {}

onMounted(bootstrap);
</script>

<template>
  <main class="shell">
    <header class="hero"><div><p class="eyebrow">Milestone 9</p><h1>Feisbuc Vue SPA</h1></div><button v-if="loggedIn" type="button" @click="logout">Logout</button></header>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <AuthPanel v-if="!loggedIn" :loading="loading" @login="login" @register="register" />
    <template v-else>
      <p>Utente: <strong>{{ user.displayName }}</strong> · post {{ postCount }} · liked {{ likedCount }}</p>
      <PostComposer :disabled="loading" @create="createPost" />
      <section aria-labelledby="feed-title"><h2 id="feed-title">Feed</h2><PostCard v-for="post in posts" :key="post.id" :post="post" :can-delete="post.authorId === user.id" @toggle-like="toggleLike" @delete="deletePost" /></section>
    </template>
  </main>
</template>
