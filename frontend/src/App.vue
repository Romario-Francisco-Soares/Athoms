<script>
import TelaAcesso from './components/TelaAcesso.vue'
import MenuOpcoes from './components/MenuOpcoes.vue'
import cadastro_profissionais from './components/TemplateProfissionais.vue'
import consulta_dados from './components/reutilizaveis/consulta_dados.vue'
import registrar from './components/Registro.vue'

export default {
  components: { MenuOpcoes, consulta_dados, TelaAcesso, cadastro_profissionais, registrar },
  data() {
    return {
      autenticado: false,
      dados_perfil: [],
      subMenu: '',
      endPontDados: '/usuario',
      endPointNomesCampos: '/exibicao',
      tipo_exibicao:''
    }
  },
  methods: {
    abrirSubMenu(event){
      this.subMenu = event
      if (event === 'consulta_ponto'){
        this.tipo_exibicao = 'consulta_ponto'
      }
      if (event === 'consulta_profissional'){
        this.tipo_exibicao = 'consulta_profissional'
      }
      if (event === 'consulta_servicos'){
        this.tipo_exibicao = 'consulta_servicos'
      }
      this.$nextTick(() => {
          if (this.$refs.consulta_dados && this.$refs.consulta_dados.carregarDados()) {
              this.$refs.consulta_dados.carregarDados();
          }
          /*if (this.$refs.consulta_servicos && this.$refs.consulta_servicos.carregarDados) {
              this.$refs.consulta_servicos.carregarDados();
          }
          if (this.$refs.cadastro_turnos && this.$refs.cadastro_turnos.carregarDados) {
              this.$refs.cadastro_turnos.carregarDados();
          }
          if (this.$refs.cadastro_profissionais && this.$refs.cadastro_profissionais.carregarDados) {
              this.$refs.cadastro_profissionais.carregarDados();
          }
          if (this.$refs.registrar && this.$refs.registrar.carregarDados) {
              this.$refs.registrar.carregarDados();
          }
          if (this.$refs.configuracoes && this.$refs.configuracoes.carregarDados) {
              this.$refs.configuracoes.carregarDados();
          }*/
        });
    },
    async acessar_sistema(evento) {
      try {
        const resposta = await fetch('/listar_acessos', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',  // importante para enviar cookies
        })
        if (resposta.ok && evento) {
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
    <consulta_dados
      ref="consulta_dados"
      v-if="subMenu==='consulta_profissional' ||
            subMenu === 'consulta_ponto' ||
            subMenu=='consulta_servicos'"
      :endPontDados="endPontDados"
      :endPointNomesCampos="endPointNomesCampos"
      :tipo_exibicao="tipo_exibicao"
      >
    </consulta_dados>
    <div ref="cadastro_turnos" v-if="this.subMenu=='cadastro_turnos'">{{ this.subMenu }}</div> <!--cadastro_turnos: -->
    <cadastro_profissionais ref="cadastro_profissionais"  v-if="this.subMenu=='cadastro_profissionais'"></cadastro_profissionais>
    <registrar ref="registrar" v-if="this.subMenu=='registrar'"></registrar>
    <div ref="configuracoes" v-if="this.subMenu=='configuracoes'">{{ this.subMenu }}</div> <!--Configuracoes: -->

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
