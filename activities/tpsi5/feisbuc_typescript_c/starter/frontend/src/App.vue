<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useSession } from "./session.js";

const router = useRouter();
const session = useSession();
const error = ref("");

onMounted(async () => {
  try { await session.ensureKnown(); }
  catch (cause) { error.value = cause instanceof Error ? cause.message : "Errore sessione"; }
});

async function logout() {
  error.value = "";
  try {
    await session.logout();
    await router.replace({ name: "login" });
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : "Errore logout";
  }
}
</script>

<template>
  <div class="shell">
    <header class="hero">
      <div><p class="eyebrow">Milestone 10</p><h1>Feisbuc Vue Router</h1></div>
      <nav aria-label="Navigazione principale">
        <RouterLink :to="{ name: 'feed' }">Feed</RouterLink>
        <RouterLink :to="{ name: 'about' }">About</RouterLink>
        <RouterLink v-if="session.status.value === 'anonymous'" :to="{ name: 'login' }">Login</RouterLink>
      </nav>
      <div v-if="session.loggedIn.value" class="actions">
        <span>{{ session.user.value.displayName }}</span>
        <button :disabled="session.loading.value" type="button" @click="logout">Logout</button>
      </div>
    </header>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <RouterView />
  </div>
</template>
