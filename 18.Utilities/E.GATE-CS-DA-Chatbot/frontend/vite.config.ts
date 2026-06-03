import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// During `npm run dev`, requests to /api are proxied to the FastAPI backend so
// the browser talks to a single origin (no CORS headaches in development).
// In production, set VITE_API_BASE to your API URL at build time.
const API_TARGET = process.env.VITE_API_PROXY || "http://localhost:8000";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  build: {
    chunkSizeWarningLimit: 900,
    rollupOptions: {
      output: {
        manualChunks: {
          react: ["react", "react-dom"],
          markdown: [
            "react-markdown",
            "remark-gfm",
            "remark-math",
            "rehype-katex",
            "rehype-highlight",
          ],
        },
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: API_TARGET,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
