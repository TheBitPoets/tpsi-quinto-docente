<script setup>
import { computed, onMounted, ref } from "vue";
import { api, ApiError } from "./api.js";
import AuthPanel from "./components/AuthPanel.vue";
import PostComposer from "./components/PostComposer.vue";
import PostCard from "./components/PostCard.vue";

const user=ref(null);const posts=ref([]);const loading=ref(false);const error=ref("");
const loggedIn=computed(()=>Boolean(user.value));
const postCount=computed(()=>posts.value.length);
const likedCount=computed(()=>posts.value.filter(post=>post.liked).length);
const messageOf=(e)=>e instanceof Error?e.message:"Errore inatteso";

async function loadPosts(){posts.value=await api.listPosts();}
async function bootstrap(){loading.value=true;error.value="";try{const payload=await api.me();user.value=payload.user;await loadPosts();}catch(e){if(!(e instanceof ApiError&&e.status===401))error.value=messageOf(e);}finally{loading.value=false;}}
async function login(credentials){loading.value=true;error.value="";try{user.value=(await api.login(credentials)).user;await loadPosts();}catch(e){error.value=messageOf(e);}finally{loading.value=false;}}
async function register(credentials){loading.value=true;error.value="";try{user.value=(await api.register(credentials)).user;await loadPosts();}catch(e){error.value=messageOf(e);}finally{loading.value=false;}}
async function logout(){loading.value=true;error.value="";try{await api.logout();user.value=null;posts.value=[];}catch(e){error.value=messageOf(e);}finally{loading.value=false;}}
async function createPost(text){loading.value=true;error.value="";try{const created=await api.createPost(text);posts.value=[created,...posts.value];}catch(e){error.value=messageOf(e);}finally{loading.value=false;}}
async function toggleLike(id){const current=posts.value.find(post=>post.id===id);if(!current)return;loading.value=true;error.value="";try{const updated=await api.setLiked(id,!current.liked);posts.value=posts.value.map(post=>post.id===id?updated:post);}catch(e){error.value=messageOf(e);}finally{loading.value=false;}}
async function deletePost(id){loading.value=true;error.value="";try{await api.deletePost(id);posts.value=posts.value.filter(post=>post.id!==id);}catch(e){error.value=messageOf(e);}finally{loading.value=false;}}
onMounted(bootstrap);
</script>
<template>
  <main class="shell">
    <header class="hero"><div><p class="eyebrow">Milestone 9</p><h1>Feisbuc Vue SPA</h1></div><button v-if="loggedIn" :disabled="loading" type="button" @click="logout">Logout</button></header>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <AuthPanel v-if="!loggedIn" :loading="loading" @login="login" @register="register" />
    <template v-else>
      <p>Utente: <strong>{{ user.displayName }}</strong> · post {{ postCount }} · liked {{ likedCount }}</p>
      <PostComposer :disabled="loading" @create="createPost" />
      <section aria-labelledby="feed-title"><h2 id="feed-title">Feed</h2><p v-if="posts.length===0">Nessun post.</p><PostCard v-for="post in posts" :key="post.id" :post="post" :can-delete="post.authorId===user.id" @toggle-like="toggleLike" @delete="deletePost" /></section>
    </template>
  </main>
</template>
