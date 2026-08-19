<script setup>
const props=defineProps({post:{type:Object,required:true}});const emit=defineEmits(["toggle"]);
function localToggle(){props.post.liked=!props.post.liked;emit("toggle",props.post.id);}
</script>
<template><article><strong>{{ props.post.author }}</strong><p>{{ props.post.text }}</p><button @click="localToggle">{{ props.post.liked?"Unlike":"Like" }}</button></article></template>
