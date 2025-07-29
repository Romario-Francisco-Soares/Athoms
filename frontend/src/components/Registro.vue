<template>
  <div id="app">
    <div class="botaoRetornarEsquerdoSuperior">
      <button v-if="conectado">Sair</button>
    </div>
    <video class="video-bg" autoplay muted loop playsinline>
      <source src="../assets/tecvideo.mp4" type="video/mp4" />
      Seu navegador não suporta vídeo HTML5.
    </video>
    <div class="ContainerTexto">
      <h1 v-if="usuarioIdentificadoNome">
        <b>{{ usuarioIdentificadoNome }}</b> é você?
      </h1>
      <h1 v-if="!usuarioIdentificadoNome">Olá, há alguém aí?</h1>
    </div>

    <div class="ContainerFace" v-if="metodoRegistroSelecionado == 'Face'">
      <Gifs id="DotLottieVue" class="AniFace" :animacao_json="nm_anima_json"/>
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

    <UiAlert :show="showAlert" :message="alertMessage" :type="alertType" @close="showAlert = false" />
  </div>
</template>

<script>
import Gifs from './reutilizaveis/animacoes_gif.vue'
import CameraCaptura from './reutilizaveis/camera_captura.vue'
import TecladoNumerico from './reutilizaveis/teclado_numerico.vue'
import UiAlert from './UiAlert.vue'

export default {
  name: 'App',
  components: {
    Gifs,
    CameraCaptura,
    TecladoNumerico,
    UiAlert
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
      conectado: false,
      nm_anima_json: 'AnimacaoFace.json',
      showAlert: false,
      alertMessage: '',
      alertType: 'info'
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
    showUiAlert(msg, type = 'info') {
      this.alertMessage = msg
      this.alertType = type
      this.showAlert = true
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
          credentials: 'include',
        })
        const data = await response.json()
        if (data.status == 200) {
          return data
        }
        if (data.status == 400) {
          this.showUiAlert(data.erro || 'Erro ao reconhecer credenciais', 'error')
        }
      } catch (error) {
        console.error('Erro ao armazenar imagem:', error.message)
        this.showUiAlert('Erro ao reconhecer credenciais', 'error')
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
          credentials: 'include',
        })
        const data = await response.json()
        if (data.status == 200) {
          this.showUiAlert(data.message || 'Registro realizado com sucesso!', 'success')
          return data
        }
        if (data.status == 400) {
          this.showUiAlert(data.erro || 'Erro ao registrar', 'error')
        }
      } catch (error) {
        console.error('Erro ao armazenar imagem:', error.message)
        this.showUiAlert('Erro ao registrar', 'error')
      }
    },
    async cadastrarUsuario(usuario) {
      try {
        const response = await fetch('/usuario', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            ...usuario,
            acao: 'inserir'
          }),
          credentials: 'include'
        })
        const data = await response.json()
        if (!response.ok) {
          this.showUiAlert(data.error || 'Erro ao cadastrar usuário', 'error')
          return false
        }
        this.showUiAlert(data.return_post || 'Usuário cadastrado com sucesso!', 'success')
        return true
      } catch (error) {
        this.showUiAlert('Erro ao cadastrar usuário', error)
        return false
      }
    },
  },
  mounted() {},
}
</script>

<style scoped>
.botaoRetornarEsquerdoSuperior {
  width: 250px;
  height: 250px;
  background-color: rgba(97, 241, 119, 0.6);
  border-radius: 50%;
  position: relative;
  top: -15vh;
  left: -5vw;
}
.botaoRetornarEsquerdoSuperior button{
  width: 3vw;
  height: 5vh;
  position: relative;
  border-radius: 50%;
  background: none;
  border: none;
  top: 25vh;
  left: 0vw;
  font-family: 'Arial', sans-serif;
  font-size: clamp(1vw, 2vw, 1.2vw);
  font-weight: bold;
  color: white;
}
.video-bg {
  position: fixed;
  top: 0;
  left: 0;
  min-width: 100%;
  min-height: 100%;
  object-fit: cover;
  z-index: -1;
  opacity: 30%;
}

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
  border-radius: 5vw;
  font-family: 'Arial', sans-serif;
  font-size: clamp(10px, 2vw, 1vw);
  font-weight: bold;
  background: #4f46e5;
  color: #fff;
  border: none;
  transition: background 0.2s;
}
.ContainerBotoes button:hover {
  background: #3730a3;
}
#DotLottieVue{
  background-color: rgb(2, 71, 28, 0.6);
  width: 420px;
  border-radius: 1.5vw;

}
#app {
  display: flex;
  flex-direction: column;
  text-align: center;
  justify-content: space-between;
  min-width: 100vw;
  min-height: 100vh;
  background: linear-gradient(90deg,
                      rgba(12, 63, 15, 0.6),   /* #0c3f0f */
                      rgba(111, 220, 127, 0.6),/* #6fdc7f */
                      rgba(79, 196, 106, 0.6), /* #4fc46a */
                      rgba(58, 173, 90, 0.6)   /* #3aad5a */);
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
