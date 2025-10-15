<template>
  <nav class="bg-gray-900 text-white p-4 shadow-lg">
    <div class="container mx-auto flex items-center justify-between">
      <NuxtLink to="/" class="text-xl font-bold hover:text-blue-400">
        Clinical Note AI
      </NuxtLink>
      <div class="flex items-center space-x-4 divide-x divide-gray-700">
        <NuxtLink to="/" class="hover:text-blue-400 px-4">Dashboard</NuxtLink>
        <div v-if="authStore.isLoggedIn" class="flex items-center space-x-2 px-4">
          <span class="text-sm">Welcome, {{ authStore.user?.name || 'User' }}</span>
          <button @click="handleLogout" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded-md text-sm focus:outline-none">
            Logout
          </button>
        </div>
        <NuxtLink v-else to="/login" class="hover:text-blue-400 px-4">Login</NuxtLink>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useRouter } from '#imports'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  useRouter().push('/login')
}
</script>