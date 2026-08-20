<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api, ApiError } from "../api";
import PostComposer from "../components/PostComposer.vue";
import PostCard from "../components/PostCard.vue";
import { useSession } from "../session";
import type { Post } from "../domain";

const route = useRoute();
const router = useRouter();
const session = useSession();
const posts = ref<Post[]>([]);
const loading = ref(false);
const error = ref("");
const postCount = computed(() => posts.value.length);
const likedCount = computed(() => posts.value.filter((post) => post.liked).length);

async function handleError(cause: unknown): Promise<void> {
  if (cause instanceof ApiError && cause.status === 401) {
    session.markAnonymous();
    await router.replace({ name: "login", query: { redirect: route.fullPath } });
    return;
  }
  error.value = cause instanceof Error ? cause.message : "Errore inatteso";
}

async function loadPosts(): Promise<void> {
  loading.value = true;
  error.value = "";
  try {
    posts.value = await api.listPosts();
  } catch (cause: unknown) {
    await handleError(cause);
  } finally {
    loading.value = false;
  }
}

async function createPost(text: string): Promise<void> {
  try {
    posts.value = [await api.createPost(text), ...posts.value];
  } catch (cause: unknown) {
    await handleError(cause);
  }
}

async function toggleLike(id: string): Promise<void> {
  const current = posts.value.find((post) => post.id === id);
  if (!current) return;
  try {
    const updated = await api.setLiked(id, !current.liked);
    posts.value = posts.value.map((post) => post.id === id ? updated : post);
  } catch (cause: unknown) {
    await handleError(cause);
  }
}

async function deletePost(id: string): Promise<void> {
  try {
    await api.deletePost(id);
    posts.value = posts.value.filter((post) => post.id !== id);
  } catch (cause: unknown) {
    await handleError(cause);
  }
}

// TODO milestone 12:
// - importa createRealtimeClient/applyRealtimeEvent;
// - registra il lifecycle una sola volta e fai cleanup in onUnmounted;
// - AVVIA connect e primo snapshot insieme;
// - mentre GET /api/posts e in volo, accoda gli eventi ricevuti;
// - applica gli eventi accodati allo snapshot prima di sostituire posts;
// - quando arriva il PRIMO onConnect, esegui comunque un nuovo resync:
//   socket.connect() e asincrono e il primo GET potrebbe essere terminato prima
//   dell'handshake, lasciando altrimenti una finestra di perdita;
// - al reconnect ripeti lo stesso resync snapshot + coda eventi;
// - non accettare payload socket come Post senza runtime validation.

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
