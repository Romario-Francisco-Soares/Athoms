<template>
  <div ref="lottieContainer"></div>
</template>

<script>
import lottie from 'lottie-web'

export default {
  name: 'animacaoFace',
  data() {
    return {
      embed: '/gif_scanner',
    }
  },
  methods: {
    async obterGif() {
      try {
        const response = await fetch(this.embed)
        const data = await response.json()
        return data.gif
      } catch (error) {
        console.error('Erro ao buscar a animação:', error)
      }
    },
  },
  async mounted() {
    const animationData = await this.obterGif()
    lottie.loadAnimation({
      container: this.$refs.lottieContainer,
      renderer: 'svg',
      loop: true,
      autoplay: true,
      animationData,
    })
  },
}
</script>

<style scoped>
div {
  width: 500px;
  height: 500px;
}
</style>
