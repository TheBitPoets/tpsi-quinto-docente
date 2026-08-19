<script setup>
import { computed, reactive, ref, toRef } from "vue";
import PostCard from "./components/PostCard.vue";
const state=reactive({title:"Feed debug"});const title=toRef(state,"title");
const posts=ref([{id:"p1",author:"Ada",text:"Primo",likes:0,liked:false},{id:"p2",author:"Linus",text:"Secondo",likes:1,liked:true}]);
const postCount=computed(()=>posts.value.length);
function addPost(){posts.value=[{id:crypto.randomUUID(),author:"Student",text:"Nuovo",likes:0,liked:false},...posts.value];}
function toggleLike(id){posts.value=posts.value.map(post=>post.id===id?{...post,liked:!post.liked}:post);}
</script>
<template><main><h1>{{ title }}</h1><p>Post: {{ postCount }}</p><button @click="addPost">Aggiungi</button><PostCard v-for="post in posts" :key="post.id" :post="post" @toggle-like="toggleLike"/></main></template>
