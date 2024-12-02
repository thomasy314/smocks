import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  server: {
    host: "0.0.0.0",
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000", // Replace with your backend URL and port
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""), // Optional, to modify paths
      },
    },
  },
});
