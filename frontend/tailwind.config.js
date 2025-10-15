/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
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
        // Light Theme Colors
        primary: '#F0FDF4',      // A very light green for the background
        secondary: '#ECFCCB',    // A subtle off-white for secondary elements
        accent: '#14B8A6',       // A vibrant teal for highlights and buttons
        text: '#1F2937',         // Dark gray for text
        soft: '#9CA3AF',         // A soft gray for icons or subtle text        
        
        // Dark Theme Colors
        'dark-primary': '#1F2937',      // Inverted light primary
        'dark-secondary': '#4B5563',    // A darker shade for secondary elements
        'dark-accent': '#14B8A6',       // Accent color remains consistent
        'dark-text': '#F0FDF4',         // Inverted light text
        'dark-soft': '#9CA3AF'          // Soft color remains consistent
      },
    },
  },
  plugins: [],
};