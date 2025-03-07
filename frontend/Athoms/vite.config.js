import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/health': {
        target: 'http://localhost:5000', // endereço do servidor backend
        changeOrigin: true,
        secure: false, // Se estiver usando HTTP não seguro
        ws: true, // Se você estiver usando WebSocket para streaming
      },
      '/reg02': {
        target: 'http://localhost:5000', // endereço do servidor backend
        changeOrigin: true,
        secure: false, // Se estiver usando HTTP não seguro
        ws: true, // Se você estiver usando WebSocket para streaming
      },
      '/Tur03': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false, // Se estiver usando HTTP não seguro
        ws: true, // Se você estiver usando WebSocket para streaming
      },
      '/reg04': {
        target: 'https://lottie.host/1b6c0048-56c9-41e9-b2ee-f584c94fe5d8/wTVHd6FSLL.lottie',
        changeOrigin: true,
        secure: false, // Se estiver usando HTTP não seguro
        ws: true, // Se você estiver usando WebSocket para streaming
      },
      '/serv05': {
        target: 'https://lottie.host/1b6c0048-56c9-41e9-b2ee-f584c94fe5d8/wTVHd6FSLL.lottie',
        changeOrigin: true,
        secure: false, // Se estiver usando HTTP não seguro
        ws: true, // Se você estiver usando WebSocket para streaming
      },
      '/confg06': {
        target: 'https://lottie.host/1b6c0048-56c9-41e9-b2ee-f584c94fe5d8/wTVHd6FSLL.lottie',
        changeOrigin: true,
        secure: false, // Se estiver usando HTTP não seguro
        ws: true, // Se você estiver usando WebSocket para streaming
      },
    },
  },
})
