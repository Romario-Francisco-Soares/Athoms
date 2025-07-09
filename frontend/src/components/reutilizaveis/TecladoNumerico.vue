<template>
  <div class="teclado">
    <div>{{ this.conteudoDigitado }}</div>
    <div class="keyboard">
      <div class="key" v-on:click="armazenarDigitos(1)">1</div>
      <div class="key" v-on:click="armazenarDigitos(2)">2</div>
      <div class="key" v-on:click="armazenarDigitos(3)">3</div>
      <div class="key" v-on:click="armazenarDigitos(4)">4</div>
      <div class="key" v-on:click="armazenarDigitos(5)">5</div>
      <div class="key" v-on:click="armazenarDigitos(6)">6</div>
      <div class="key" v-on:click="armazenarDigitos(7)">7</div>
      <div class="key" v-on:click="armazenarDigitos(8)">8</div>
      <div class="key" v-on:click="armazenarDigitos(9)">9</div>
      <div class="key" v-on:click="armazenarDigitos(0)">0</div>
    </div>
    <div class="apagar" v-show="!verificado" v-on:click="apagarUltDigito">Apagar</div>
  </div>
</template>

<style>
.teclado {
  display: flex;
  flex-direction: column;
}
.keyboard {
  display: grid;
  grid-template-columns: repeat(5, 85px);
  gap: 10px;
}

.key,
.apagar {
  width: 5.2vw;
  height: 10vh;
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  border: 2px solid #ccc;
  color: #201010;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.key:hover {
  background-color: #ddd;
}

.apagar {
  width: 100%;
  margin: 1vw 2vh;
}
@media (min-width: 1024px) {
  .teclado {
    min-height: 100%;
    display: flex;
    align-items: center;
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
