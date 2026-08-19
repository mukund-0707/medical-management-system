/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Inter Tight"', 'Inter', 'sans-serif'],
        inter:   ['Inter', 'sans-serif'],
        serif:   ['"Instrument Serif"', 'Georgia', 'serif'],
      },
      colors: {
        gold: {
          50:  '#fffaeb',
          100: '#fdf0c8',
          200: '#fbe08c',
          300: '#f8cd5a',
          400: '#f5c24c',
          500: '#e0a526',
          600: '#c2861a',
          700: '#a9761a',
          800: '#7c5512',
          900: '#54390c',
          950: '#2c1d06',
        },
        // Neutral, camera-clean base — replaces the old brownish black
        ink: {
          DEFAULT: '#07070a',
          950: '#07070a',
          900: '#0b0b10',
          800: '#101017',
          700: '#16161f',
          600: '#1d1d28',
          500: '#262632',
        },
        mint: '#6ee7b7',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.75rem',
      },
      animation: {
        'fade-up':   'fadeUp 0.7s cubic-bezier(0.22,1,0.36,1) both',
        'fade-in':   'fadeIn 0.6s ease both',
        'float':     'float 7s ease-in-out infinite',
        'drift':     'drift 22s ease-in-out infinite',
        'marquee':   'marquee 38s linear infinite',
        'shimmer':   'shimmerMove 3.2s linear infinite',
        'pulse-ring':'pulseRing 2.4s cubic-bezier(0.4,0,0.6,1) infinite',
        'scan':      'scan 3.4s ease-in-out infinite',
      },
      keyframes: {
        fadeUp: {
          from: { opacity: '0', transform: 'translateY(28px)' },
          to:   { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          from: { opacity: '0' },
          to:   { opacity: '1' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':      { transform: 'translateY(-14px)' },
        },
        drift: {
          '0%, 100%': { transform: 'translate3d(0,0,0) scale(1)' },
          '33%':      { transform: 'translate3d(6%,-8%,0) scale(1.12)' },
          '66%':      { transform: 'translate3d(-7%,6%,0) scale(0.94)' },
        },
        marquee: {
          from: { transform: 'translateX(0)' },
          to:   { transform: 'translateX(-50%)' },
        },
        shimmerMove: {
          '0%':   { backgroundPosition: '-200% center' },
          '100%': { backgroundPosition: '200% center' },
        },
        pulseRing: {
          '0%':   { transform: 'scale(0.85)', opacity: '0.6' },
          '70%':  { transform: 'scale(1.6)',  opacity: '0' },
          '100%': { transform: 'scale(1.6)',  opacity: '0' },
        },
        scan: {
          '0%':   { transform: 'translateY(0%)',    opacity: '0' },
          '12%':  { opacity: '0.9' },
          '50%':  { transform: 'translateY(560%)',  opacity: '0.9' },
          '88%':  { opacity: '0' },
          '100%': { transform: 'translateY(0%)',    opacity: '0' },
        },
      },
    },
  },
  plugins: [],
}
