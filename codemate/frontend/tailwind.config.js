/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0d1117",
        surface: "#161b22",
        borderc: "#30363d",
        accent: "#f78166",
        accent2: "#79c0ff",
        success: "#56d364",
        textPrimary: "#e6edf3",
        textSecondary: "#8b949e"
      }
    }
  },
  plugins: []
};
