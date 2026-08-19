<script setup>
import { ref } from "vue";
defineProps({ loading: { type:Boolean, default:false } });
const emit = defineEmits(["login", "register"]);
const displayName=ref(""); const email=ref(""); const password=ref("");
const login=()=>emit("login",{email:email.value,password:password.value});
const register=()=>emit("register",{displayName:displayName.value,email:email.value,password:password.value});
</script>
<template>
  <section class="panel" aria-labelledby="auth-title">
    <h2 id="auth-title">Accedi o registrati</h2>
    <label>Nome <input v-model.trim="displayName" autocomplete="name"></label>
    <label>Email <input v-model.trim="email" type="email" autocomplete="email" required></label>
    <label>Password <input v-model="password" type="password" autocomplete="current-password" required></label>
    <div class="actions"><button :disabled="loading" type="button" @click="login">Login</button><button :disabled="loading" type="button" @click="register">Registrati</button></div>
  </section>
</template>
