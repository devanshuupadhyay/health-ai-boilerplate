<template>
  <div class="p-8">
    <h1 class="text-3xl font-bold">Settings</h1>
    <p class="mt-2">This is the settings page.</p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ['auth'] // Apply the auth.ts middleware
})
</script>