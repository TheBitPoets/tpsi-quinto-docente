<script setup lang="ts">
import { ref } from "vue";
import type { LoginCredentials, RegistrationCredentials } from "../domain";

withDefaults(defineProps<{ loading?: boolean }>(), { loading: false });
const emit = defineEmits<{
  login: [credentials: LoginCredentials];
  register: [credentials: RegistrationCredentials];
}>();

const displayName = ref("");
const email = ref("");
const password = ref("");

function login(): void {
  emit("login", { email: email.value, password: password.value });
}

function register(): void {
  emit("register", {
    displayName: displayName.value,
    email: email.value,
    password: password.value,
  });
}
</script>

<template>
  <section class="panel" aria-labelledby="auth-title">
    <h2 id="auth-title">Accedi o registrati</h2>
    <label>Nome <input v-model.trim="displayName" autocomplete="name"></label>
    <label>Email <input v-model.trim="email" type="email" autocomplete="email" required></label>
    <label>Password <input v-model="password" type="password" autocomplete="current-password" required></label>
    <div class="actions">
      <button :disabled="loading" type="button" @click="login">Login</button>
      <button :disabled="loading" type="button" @click="register">Registrati</button>
    </div>
  </section>
</template>
