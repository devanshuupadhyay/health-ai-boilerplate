<template>
  <ClientOnly>
    <button
      @click="colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark'"
      class="flex items-center justify-center p-2 rounded-full text-text dark:text-dark-text bg-secondary dark:bg-dark-secondary focus:outline-none transition-colors duration-300"
    >
      <SunIcon v-if="colorMode.value === 'dark'" class="h-5 w-5 text-yellow-500" />
      <MoonIcon v-else class="h-5 w-5 text-gray-400" />
    </button>
  </ClientOnly>
</template>

<script setup lang="ts">
import { SunIcon, MoonIcon } from '@heroicons/vue/24/solid';

const colorMode = useColorMode();
</script>