// path: frontend/stores/auth.ts

import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null as string | null,
    user: null as { email: string; name: string } | null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(email: string, password: string): Promise<{ success: boolean; message: string | null }> { // Return object
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
        })

        if (response.ok) {
          const data = await response.json()
          this.token = data.access_token
          // For now, let's keep the user object simple
          this.user = { email: email, name: 'User' } // Simplified user object
          console.log("Login successful, token set."); // Add success log
          return { success: true, message: null }; // Return success
        } else {
          // Try to get the specific error detail from the backend
          let errorMessage = 'Login failed. Please check your credentials.'; // Default error
          try {
            const errorData = await response.json();
            if (errorData && errorData.detail) {
              errorMessage = errorData.detail; // Use backend's specific message
            }
          } catch (e) {
            // Ignore if response is not JSON or doesn't have detail
            console.error('Could not parse error response JSON:', e);
          }
          console.error('Login failed:', errorMessage, 'Status:', response.status); // Log the specific message
          return { success: false, message: errorMessage }; // Return failure and message
        }
      } catch (error) {
        console.error('API call failed during login:', error);
        return { success: false, message: 'An unexpected error occurred. Please try again.' }; // Return failure and generic message
      }
    },
    logout() {
      this.token = null
      this.user = null
      console.log("User logged out."); // Add logout log
    },
  },
})