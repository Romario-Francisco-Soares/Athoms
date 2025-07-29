<script>
import TelaAcesso from './components/TelaAcesso.vue'
import MenuOpcoes from './components/MenuOpcoes.vue'
import CadastroProfissionais from './components/TemplateProfissionais.vue'
import CadastroTurnos from './components/cadastro_turnos.vue'
import ConsultaDados from './components/reutilizaveis/consulta_dados.vue'
import Registrar from './components/Registro.vue'
import PaginaEmpresarial from './components/PaginaEmpresarial/PaginaEmpresarial.vue'
import EscalaSemanal from './components/EscalaSemanal.vue'

export default {
  name: 'App',
  components: {
    MenuOpcoes,
    ConsultaDados,
    TelaAcesso,
    CadastroProfissionais,
    Registrar,
    PaginaEmpresarial,
    CadastroTurnos,
    EscalaSemanal
  },
  data() {
    return {
      autenticado: false,
      dados_perfil: [],
      subMenu: '',
      endPointEnviaDados: '',
      endPointBuscaDados: '',
      endPointBuscaNomesCampos: '',
      tipo_exibicao: '',
      titulo_sub_menu: ''
    }
  },
  methods: {
    redefinirEntradasMenus(tipo_exibicao, titulo_sub_menu, endPointBuscaNomesCampos, endPointBuscaDados, endPointEnviaDados) {
      this.tipo_exibicao = tipo_exibicao
      this.titulo_sub_menu = titulo_sub_menu
      this.endPointBuscaNomesCampos = endPointBuscaNomesCampos
      this.endPointBuscaDados = endPointBuscaDados
      this.endPointEnviaDados = endPointEnviaDados
    },
    abrirSubMenu(event) {
      this.subMenu = event
      const menuConfig = {
        consulta_ponto:    ['consulta_ponto', 'Consulta de Ponto', '/exibicao', '/registro_ponto', ''],
        consulta_profissional: ['consulta_profissional', 'Consulta de Profissionais', '/exibicao', '/usuario', ''],
        consulta_turno:    ['consulta_turno', 'Consulta de Turnos', '/exibicao', '/turnos', ''],
        consulta_servicos: ['consulta_servicos', 'Consulta de Serviços', '', '', ''],
        cadastro_turnos:   ['cadastro_turnos', 'Cadastrar Turnos', '/exibicao', '/turnos', '/turnos']
      }
      if (menuConfig[event]) {
        this.redefinirEntradasMenus(...menuConfig[event])
      }
      this.$nextTick(() => {
        if (this.$refs.consulta_dados?.carregarDados) {
          this.$refs.consulta_dados.carregarDados()
        }
        if (this.$refs.escala_semanal?.carregarDados) {
          this.$refs.escala_semanal.carregarDados()
        }
        if (this.$refs.cadastro_turnos?.carregarDados) {
          this.$refs.cadastro_turnos.carregarDados()
        }
      })
    },
    async acessar_sistema(evento) {
      try {
        const resposta = await fetch('/listar_acessos', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        })
        if (resposta.ok && evento) {
          const data = await resposta.json()
          this.dados_perfil = data.dados_perfil
          this.autenticado = true
          this.$nextTick(() => {
            this.$refs.MenuOpcoes?.exibirMenus?.()
          })
        } else {
          const erro = await resposta.json()
          console.warn('Erro do servidor:', erro.error)
          alert(erro.error || 'Erro ao acessar sistema.')
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
    <PaginaEmpresarial v-if="false" />
    <TelaAcesso v-if="!autenticado" @autorizado_login="acessar_sistema($event)" />
    <MenuOpcoes
      ref="MenuOpcoes"
      v-if="autenticado"
      :perfil_acessos="dados_perfil"
      @abrirSubMenu="abrirSubMenu"
    />
    <ConsultaDados
      ref="consulta_dados"
      v-if="['consulta_profissional', 'consulta_ponto', 'consulta_servicos'].includes(subMenu)"
      :endPointDados="endPointBuscaDados"
      :endPointNomesCampos="endPointBuscaNomesCampos"
      :tipo_exibicao="tipo_exibicao"
      :titulo="titulo_sub_menu"
    />
    <EscalaSemanal
      ref="escala_semanal"
      v-if="subMenu === 'consulta_turno'"
      :endPointDados="endPointBuscaDados"
      :endPointNomesCampos="endPointBuscaNomesCampos"
      :tipo_exibicao="tipo_exibicao"
      :titulo="titulo_sub_menu"
    />
    <CadastroTurnos
      ref="cadastro_turnos"
      v-if="subMenu === 'cadastro_turnos'"
      :endPointDados="endPointEnviaDados"
      :endPointNomesCampos="endPointBuscaNomesCampos"
      :tipo_exibicao="tipo_exibicao"
      :titulo="titulo_sub_menu"
    />
    <CadastroProfissionais ref="cadastro_profissionais" v-if="subMenu === 'cadastro_profissionais'" />
    <Registrar ref="registrar" v-if="subMenu === 'registrar'" />
    <div ref="configuracoes" v-if="subMenu === 'configuracoes'">{{ subMenu }}</div>
  </div>
</template>

<style>
.PlanoFundo {
  min-height: 100vh;
  background: linear-gradient(135deg, #f3f4f6 0%, #e0e7ff 100%);
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: flex-start;
  padding-bottom: 2rem;
}
button {
  background-color: #4f46e5;
  border: none;
  color: #fff;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  transition: background 0.2s;
  cursor: pointer;
}
button:hover {
  background-color: #3730a3;
}
</style>
