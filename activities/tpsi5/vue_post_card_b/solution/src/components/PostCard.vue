<script setup>
const props = defineProps({
  post: { type: Object, required: true },
  canDelete: { type: Boolean, default: false },
});
const emit = defineEmits(["toggle-like", "delete"]);
</script>

<template>
  <article class="card" :data-post-id="props.post.id">
    <h2>{{ props.post.author }}</h2>
    <p>{{ props.post.text }}</p>
    <p>Like: {{ props.post.likes }}</p>
    <button type="button" @click="emit('toggle-like', props.post.id)">{{ props.post.liked ? "Unlike" : "Like" }}</button>
    <button v-if="props.canDelete" type="button" @click="emit('delete', props.post.id)">Elimina</button>
  </article>
</template>
