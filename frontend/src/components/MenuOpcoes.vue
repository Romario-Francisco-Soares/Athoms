<script>
  export default{
    data(){
      return{
        nm_perfil:false,
        turn:false,
        serv:false,
        regis:false,
        reg:false,
        conf:false,
        prof:false,
        cadprof: false,
        cadturn: false,
        nr_seq_empresa: false
      }
    },
    props:{perfil_acessos: Object},
    methods:{
      emitirAcessoSubMenu(event){
        this.$emit('abrirSubMenu', event)
      },
      exibirMenus(){
        if (this.perfil_acessos) {
          this.nm_perfil = this.perfil_acessos.nm_perfil,
          this.prof = this.perfil_acessos.consulta_profissional
          this.reg = this.perfil_acessos.consulta_ponto,
          this.serv = this.perfil_acessos.consulta_servicos,
          this.turn = this.perfil_acessos.consulta_turnos,
          this.cadturn = this.perfil_acessos.cadastro_turnos,
          this.cadprof = this.perfil_acessos.cadastro_profissionais
          this.regis = this.perfil_acessos.registrar,
          this.conf = this.perfil_acessos.configuracoes,
          this.nr_seq_empresa = this.perfil_acessos.nr_seq_empresa
        }
      }
    },
    watch:{
      perfil_acessos(novoValor){
        console.log('novoValor', novoValor)
        console.log('perfil', this.perfil_acessos)
      }
    }
  }
</script>
<template>
  <link href="https://fonts.googleapis.com/css2?family=Lato&display=swap" rel="stylesheet" />
  <link href="https://use.fontawesome.com/releases/v5.6.1/css/all.css" rel="stylesheet" />

  <input type="checkbox" id="check" />

  <label for="check">
    <i class="fas fa-bars" id="btn">Menu</i>
    <i class="fas fa-times" id="cancel">Fechar</i>
  </label>

  <div class="sidebar">
    <header>Menu</header>

    <a class="link-sidebar active" v-if="prof" @click="emitirAcessoSubMenu('consulta_profissional')">
      <i class="fas fa-qrcode"></i>
      <span>Consulta Profissional</span>
    </a>

    <a class="link-sidebar"  v-if="reg" @click="emitirAcessoSubMenu('consulta_ponto')">
      <i class="fas fa-link"></i>
      <span>Consulta Registro</span>
    </a>

    <a class="link-sidebar"  v-if="reg" @click="emitirAcessoSubMenu('consulta_turno')">
      <i class="fas fa-link"></i>
      <span>Consulta Turno</span>
    </a>

    <a class="link-sidebar"  v-if="serv" @click="emitirAcessoSubMenu('consulta_servicos')">
      <i class="fas fa-sliders-h"></i>
      <span>Consulta Serviços</span>
    </a>

    <a class="link-sidebar active" v-if="cadprof" @click="emitirAcessoSubMenu('cadastro_profissionais')">
      <i class="fas fa-qrcode"></i>
      <span>Cadastro Profissional</span>
    </a>

    <a class="link-sidebar"  v-if="regis" @click="emitirAcessoSubMenu('registrar')">
      <i class="far fa-question-circle"></i>
      <span>Registrar</span>
    </a>

    <a class="link-sidebar" v-if="turn" @click="emitirAcessoSubMenu('cadastro_turnos')">
      <i class="fas fa-edit"></i>
      <span>Cadastro Turno</span>
    </a>

    <a href="confg06" class="link-sidebar"  v-if="conf" @click="emitirAcessoSubMenu('configuracoes')">
      <i class="far fa-envelope"></i>
      <span>Configurações</span>
    </a>
  </div>
</template>

<style scoped>
:root {
  --accent-color: #fff;
  --gradient-color: #fbfbfb;
}

.sidebar {
  position: fixed;
  z-index: 999;
  width: 340px;
  left: -340px;
  height: 100%;
  background-color: #202020;
  transition: all 0.5s ease;
  box-shadow: 2px 0 8px rgba(0,0,0,0.08);
}

.sidebar header {
  font-size: 28px;
  color: #ffffff;
  line-height: 70px;
  text-align: center;
  background-color: #202020;
  user-select: none;
  font-family: 'Lato', sans-serif;
  letter-spacing: 2px;
}

.sidebar .link-sidebar {
  display: block;
  height: 65px;
  width: 100%;
  color: #ffffff;
  line-height: 65px;
  padding-left: 30px;
  box-sizing: border-box;
  border-left: 5px solid transparent;
  font-family: 'Lato', sans-serif;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
  font-size: 1.1rem;
}

.link-sidebar.active,
.link-sidebar:hover {
  background: linear-gradient(to left, #32d7fd, #006bdc);
  color: #fff;
  border-left: 5px solid #32d7fd;
}

.sidebar .link-sidebar i {
  font-size: 23px;
  margin-right: 16px;
}

.sidebar .link-sidebar span {
  letter-spacing: 1px;
  text-transform: uppercase;
}

#check {
  display: none;
}

label #btn,
label #cancel {
  position: fixed;
  z-index: 999;
  left: 5px;
  cursor: pointer;
  color: #ffffff;
  border-radius: 50px;
  margin: 15px 30px;
  margin-left: 30px;
  font-size: 22px;
  background-color: #202020;
  height: 45px;
  width: 7vw;
  text-align: center;
  line-height: 44px;
  transition: all 0.5s ease;
}

label #cancel {
  opacity: 0;
  visibility: hidden;
}

#check:checked ~ .sidebar {
  left: 0;
}

#check:checked ~ label #btn {
  margin-left: 345px;
  opacity: 0;
  visibility: hidden;
}

#check:checked ~ label #cancel {
  margin-left: 345px;
  opacity: 1;
  visibility: visible;
}

@media (max-width: 860px) {
  .sidebar {
    height: auto;
    width: 70px;
    left: 0;
    margin: 100px 0;
  }

  header,
  #btn,
  #cancel {
    display: none;
  }

  span {
    position: absolute;
    margin-left: 23px;
    opacity: 0;
    visibility: hidden;
  }

  .sidebar .link-sidebar {
    height: 60px;
  }

  .sidebar .link-sidebar i {
    margin-left: -10px;
  }

  .link-sidebar:hover {
    width: 200px;
    background: inherit;
  }

  .sidebar .link-sidebar:hover span {
    opacity: 1;
    visibility: visible;
  }
}

.sidebar > .link-sidebar.active,
.sidebar > .link-sidebar:hover {
  --accent-color: #32d7fd;
  --gradient-color: #006bdc;
}
</style>
