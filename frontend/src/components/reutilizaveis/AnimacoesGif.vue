<template>
  <div ref="lottieContainer"></div>
</template>

<script>
import lottie from 'lottie-web'

export default {
  name: 'animacaoFace',

  props: {
    animacao_json: String
  },

  data() {
    return {
      embed: '/gifs'
    }
  },

  methods: {
    async obterGif(file) {
      try {
        const response = await fetch(`${this.embed}/${file}`)
        const data = await response.json()
        if (response.status === 200) {
          return data.gif
        } else if (response.status === 500) {
          console.log(data.error)
        }
      } catch (error) {
        console.error('Erro ao buscar a animação:', error)
      }
    },

    async carregarAnimacao(nomeArquivo) {
      const animationData = await this.obterGif(nomeArquivo)
      if (animationData) {
        lottie.loadAnimation({
          container: this.$refs.lottieContainer,
          renderer: 'svg',
          loop: true,
          autoplay: true,
          animationData
        })
      } else {
        console.warn('Animação não carregada:', nomeArquivo)
      }
    }
  },

  async mounted() {
    if (this.animacao_json) {
      await this.carregarAnimacao(this.animacao_json)
    }
  },
}
</script>

<style scoped>
div {}
</style>
