import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()

  // Redirects to /login if the user is not logged in 
  // AND the user is trying to access any page other than /login.
  if (!authStore.isLoggedIn && to.path !== '/login') {
    return navigateTo('/login')
  }
})