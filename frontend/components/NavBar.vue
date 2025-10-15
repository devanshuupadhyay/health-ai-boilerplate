<template>
  <Disclosure as="nav" class="bg-primary dark:bg-dark-primary text-text dark:text-dark-text p-4 shadow-lg transition-colors duration-200" v-slot="{ open, close }">
    <div class="container mx-auto">
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <DisclosureButton class="inline-flex items-center justify-center p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-inset focus:ring-accent mr-4">
            <span class="sr-only">Open main menu</span>
            <svg v-if="!open" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-text dark:text-dark-text" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-text dark:text-dark-text" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </DisclosureButton>

          <NuxtLink to="/" class="text-xl font-bold">
            Clinical Note AI
          </NuxtLink>
        </div>

        <div class="flex items-center space-x-4 divide-x divide-secondary dark:divide-dark-secondary">
          <NuxtLink to="/" class="nav-link">Dashboard</NuxtLink>
          <div v-if="authStore.isLoggedIn" class="flex items-center space-x-2 px-4">
            <span class="text-sm">Welcome, {{ authStore.user?.name || 'User' }}</span>
            <button @click="handleLogout" class="bg-accent dark:bg-dark-accent hover:bg-blue-700 text-white font-bold py-1 px-3 rounded-md text-sm focus:outline-none">
              Logout
            </button>
          </div>
          <NuxtLink v-else to="/login" class="nav-link">Login</NuxtLink>
          <div class="pl-4">
            <ThemeSwitcher />
          </div>
        </div>
      </div>

      <DisclosurePanel>
        <div class="flex flex-col space-y-2 pt-2 pb-3">
          <NuxtLink to="/settings" class="block py-2 pl-3 pr-4 nav-link-mobile" @click="close">Settings</NuxtLink>
          <NuxtLink to="/account" class="block py-2 pl-3 pr-4 nav-link-mobile" @click="close">Account</NuxtLink>
        </div>
      </DisclosurePanel>
    </div>
  </Disclosure>
</template>

<script setup lang="ts">
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'
import { useRouter } from '#imports'
import { useAuthStore } from '~/stores/auth'
import ThemeSwitcher from './ThemeSwitcher.vue'

const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  useRouter().push('/login')
}
</script>