// path: frontend/stores/auth.ts

import { defineStore } from 'pinia';

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
      try {
        const response = await fetch('/api/v1/auth/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            username: email,
            password: password,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          this.token = data.access_token;
          this.user = { email: email };
          return true; // Return success status
        } else {
          console.error('Login failed:', await response.json());
          return false; // Return failure status
        }
      } catch (error) {
        console.error('API call failed:', error);
        return false; // Return failure status
      }
    },
    logout() {
      this.token = null;
      this.user = null;
    },
  },
});