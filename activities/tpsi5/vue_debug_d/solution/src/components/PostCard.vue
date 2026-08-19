<script setup>
const props=defineProps({post:{type:Object,required:true}});const emit=defineEmits(["toggle-like"]);
</script>
<template><article><strong>{{ props.post.author }}</strong><p>{{ props.post.text }}</p><button @click="emit('toggle-like',props.post.id)">{{ props.post.liked?"Unlike":"Like" }}</button></article></template>
