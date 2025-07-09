<template>
  <div id="app">
    <div class="ContainerTexto">
      <h1 v-if="usuarioIdentificadoNome">
        <b>{{ usuarioIdentificadoNome }}</b> é você?
      </h1>
      <h1 v-if="!usuarioIdentificadoNome">Olá, há alguém aí?</h1>
    </div>

    <div class="ContainerFace" v-if="metodoRegistroSelecionado == 'Face'">
      <DotLottieVue class="AniFace" />
      <div class="img_cam">
        <CameraCaptura
          ref="CameraCaptura"
          @frameCapturado="armazenarFace($event)"
          v-if="metodoRegistroSelecionado == 'Face'"
        />
      </div>
    </div>

    <div class="ContainerTeclado" v-if="metodoRegistroSelecionado == 'Senha'">
      <TecladoNumerico ref="TecladoNumerico" @senha_digitada="armazenarSenha($event)" />
    </div>

    <div class="ContainerBotoes">
      <button @click="reconhecerCredenciais()">Reconhecer</button>
      <button @click="registrarCredenciais()">Confirmar</button>
      <div>
        <div></div>
        <button @click="alterarMetodoRegistro('Face')" v-if="metodoRegistroSelecionado == 'Senha'">
          Alterar para Face
        </button>
        <button @click="alterarMetodoRegistro('Senha')" v-if="metodoRegistroSelecionado == 'Face'">
          Alterar para Teclado
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import DotLottieVue from './reutilizaveis/AnimacaoFace.vue'
import CameraCaptura from './reutilizaveis/CameraCaptura.vue'
import TecladoNumerico from './reutilizaveis/TecladoNumerico.vue'

export default {
  name: 'App',
  components: {
    DotLottieVue,
    CameraCaptura,
    TecladoNumerico,
  },
  data() {
    return {
      mostrarCapturaVideo: true,
      videoFeedUrl: '/video_feed',
      usuarioIdentificado: '/usuario',
      usuarioIdentificadoNome: '',
      metodoRegistroSelecionado: 'Face',
      chaveRegistro: '',
      matrix_face: '',
      matrix_digital: '',
      matrix_retina: '',
      matrix_senha: '',
    }
  },
  methods: {
    limparTodasMatrix() {
      this.matrix_face = ''
      this.matrix_digital = ''
      this.matrix_retina = ''
      this.matrix_senha = ''
    },
    limparChaveRegistro() {
      this.chaveRegistro = ''
    },
    armazenarSenhaDigitada(evento) {
      this.matrix_senha = evento
    },
    alterarMetodoRegistro(evento) {
      this.metodoRegistroSelecionado = evento
      this.limparTodasMatrix()
      this.limparChaveRegistro()
    },
    armazenarFace(evento) {
      this.matrix_face = evento
    },
    armazenarSenha(evento) {
      this.matrix_senha = evento
    },
    emitirRegistros() {
      if (this.metodoRegistroSelecionado == 'Face') {
        this.$refs.CameraCaptura.captureFrame()
      }
      if (this.metodoRegistroSelecionado == 'Senha') {
        this.$refs.TecladoNumerico.emitirSenha()
      }
    },
    async enviarCredenciaisReconhecimento() {
      let response = ''
      try {
        response = await fetch('/reconhecer_credenciais', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            matrix_face: this.matrix_face,
            matrix_digital: this.matrix_digital,
            matrix_retina: this.matrix_retina,
            matrix_senha: this.matrix_senha,
            chave_registro: this.chaveRegistro,
          }),
        })
        const data = await response.json()
        if (data.status == 200) {
          return data
        }
        if (data.status == 400) {
          alert(data.erro)
        }
      } catch (error) {
        console.error('Erro ao armazenar imagem:', error.message)
      }
    },
    async reconhecerCredenciais() {
      this.emitirRegistros()
      const data = await this.enviarCredenciaisReconhecimento()
      if (!data) {
        this.limparTodasMatrix()
        return console.error('Erro ao armazenar imagem')
      }
      try {
        this.usuarioIdentificadoNome = await data.nome
        this.chaveRegistro = await data.chave_registro
        if (data.status_registro == 200 || data.status == 400) {
          this.limparTodasMatrix()
          this.limparChaveRegistro()
        }
      } catch (error) {
        console.error('Erro ao buscar o nome do usuário:', error)
      }
    },
    async registrarCredenciais() {
      let response = ''
      try {
        response = await fetch('/registro_ponto', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            matrix_face: this.matrix_face,
            matrix_digital: this.matrix_digital,
            matrix_retina: this.matrix_retina,
            matrix_senha: this.matrix_senha,
            chave_registro: this.chaveRegistro,
          }),
        })
        const data = await response.json()
        if (data.status == 200) {
          return data
        }
        if (data.status == 400) {
          alert(data.erro)
        }
      } catch (error) {
        console.error('Erro ao armazenar imagem:', error.message)
      }
    },
  },
  mounted() {},
}
</script>

<style scoped>
.ContainerTexto {
  justify-items: center;
}
.ContainerTeclado {
  justify-items: center;
}
.ContainerBotoes {
  display: flex;
  justify-content: center;
}
.ContainerBotoes button {
  width: 13vw;
  height: 6vh;
  margin: 3vh 2vw;
}
#app {
  display: flex;
  flex-direction: column;
  text-align: center;
  justify-content: space-between;
  min-width: 100vw;
  min-height: 100vh;
}

.ContainerFace {
  /*position: relative; /* Define a posição relativa para o contêiner */
  display: flex; /* Para garantir que a animação e a imagem se alinhem na mesma área */
  flex-direction: center;
  text-align: center;
  justify-content: center;
}

.AniFace {
  position: relative; /* A animação será posicionada de forma absoluta dentro do contêiner */
  top: 0; /* Ajuste conforme necessário para a posição desejada */
  left: 0; /* Ajuste conforme necessário para a posição desejada */
  z-index: 2; /* A animação estará sobre a imagem */
}

.img_cam {
  position: absolute; /* A imagem ficará atrás da animação */
  z-index: 1; /* A imagem ficará atrás da animação */
  opacity: 0.9; /* Reduz a opacidade da imagem (0.0 a 1.0) */
  /*left: 34.7vw; /* Ajuste conforme necessário para a posição desejada */
}
</style>
