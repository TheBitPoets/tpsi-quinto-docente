<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import AuthPanel from "../components/AuthPanel.vue";
import { useSession } from "../session.js";

const route = useRoute();
const router = useRouter();
const session = useSession();
const error = ref("");

function safeRedirect(value) {
  if (typeof value !== "string") return "/feed";
  if (!value.startsWith("/") || value.startsWith("//")) return "/feed";
  return value;
}

async function completeAuth(operation, credentials) {
  error.value = "";
  try {
    await operation(credentials);
    await router.replace(safeRedirect(route.query.redirect));
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : "Errore autenticazione";
  }
}
</script>

<template>
  <main>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <AuthPanel
      :loading="session.loading.value"
      @login="completeAuth(session.login, $event)"
      @register="completeAuth(session.register, $event)"
    />
  </main>
</template>
