<template>
  <nav class="bg-primary text-text p-4 shadow-lg">
    <div class="container mx-auto flex items-center justify-between">
      <NuxtLink to="/" class="text-xl font-bold nav-link">
        Clinical Note AI
      </NuxtLink>
      <div class="flex items-center space-x-4 divide-x divide-secondary">
        <NuxtLink to="/" class="nav-link">Dashboard</NuxtLink>
        <div v-if="authStore.isLoggedIn" class="flex items-center space-x-2 px-4">
          <span class="text-sm">Welcome, {{ authStore.user?.name || 'User' }}</span>
          <button @click="handleLogout" class="bg-accent hover:bg-blue-700 text-white font-bold py-1 px-3 rounded-md text-sm focus:outline-none">
            Logout
          </button>
        </div>
        <NuxtLink v-else to="/login" class="nav-link">Login</NuxtLink>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  useRouter().push('/login')
}
</script>