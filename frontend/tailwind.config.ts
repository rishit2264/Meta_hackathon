import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        pink: {
          50:  '#fff0f3',
          100: '#ffe0e9',
          200: '#ffc2d4',
          300: '#ff9ab8',
          400: '#ff6b9d',
          500: '#e84393',
          600: '#c2185b',
        },
        cream: '#fffaf8',
        charcoal: '#1a1a2e',
        slate: '#4a4a6a',
        muted: '#9090b0',
        border: '#f0d4df',
      },
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
        sans: ['"DM Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
    },
  },
  plugins: [],
}
export default config
