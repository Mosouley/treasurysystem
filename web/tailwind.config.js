/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        sans: "'cairo'",
        Poppins: "'Poppins', 'sans-serif'",
        Quicksand: "'Quicksand', 'sans-serif'",
        Lato: "'Lato'",
        monfont:
        "Inter var, ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', Segoe UI Symbol, 'Noto Color Emoji'",
        sideFont:'Euclid Circular A'
      },
      colors: {
        primary: "#7375de",
        main_one: "#4798af",
        main_two: "#5e83c9",
        main_four: "#885efb",
        main_five: "#966af0",
        my_primary: "#4f0fc4",
        "col-rgba": "rgba( 210, 210, 210, 0.25 )",
        base_color: "#8584d3",
      },
      boxShadow: {
        "3xl": "0 35px 60px -15px rgba(0, 0, 0, 0.3)",
      },
    },
  },
  plugins: [],
};


