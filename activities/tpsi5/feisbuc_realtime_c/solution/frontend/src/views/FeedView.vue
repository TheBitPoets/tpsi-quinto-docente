<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api, ApiError } from "../api";
import PostComposer from "../components/PostComposer.vue";
import PostCard from "../components/PostCard.vue";
import { useSession } from "../session";
import type { Post } from "../domain";
import {
  applyRealtimeEvent,
  type RealtimeEvent,
} from "../realtime-events";
import { createRealtimeClient } from "../realtime";

const route = useRoute();
const router = useRouter();
const session = useSession();
const posts = ref<Post[]>([]);
const loading = ref(false);
const error = ref("");
const realtimeStatus = ref<"offline" | "online">("offline");
const postCount = computed(() => posts.value.length);
const likedCount = computed(() => posts.value.filter((post) => post.liked).length);
const realtime = createRealtimeClient();

const queuedEvents: RealtimeEvent[] = [];
let resyncing = false;
let resyncRequested = false;

async function handleError(cause: unknown): Promise<void> {
  if (cause instanceof ApiError && cause.status === 401) {
    session.markAnonymous();
    await router.replace({ name: "login", query: { redirect: route.fullPath } });
    return;
  }
  error.value = cause instanceof Error ? cause.message : "Errore inatteso";
}

function applyOrQueue(event: RealtimeEvent): void {
  if (resyncing) {
    queuedEvents.push(event);
    return;
  }
  posts.value = applyRealtimeEvent(posts.value, event);
}

async function resyncPosts(): Promise<void> {
  if (resyncing) {
    resyncRequested = true;
    return;
  }

  resyncing = true;
  resyncRequested = false;
  loading.value = true;
  error.value = "";
  try {
    const snapshot = await api.listPosts();
    let next = snapshot;
    for (const event of queuedEvents) {
      next = applyRealtimeEvent(next, event);
    }
    posts.value = next;
  } catch (cause: unknown) {
    await handleError(cause);
  } finally {
    queuedEvents.splice(0);
    resyncing = false;
    loading.value = false;
    if (resyncRequested) void resyncPosts();
  }
}

async function createPost(text: string): Promise<void> {
  loading.value = true;
  error.value = "";
  try {
    const created = await api.createPost(text);
    posts.value = applyRealtimeEvent(posts.value, { type: "post:created", post: created });
  } catch (cause: unknown) {
    await handleError(cause);
  } finally {
    loading.value = false;
  }
}

async function toggleLike(id: string): Promise<void> {
  const current = posts.value.find((post) => post.id === id);
  if (!current) return;
  loading.value = true;
  error.value = "";
  try {
    const updated = await api.setLiked(id, !current.liked);
    posts.value = applyRealtimeEvent(posts.value, { type: "post:updated", post: updated });
  } catch (cause: unknown) {
    await handleError(cause);
  } finally {
    loading.value = false;
  }
}

async function deletePost(id: string): Promise<void> {
  loading.value = true;
  error.value = "";
  try {
    await api.deletePost(id);
    posts.value = applyRealtimeEvent(posts.value, { type: "post:deleted", postId: id });
  } catch (cause: unknown) {
    await handleError(cause);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  if (session.status.value !== "authenticated") {
    void resyncPosts();
    return;
  }

  realtime.start({
    onEvent(event) {
      applyOrQueue(event);
    },
    onConnect() {
      realtimeStatus.value = "online";
    },
    onReconnect() {
      realtimeStatus.value = "online";
      void resyncPosts();
    },
    onDisconnect() {
      realtimeStatus.value = "offline";
    },
    onError(message) {
      realtimeStatus.value = "offline";
      error.value = `Realtime: ${message}`;
    },
  });

  // Apriamo il realtime prima dello snapshot. Gli eventi ricevuti mentre
  // GET /api/posts e in volo vengono accodati e applicati allo snapshot:
  // cosi non esiste una finestra snapshot -> connect in cui perdere update.
  void resyncPosts();
});

onUnmounted(() => realtime.stop());
</script>

<template>
  <main>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <p>Post {{ postCount }} · liked {{ likedCount }} · realtime {{ realtimeStatus }}</p>
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
