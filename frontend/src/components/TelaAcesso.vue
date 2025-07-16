<template>
  <div class="botao-retornar">
    <button v-if="!conectado" @click="alternarLogin">{{ entraSai }}</button>
  </div>

  <Gifs id="DotLottieVue" class="ani-face" :animacao_json="nmGif" />

  <div class="wrapper fadeInDown" v-if="entrar">
    <div id="formContent">
      <h2 class="active">Conectar</h2>

      <form @submit.prevent="handleLogin">
        <input
          type="text"
          id="login"
          class="fadeIn second"
          name="login"
          placeholder="Usuário"
          v-model="login"
        />
        <input
          type="password"
          id="password"
          class="fadeIn third"
          name="password"
          placeholder="Senha"
          v-model="password"
        />
        <input type="submit" class="fadeIn fourth" value="Confirmar" />
      </form>

      <div id="formFooter">
        <h5 class="underlineHover">Em caso de problemas contate a assistência</h5>
      </div>
    </div>
  </div>
</template>

<script>
import Gifs from './reutilizaveis/animacoes_gif.vue'

export default {
  name: 'AnimacaoFace',
  components: { Gifs },
  data() {
    return {
      nmGif: 'LineasDeteccion.json',
      entrar: false,
      conectado: false,
      login: '',
      password: '',
      entraSai: 'Entrar'
    }
  },
  methods: {
    alternarLogin() {
      this.entrar = !this.entrar
      if (this.entraSai == 'Entrar'){
        this.entraSai = 'Sair'
      }else{
        this.entraSai = 'Entrar'
      }
    },
    async handleLogin() {
      try {
        const resposta = await fetch('/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            login: this.login,
            password: this.password
          }),
          credentials: 'include',  // importante!
        })
        const data = await resposta.json()
        if (!resposta.ok) {
          //throw new Error('Erro ao autenticar')
          alert(data.error)
        }
        else{
          alert(data.message)
          this.emitirLogin()
          this.conectado = true
          this.entrar = false
        }
      } catch (erro) {
        console.error(erro)
        alert('Falha no login.')
      }
    },
    emitirLogin(){
      this.$emit('autorizado_login', true)
    }
  }
}
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css?family=Poppins');

.botao-retornar {
  width: 250px;
  height: 250px;
  background-color: rgba(97, 241, 119, 0.6);
  border-radius: 50%;
  position: absolute;
  top: -15vh;
  left: -5vw;
  z-index: 1;
}

.botao-retornar button {
  width: 3vw;
  height: 5vh;
  position: absolute;
  border-radius: 50%;
  background: none;
  border: none;
  top: 25vh;
  left: 8vw;
  font-family: 'Arial', sans-serif;
  font-size: clamp(2vw, 2vw, 1.2vw);
  font-weight: bold;
  color: white;
  z-index: 2;
}
.ani-face {
  position: absolute;
  top: 0;
  left: 0;
  z-index: -2;
  background-color: rgba(1, 32, 13, 1);
  width: 100%;
  height: 100%;
  border-radius: 1.5vw;
}

.wrapper {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  padding: 20px;
  z-index: 5;
  position: absolute;
  width: 100%;
  height: 100%;
}

#formContent {
  border-radius: 10px;
  background: #afafafd2;
  padding: 30px;
  max-width: 450px;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
  text-align: center;
}

#formFooter {
  background-color: #afafafd2;
  border-top: 1px solid #afafafd2;
  padding: 25px;
  text-align: center;
  border-radius: 0 0 10px 10px;
}

h2.active {
  color: #0d0d0d;
  border-bottom: 2px solid #5fbae9;
}

input[type='text'],
input[type='password'],
input[type='submit'] {
  width: 85%;
  padding: 15px 32px;
  margin: 5px;
  font-size: 16px;
  border-radius: 5px;
  border: 2px solid #085001c7;
  background-color: #afafafd2;
  color: #0d0d0d;
  transition: all 0.5s ease-in-out;
}

input[type='submit'] {
  background-color: #076814e0;
  color: #fff;
  text-transform: uppercase;
  box-shadow: 0 10px 30px rgba(95, 186, 233, 0.4);
  cursor: pointer;
}

input[type='submit']:hover {
  background-color: #029432;
}

input:focus {
  background-color: #fff;
  border-bottom: 2px solid #5fbae9;
  outline: none;
}

.underlineHover {
  position: relative;
  display: inline-block;
  color: #0d0d0d;
  cursor: pointer;
}

.underlineHover::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -10px;
  width: 0;
  height: 2px;
  background-color: #56baed;
  transition: width 0.2s;
}

.underlineHover:hover::after {
  width: 100%;
}

.fadeInDown {
  animation: fadeInDown 2s both;
}

.fadeIn {
  animation: fadeIn 1s ease-in forwards;
}

.fadeIn.second { animation-delay: 0.6s; }
.fadeIn.third { animation-delay: 0.8s; }
.fadeIn.fourth { animation-delay: 1s; }

@keyframes fadeInDown {
  0% { opacity: 0; transform: translateY(-100%); }
  100% { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 900px) {
  .botao-retornar button {
    left: 10vw;
    font-size: clamp(3vw, 2vw, 1.2vw);
  }
  .botao-retornar {
    width: 230px;
    height: 230px;
  }
}
@media (max-width: 600px) {
  .botao-retornar button {
    left: 10vw;
    top: 20vh;
    font-size: clamp(4vw, 2vw, 1.2vw);
  }
  .botao-retornar {
    width: 180px;
    height: 180px;
  }
}

</style>
