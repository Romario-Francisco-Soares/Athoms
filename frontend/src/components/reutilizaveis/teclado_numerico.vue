<template>
  <div class="teclado">
    <div class="display-digitado">{{ conteudoDigitado }}</div>
    <div class="keyboard">
      <div class="key" v-for="n in 9" :key="n" @click="armazenarDigitos(n)">{{ n }}</div>
      <div class="key" @click="armazenarDigitos(0)">0</div>
    </div>
    <div class="apagar" v-show="!verificado" @click="apagarUltDigito">Apagar</div>
    <button class="btn-confirmar" @click="emitirSenha" v-show="conteudoDigitado.length > 0">Confirmar</button>
  </div>
</template>

<style scoped>
.teclado {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
.display-digitado {
  font-size: 2rem;
  margin-bottom: 1rem;
  letter-spacing: 0.2em;
  color: #222;
  background: #f3f4f6;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  min-width: 120px;
  text-align: center;
}
.keyboard {
  display: grid;
  grid-template-columns: repeat(5, 60px);
  gap: 10px;
  margin-bottom: 1rem;
}
.key,
.apagar {
  width: 60px;
  height: 60px;
  background-color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  border: 2px solid #ccc;
  color: #201010;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
  user-select: none;
}
.key:hover {
  background-color: #e0e7ff;
}
.apagar {
  width: 100%;
  margin: 1vw 2vh;
  background: #dc2626;
  color: #fff;
  font-weight: bold;
}
.btn-confirmar {
  background: #4f46e5;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.5rem 1.2rem;
  font-size: 1rem;
  margin-top: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-confirmar:hover {
  background: #3730a3;
}
@media (max-width: 700px) {
  .keyboard {
    grid-template-columns: repeat(5, 40px);
  }
  .key, .apagar {
    width: 40px;
    height: 40px;
    font-size: 1.1rem;
  }
}
</style>

<script>
export default {
  name: 'TecladoNumerico',
  data() {
    return {
      verificado: false,
      conteudoDigitado: '',
      opcaoLimpar: false,
      nomeProfissional: '',
    }
  },
  methods: {
    apagarUltDigito() {
      this.conteudoDigitado = this.conteudoDigitado.slice(0, -1)
    },
    armazenarDigitos(valor) {
      this.conteudoDigitado += valor
    },
    emitirSenha() {
      this.$emit('senha_digitada', this.conteudoDigitado)
    },
  },
  watch: {
    conteudoDigitado() {
      if (this.conteudoDigitado != '') {
        this.opcaoLimpar = true
      }
    },
  },
}
</script>
