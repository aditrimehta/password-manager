/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // scan all React component files
  ],
  theme: {
    extend: {
      colors: {
        primary: '#4f46e5',          // example custom color
        'primary-dark': '#4338ca',
      },
      spacing: {
        128: '32rem',                 // example custom spacing
      },
    },
  },
  plugins: [],                     // add Tailwind plugins here if needed
};
