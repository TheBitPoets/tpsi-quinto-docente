<script setup>
function goFeed(){
  // BUG: reload completo e path che ignora il mount /vue/.
  window.location.assign("/feed");
}
</script>
<template><main><h1>Router debug</h1><button type="button" @click="goFeed">Feed</button><RouterView /></main></template>
