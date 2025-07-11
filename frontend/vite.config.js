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
      '/gifs': {
        //GIF
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false,
        ws: true,
      },
      '/usuario': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false,
        ws: true,
      },
      '/video_feed': {
        target: 'http://127.0.0.1:5000', // endereço do servidor backend
        changeOrigin: true,
        secure: false, // Se estiver usando HTTP não seguro
        ws: true, // Se você estiver usando WebSocket para streaming
      },
      '/registro_ponto': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false, // Se estiver usando HTTP não seguro
        ws: true, // Se você estiver usando WebSocket para streaming
      },
      '/reconhecer_credenciais': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false, // Se estiver usando HTTP não seguro
        ws: true, // Se você estiver usando WebSocket para streaming
      },
      '/login': {
        target: 'http://127.0.0.1:5000',
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
