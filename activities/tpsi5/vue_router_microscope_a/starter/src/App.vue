<script setup>
import { useRoute } from "vue-router";
const route = useRoute();
</script>

<template>
  <main class="shell">
    <h1>Vue Router microscope</h1>
    <p>Current route: <code>{{ route.fullPath }}</code></p>
    <nav aria-label="Navigazione laboratorio">
      <RouterLink :to="{ name: 'home' }">Home</RouterLink>
      <RouterLink :to="{ name: 'feed' }">Feed</RouterLink>
      <RouterLink to="/inesistente">404 client</RouterLink>
    </nav>
    <RouterView />
  </main>
</template>

<style>
body{font-family:system-ui,sans-serif;margin:0;background:#f4f5f7;color:#1f2937}.shell{max-width:52rem;margin:auto;padding:2rem}nav{display:flex;gap:1rem;flex-wrap:wrap;margin:1rem 0 2rem}a{color:inherit}.router-link-active{font-weight:700}.panel{background:white;padding:1rem;border-radius:.75rem}
</style>
