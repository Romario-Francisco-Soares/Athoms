<template>
  <div class="camera-captura">
    <video ref="videoElement" autoplay playsinline aria-label="Câmera"></video>
    <button class="btn-captura" @click="captureFrame" aria-label="Capturar Foto">Capturar</button>
    <img v-if="imageSrc" :src="imageSrc" class="preview-img" alt="Prévia da captura" />
  </div>
</template>

<script>
export default {
  name: 'CameraCaptura',
  data() {
    return {
      imageSrc: '',
    }
  },
  mounted() {
    this.startVideo()
  },
  methods: {
    async startVideo() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true })
        this.$refs.videoElement.srcObject = stream
      } catch (error) {
        console.error('Erro ao acessar a câmera', error)
      }
    },
    captureFrame() {
      const video = this.$refs.videoElement
      if (!video.videoWidth || !video.videoHeight) return null
      const canvas = document.createElement('canvas')
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      const ctx = canvas.getContext('2d')
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      this.imageSrc = canvas.toDataURL('image/png')
      this.$emit('frameCapturado', this.imageSrc)
    },
  },
}
</script>

<style scoped>
.camera-captura {
  display: flex;
  flex-direction: column;
  align-items: center;
}
video, .preview-img {
  width: 100%;
  max-width: 420px;
  height: 320px;
  border-radius: 12px;
  background: #222;
  margin-bottom: 0.5rem;
}
.btn-captura {
  background: #4f46e5;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1.2rem;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-captura:hover {
  background: #3730a3;
}
</style>
