<script>
import TelaAcesso from './components/TelaAcesso.vue'
import MenuOpcoes from './components/MenuOpcoes.vue'
import Profissionais from './components/TemplateProfissionais.vue'
import ProfList from './components/ProfList.vue'
import Registro from './components/Registro.vue'

export default {
  components: { MenuOpcoes, ProfList, TelaAcesso, Profissionais, Registro },
  data() {
    return {
      autenticado: false,
      dados_perfil: [],
      a:false,
      b:false,
      c:false
    }
  },
  methods: {
    async acessar_sistema(evento) {
      console.log(evento)
      try {
        const resposta = await fetch('/listar_acessos', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',  // importante para enviar cookies
        })

        if (resposta.ok) {
          const data = await resposta.json();
          this.dados_perfil = data.dados_perfil;
          this.autenticado = true
        } else {
          const erro = await resposta.json();
          console.warn('Erro do servidor:', erro);
          alert(erro.error || 'Erro ao acessar sistema.');
        }
      } catch (erro) {
        console.error('Erro de rede:', erro)
        alert('Falha na busca de acessos.')
      }
    }

  }
}
</script>

<template>
  <div class="PlanoFundo">
    <TelaAcesso v-if="!autenticado" @autorizado_login="acessar_sistema($event)"></TelaAcesso>
    <MenuOpcoes v-if="autenticado" :perfil_acessos="dados_perfil"></MenuOpcoes>
    <ProfList v-if="a"></ProfList>
    <Profissionais v-if="b"></Profissionais>
    <Registro v-if="c"></Registro>
  </div>
</template>

<style>
.PlanoFundo {

}
button {
  background-color: #8cf393;
  border: 2px solid #37813c;
  transition: background-color 0.2s;
  cursor: pointer;
}
button:hover {
  background-color: #3af147;
}
</style>
