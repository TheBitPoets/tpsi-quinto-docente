<script setup lang="ts">
const props = defineProps<{ id: string }>();
const emit = defineEmits<{ delete: [id: string] }>();

function remove(): void {
  emit("delete", props.id);
}
</script>

<template><button type="button" @click="remove">Elimina {{ props.id }}</button></template>
