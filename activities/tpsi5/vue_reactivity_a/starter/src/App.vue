<script setup>
import { computed, ref } from "vue";

const count = ref(0);
const step = ref(1);
const doubled = computed(() => count.value * 2);
const description = computed(() => `${count.value} × 2 = ${doubled.value}`);

function increment() {
  count.value += step.value;
}

function reset() {
  count.value = 0;
}
</script>

<template>
  <main>
    <h1>Vue reactivity microscope</h1>
    <p data-testid="count">Count: {{ count }}</p>
    <p data-testid="doubled">Doubled: {{ doubled }}</p>
    <p>{{ description }}</p>

    <label>
      Step
      <input v-model.number="step" type="number" min="1" max="5">
    </label>

    <div>
      <button type="button" @click="increment">Incrementa</button>
      <button type="button" @click="reset">Reset</button>
    </div>
  </main>
</template>

<style scoped>
main { max-width: 36rem; margin: 3rem auto; font-family: system-ui, sans-serif; }
label, div { display: block; margin-block: 1rem; }
button { margin-right: .5rem; }
</style>
