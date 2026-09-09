<script setup>
const props=defineProps({post:{type:Object,required:true},canDelete:{type:Boolean,default:false}}); const emit=defineEmits(["toggle-like","delete"]);
</script>
<template><article class="post" :data-post-id="props.post.id"><header><strong>{{ props.post.author }}</strong></header><p>{{ props.post.text }}</p><footer><button type="button" @click="emit('toggle-like',props.post.id)">{{ props.post.liked ? "Unlike" : "Like" }} · {{ props.post.likes }}</button><button v-if="props.canDelete" type="button" @click="emit('delete',props.post.id)">Elimina</button></footer></article></template>
