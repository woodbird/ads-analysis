/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f8ff',
          100: '#e5eeff',
          200: '#cddfff',
          300: '#a6c4ff',
          400: '#7aa2ff',
          500: '#5578ff',
          600: '#3355ff',
          700: '#2644e5',
          800: '#1f3bc4',
          900: '#1c359f',
          950: '#0f1c5c',
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
