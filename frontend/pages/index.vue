<template>
  <div class="p-8">
    <h1 class="text-3xl font-bold">Welcome to the Dashboard</h1>
    <p class="mt-2">Your journey to a better user experience begins here.</p>
    <div class="mt-6">
      <NuxtLink to="/patients" class="btn-primary !w-auto">
        View Patient Dashboard
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: ['auth'] // Apply the auth.ts middleware
})
</script>