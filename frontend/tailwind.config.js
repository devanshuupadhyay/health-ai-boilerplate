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
    extend: {
      colors: {
        primary: '#004d40',  // A deep, dark teal for the background
        secondary: '#263238', // A neutral dark gray for secondary elements
        accent: '#1e88e5',  // A vibrant blue for highlights and buttons
        text: '#F8FAFC',    // A clean off-white for body text
        soft: '#94A3B8'     // A soft, subtle gray for secondary text or icons
      },
    },
  },
  plugins: [],
};