// path: frontend/nuxt.config.ts

import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@nuxtjs/i18n',
    '@vee-validate/nuxt',
    '@nuxtjs/color-mode',
  ],

  // Global CSS settings
  css: ['~/assets/css/main.css'],

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
          target: 'http://localhost:8008', // Your backend URL
          changeOrigin: true,
        }
      }
    }
  },

  // Color mode configuration
  colorMode: {
    classSuffix: '',
  },

  // Adds font-sans to the <body> element globally
  app: {
    head: {
      bodyAttrs: {
        class: 'font-sans'
      }
    }
  },

  // --- ADD THIS RUNTIME CONFIG BLOCK ---
  runtimeConfig: {
    // Keys within public are exposed to the frontend
    public: {
      meiliHost: process.env.MEILI_HOST || 'http://localhost:7700', // Use localhost for browser access
      // WARNING: Using Master Key in frontend ONLY for local dev.
      // Generate and use a Search API Key for production!
      meiliKey: process.env.MEILI_SEARCH_KEY || 'chnadukechachanechandukichachikochandikechamchesechatnichatai'
    }
  }
  // --- END RUNTIME CONFIG BLOCK ---
})