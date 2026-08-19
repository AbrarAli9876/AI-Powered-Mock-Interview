/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],

  theme: {
    extend: {
      fontFamily: {
        display: [
          "Space Grotesk",
          "sans-serif",
        ],
        body: [
          "DM Sans",
          "sans-serif",
        ],
        mono: [
          "JetBrains Mono",
          "monospace",
        ],
      },

      colors: {
        midnight: {
          950: "#070912",
          900: "#0B0F1A",
          800: "#111827",
          700: "#182033",
        },

        signal: {
          violet: "#8B5CF6",
          purple: "#A855F7",
          cyan: "#22D3EE",
          mint: "#2DD4BF",
        },
      },

      boxShadow: {
        glow: "0 0 60px rgba(139, 92, 246, 0.18)",
        "glow-cyan":
          "0 0 50px rgba(34, 211, 238, 0.14)",
      },

      animation: {
        "pulse-slow":
          "pulseSlow 4s ease-in-out infinite",

        "float-slow":
          "floatSlow 6s ease-in-out infinite",

        "grid-move":
          "gridMove 20s linear infinite",
      },

      keyframes: {
        pulseSlow: {
          "0%, 100%": {
            opacity: "0.45",
            transform: "scale(1)",
          },
          "50%": {
            opacity: "0.8",
            transform: "scale(1.08)",
          },
        },

        floatSlow: {
          "0%, 100%": {
            transform: "translateY(0px)",
          },
          "50%": {
            transform: "translateY(-10px)",
          },
        },

        gridMove: {
          "0%": {
            transform: "translateY(0)",
          },
          "100%": {
            transform: "translateY(40px)",
          },
        },
      },
    },
  },

  plugins: [],
};