<script setup>
import { reactive, ref } from "vue";
import PostCard from "./components/PostCard.vue";

const state = reactive({ title: "Feed debug" });
const { title } = state;
const posts = ref([
  { id:"p1", author:"Ada", text:"Primo", likes:0, liked:false },
  { id:"p2", author:"Linus", text:"Secondo", likes:1, liked:true },
]);
const postCount = ref(posts.value.length);

function addPost(){posts.value=[{id:crypto.randomUUID(),author:"Student",text:"Nuovo",likes:0,liked:false},...posts.value];}
function toggleLike(id){const p=posts.value.find(x=>x.id===id);if(p)p.liked=!p.liked;}
</script>
<template><main><h1>{{ title }}</h1><p>Post: {{ postCount }}</p><button @click="addPost">Aggiungi</button><PostCard v-for="(post,index) in posts" :key="index" :post="post" @toggle-like="toggleLike"/></main></template>
