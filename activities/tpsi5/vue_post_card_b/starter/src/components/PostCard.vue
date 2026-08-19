<script setup>
defineProps({
  post: { type: Object, required: true },
  canDelete: { type: Boolean, default: false },
});

defineEmits(["toggle-like", "delete"]);
</script>

<template>
  <article class="card">
    <h2>{{ post.author }}</h2>
    <p>{{ post.text }}</p>
    <p>Like: {{ post.likes }}</p>
    <!-- TODO B: collega i due button con emit; il delete deve comparire solo per canDelete -->
    <button type="button">{{ post.liked ? "Unlike" : "Like" }}</button>
    <button type="button">Elimina</button>
  </article>
</template>
