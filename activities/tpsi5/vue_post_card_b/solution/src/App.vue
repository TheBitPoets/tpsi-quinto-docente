<script setup>
import { ref } from "vue";
import PostCard from "./components/PostCard.vue";
const post=ref({id:"p-1",author:"Ada",text:"Props down, events up",likes:2,liked:false});
const lastEvent=ref("nessuno");
function toggleLike(id){lastEvent.value=`toggle-like:${id}`;post.value={...post.value,liked:!post.value.liked,likes:post.value.liked?post.value.likes-1:post.value.likes+1};}
function removePost(id){lastEvent.value=`delete:${id}`;}
</script>
<template><main><h1>PostCard contract</h1><PostCard :post="post" :can-delete="true" @toggle-like="toggleLike" @delete="removePost"/><p>Ultimo evento: {{ lastEvent }}</p></main></template>
