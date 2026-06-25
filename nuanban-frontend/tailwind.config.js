/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#FF8A65',
        secondary: '#FFB74D',
        warm: '#FFF3E0',
      }
    },
  },
  plugins: [],
}