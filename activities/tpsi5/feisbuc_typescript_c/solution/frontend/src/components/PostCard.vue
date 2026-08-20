<script setup lang="ts">
import type { Post } from "../domain";

const props = withDefaults(defineProps<{
  post: Post;
  canDelete?: boolean;
}>(), {
  canDelete: false,
});

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
