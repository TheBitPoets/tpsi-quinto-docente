<script setup>
import { ref } from "vue";
defineProps({disabled:{type:Boolean,default:false}});const emit=defineEmits(["create"]);const draft=ref("");function submit(){const text=draft.value.trim();if(!text)return;emit("create",text);draft.value="";}
</script>
<template><form class="panel" @submit.prevent="submit"><label for="post-text">Nuovo post</label><textarea id="post-text" v-model="draft" maxlength="280" rows="3"></textarea><button :disabled="disabled || !draft.trim()">Pubblica</button></form></template>
