/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./components/**/*.{vue,js,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./composables/**/*.{js,ts}",
    "./plugins/**/*.{js,ts}",
    "./utils/**/*.{js,ts}",
    "./app.vue",
    "./error.vue",
    "./nuxt.config.ts",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};