// path: frontend/stores/auth.ts

import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null as string | null,
    user: null as any | null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(email: string, password: string) {
      // In a later step, we will add the API call here
      console.log('Logging in with:', email, password);
    },
    logout() {
      this.token = null;
      this.user = null;
      console.log('Logged out');
    },
  },
});