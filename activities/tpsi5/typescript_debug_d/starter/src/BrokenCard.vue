<script setup lang="ts">
const props = defineProps<{ id: string }>();
const emit = defineEmits<{ delete: [id: string] }>();

function remove(): void {
  // Bug 4: il contratto richiede string, ma viene emesso un number.
  emit("delete", 42);
}
</script>

<template><button type="button" @click="remove">Elimina {{ props.id }}</button></template>
