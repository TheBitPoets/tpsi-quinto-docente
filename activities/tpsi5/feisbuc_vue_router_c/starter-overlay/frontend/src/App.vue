<script setup>
import { useSession } from "./session.js";
const session = useSession();
// TODO: usa useRouter() per logout -> login e gestisci un eventuale errore layout.
</script>

<template>
  <div class="shell">
    <header class="hero">
      <div><p class="eyebrow">Milestone 10</p><h1>Feisbuc Vue Router</h1></div>
      <!-- TODO: RouterLink verso feed/about/login e logout se autenticato. -->
    </header>
    <p>Session status: {{ session.status.value }}</p>
    <!-- TODO: inserisci RouterView. -->
  </div>
</template>
