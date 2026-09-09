<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import AuthPanel from "../components/AuthPanel.vue";
import { useSession } from "../session";
import type { LoginCredentials, RegistrationCredentials } from "../domain";

const route = useRoute();
const router = useRouter();
const session = useSession();
const error = ref("");

function safeRedirect(value: unknown): string {
  if (typeof value !== "string") return "/feed";
  if (!value.startsWith("/") || value.startsWith("//")) return "/feed";
  return value;
}

async function finish(): Promise<void> {
  await router.replace(safeRedirect(route.query.redirect));
}

async function login(credentials: LoginCredentials): Promise<void> {
  error.value = "";
  try {
    await session.login(credentials);
    await finish();
  } catch (cause: unknown) {
    error.value = cause instanceof Error ? cause.message : "Errore autenticazione";
  }
}

async function register(credentials: RegistrationCredentials): Promise<void> {
  error.value = "";
  try {
    await session.register(credentials);
    await finish();
  } catch (cause: unknown) {
    error.value = cause instanceof Error ? cause.message : "Errore autenticazione";
  }
}
</script>

<template>
  <main>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <AuthPanel
      :loading="session.loading.value"
      @login="login"
      @register="register"
    />
  </main>
</template>
