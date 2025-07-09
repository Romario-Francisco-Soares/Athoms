<template>
  <div>
    <video ref="videoElement" autoplay playsinline></video>
    <!--<img :src="imageSrc" />-->
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
    /*setInterval(this.captureFrame, 2000)*/
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
video,
img {
  width: 420px;
  height: 400px;
}
</style>
