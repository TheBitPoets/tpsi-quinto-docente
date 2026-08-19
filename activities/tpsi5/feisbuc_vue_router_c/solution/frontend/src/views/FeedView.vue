<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api, ApiError } from "../api.js";
import PostComposer from "../components/PostComposer.vue";
import PostCard from "../components/PostCard.vue";
import { useSession } from "../session.js";

const route = useRoute();
const router = useRouter();
const session = useSession();
const posts = ref([]);
const loading = ref(false);
const error = ref("");
const postCount = computed(() => posts.value.length);
const likedCount = computed(() => posts.value.filter((post) => post.liked).length);

async function handleError(cause) {
  if (cause instanceof ApiError && cause.status === 401) {
    session.markAnonymous();
    await router.replace({ name: "login", query: { redirect: route.fullPath } });
    return;
  }
  error.value = cause instanceof Error ? cause.message : "Errore inatteso";
}

async function loadPosts() {
  loading.value = true; error.value = "";
  try { posts.value = await api.listPosts(); }
  catch (cause) { await handleError(cause); }
  finally { loading.value = false; }
}

async function createPost(text) {
  loading.value = true; error.value = "";
  try { posts.value = [await api.createPost(text), ...posts.value]; }
  catch (cause) { await handleError(cause); }
  finally { loading.value = false; }
}

async function toggleLike(id) {
  const current = posts.value.find((post) => post.id === id);
  if (!current) return;
  loading.value = true; error.value = "";
  try {
    const updated = await api.setLiked(id, !current.liked);
    posts.value = posts.value.map((post) => post.id === id ? updated : post);
  } catch (cause) { await handleError(cause); }
  finally { loading.value = false; }
}

async function deletePost(id) {
  loading.value = true; error.value = "";
  try {
    await api.deletePost(id);
    posts.value = posts.value.filter((post) => post.id !== id);
  } catch (cause) { await handleError(cause); }
  finally { loading.value = false; }
}

onMounted(loadPosts);
</script>

<template>
  <main>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <p>Post {{ postCount }} · liked {{ likedCount }}</p>
    <PostComposer :disabled="loading" @create="createPost" />
    <section aria-labelledby="feed-title">
      <h2 id="feed-title">Feed</h2>
      <p v-if="loading && posts.length === 0">Caricamento...</p>
      <p v-else-if="posts.length === 0">Nessun post.</p>
      <PostCard
        v-for="post in posts"
        :key="post.id"
        :post="post"
        :can-delete="post.authorId === session.user.value?.id"
        @toggle-like="toggleLike"
        @delete="deletePost"
      />
    </section>
  </main>
</template>
