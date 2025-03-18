<script>
import TelaAcesso from './components/TelaAcesso.vue'
import MenuOpcoes from './components/MenuOpcoes.vue'
import Profissionais from './components/TemplateProfissionais.vue'
import ProfList from './components/ProfList.vue'

export default {
  components: { MenuOpcoes, ProfList, TelaAcesso, Profissionais },
  data() {
    return {
      autenticado: false,
      a: false,
    }
  },
}
</script>

<template>
  <TelaAcesso v-if="!autenticado"></TelaAcesso>
  <MenuOpcoes v-if="autenticado"></MenuOpcoes>
  <ProfList v-if="autenticado"></ProfList>
  <Profissionais v-if="autenticado"></Profissionais>
</template>

<style scoped></style>
