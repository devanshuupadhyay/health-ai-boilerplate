<template>
  <div>
    <AppHeader />
    <main class="container mx-auto p-4">
      <slot />
    </main>
  </div>
</template>

<script setup>
import AppHeader from '~/components/AppHeader.vue';
</script>