<script setup lang="ts">
import type { Post } from "../domain";

// TODO: sostituisci il contratto troppo largo con props/emits type-based.
const props = defineProps<{ post: Post; canDelete?: boolean }>();
const emit = defineEmits<{
  "toggle-like": [id: string];
  delete: [id: string];
}>();
</script>

<template>
  <article class="post" :data-post-id="props.post.id">
    <header><strong>{{ props.post.author }}</strong></header>
    <p>{{ props.post.text }}</p>
    <footer>
      <button type="button" @click="emit('toggle-like', props.post.id)">
        {{ props.post.liked ? "Unlike" : "Like" }} · {{ props.post.likes }}
      </button>
      <button v-if="props.canDelete" type="button" @click="emit('delete', props.post.id)">Elimina</button>
    </footer>
  </article>
</template>
