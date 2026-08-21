<script setup>
import { computed, ref } from "vue";

const count = ref(0);
const doubled = computed(() => count.value * 2);
</script>

<template>
  <main>
    <h1>Vue translation source</h1>
    <p>count: {{ count }}</p>
    <p>doubled: {{ doubled }}</p>
    <button type="button" @click="count++">+1</button>
  </main>
</template>
