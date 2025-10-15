<template>
  <div class="flex flex-col min-h-screen">
    <NavBar />
    <main class="container mx-auto p-4 flex-grow">
      <slot />
    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import NavBar from '~/components/NavBar.vue';
import AppFooter from '~/components/AppFooter.vue';
</script>