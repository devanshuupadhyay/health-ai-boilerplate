<template>
  <Transition
    enter-active-class="transition-all duration-300 ease-out"
    enter-from-class="opacity-0 translate-x-12"
    enter-to-class="opacity-100 translate-x-0"
    leave-active-class="transition-all duration-200 ease-in"
    leave-from-class="opacity-100 translate-x-0"
    leave-to-class="opacity-0 translate-x-12"
  >
    <div
      v-if="message"
      class="fixed bottom-6 right-6 z-50 max-w-sm rounded-lg bg-secondary p-4 shadow-xl dark:bg-dark-secondary"
    >
      <p class="font-bold text-accent">Cypress is Running:</p>
      <p class="text-sm text-text dark:text-dark-text">{{ message }}</p>
    </div>
  </Transition>
</template>

<script setup lang="ts">
// Get the global message state from our composable
const { message } = useDemoToaster();
</script>