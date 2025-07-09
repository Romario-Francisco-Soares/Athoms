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
      a: false,
    }
  },
}
</script>

<template>
  <div class="PlanoFundo">
    <TelaAcesso v-if="autenticado"></TelaAcesso>
    <MenuOpcoes v-if="autenticado"></MenuOpcoes>
    <ProfList v-if="autenticado"></ProfList>
    <Profissionais v-if="autenticado"></Profissionais>
    <Registro v-if="!autenticado"></Registro>
  </div>
</template>

<style>
.PlanoFundo {
  background: linear-gradient(90deg, #8cf393, #6fdc7f, #4fc46a, #3aad5a);
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
