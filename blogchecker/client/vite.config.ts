import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      input: path.resolve(__dirname, "src/main.tsx"),
      output: {
        dir: path.resolve(__dirname, ".././static"),
        entryFileNames: "index-bundle.js",
        assetFileNames: "[name].[ext]",
      },
    },
    // cssCodeSplit: false,
    // assetsInlineLimit: 0,
    // copyPublicDir: false,
  },
  publicDir: path.resolve(__dirname, "assets"),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
