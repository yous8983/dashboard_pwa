import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "Project Manager",
        short_name: "ProjMgr",
        icons: [{ src: "icon.png", sizes: "192x192", type: "image/png" }], // Ajoutez une icône plus tard
      },
    }),
  ],
});
