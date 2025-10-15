// path: frontend/nuxt.config.ts

import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@nuxtjs/i18n',
    '@vee-validate/nuxt',
  ],

  // Global CSS settings
  css: [
    '~/assets/css/main.css'
  ],

  // Configuration for Tailwind CSS
  tailwindcss: {
    cssPath: '~/assets/css/main.css',
    configPath: 'tailwind.config.js',
    exposeConfig: false,
    editorSupport: true,
    viewer: false,
  },

  // Correct proxy configuration for Vite development server
  vite: {
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:8008',
          changeOrigin: true,
        }
      }
    }
  }
})