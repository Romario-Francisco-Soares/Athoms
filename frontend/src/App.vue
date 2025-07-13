<script>
import TelaAcesso from './components/TelaAcesso.vue'
import MenuOpcoes from './components/MenuOpcoes.vue'
import cadastro_profissionais from './components/TemplateProfissionais.vue'
import consulta_profissional from './components/ProfList.vue'
import registrar from './components/Registro.vue'

export default {
  components: { MenuOpcoes, consulta_profissional, TelaAcesso, cadastro_profissionais, registrar },
  data() {
    return {
      autenticado: false,
      dados_perfil: [],
      subMenu: '',
    }
  },
  methods: {
    abrirSubMenu(event){
      console.log(event)
      this.subMenu = event
    },
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
          this.autenticado = true;
          // Aguarde o DOM renderizar o componente <MenuOpcoes>
          this.$nextTick(() => {
            if (this.$refs.MenuOpcoes && this.$refs.MenuOpcoes.exibirMenus) {
              this.$refs.MenuOpcoes.exibirMenus();
            }
          });
        }
        else {
          const erro = await resposta.json();
          console.warn('Erro do servidor:', erro.error);
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
    <MenuOpcoes ref="MenuOpcoes" v-if="autenticado" :perfil_acessos="dados_perfil" @abrirSubMenu="abrirSubMenu($event)"></MenuOpcoes>
    <consulta_profissional v-if="this.subMenu=='consulta_profissional'"></consulta_profissional>
    <!--consulta_ponto: -->
    <!--consulta_servicos: -->
    <!--cadastro_turnos: -->
    <cadastro_profissionais v-if="this.subMenu=='cadastro_profissionais'"></cadastro_profissionais>
    <registrar v-if="this.subMenu=='registrar'"></registrar>
    <!--Configuracoes: -->
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
