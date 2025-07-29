<template>
  <div ref="lottieContainer" class="lottie-container" aria-label="Animação"></div>
  <div v-if="carregando" class="loading-msg">Carregando animação...</div>
  <div v-if="erro" class="erro-msg">Erro ao carregar animação</div>
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
      embed: '/gifs',
      carregando: false,
      erro: false
    }
  },

  methods: {
    async obterGif(file) {
      try {
        this.carregando = true
        this.erro = false
        const response = await fetch(`${this.embed}/${file}`)
        const data = await response.json()
        this.carregando = false
        if (response.status === 200) {
          return data.gif
        } else {
          this.erro = true
          return null
        }
      } catch (error) {
        this.carregando = false
        this.erro = true
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
.lottie-container {
  width: 100%;
  max-width: 420px;
  min-height: 200px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
}
.loading-msg, .erro-msg {
  text-align: center;
  color: #666;
  font-size: 1rem;
  margin-top: 1rem;
}
.erro-msg {
  color: #dc2626;
}
</style>
