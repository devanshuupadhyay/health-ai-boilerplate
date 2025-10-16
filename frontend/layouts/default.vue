<template>
  <div class="flex flex-col min-h-screen">
    <NavBar />
    <main class="flex-grow flex items-center justify-center p-4">
      <slot />
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import NavBar from '~/components/NavBar.vue';
import AppFooter from '~/components/AppFooter.vue';
</script>