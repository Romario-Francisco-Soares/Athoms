<template>
  <div class="container-back">
    <h1>Minha Tabela Vue.js</h1>
    <input
      id="input"
      class="truncate"
      type="search"
      autocomplete="off"
      spellcheck="false"
      role="combobox"
      aria-controls="matches"
      aria-expanded="false"
      aria-live="polite"
      placeholder="Buscar"
      v-model="valor_busca"
      @input="filtrar"
    />
    <table border="1" cellpadding="5" cellspacing="0">
      <thead>
        <tr>
          <th v-for="campo in lsNomesCampos" :key="campo._id">
            {{ campo.nm_campo }}
          </th>
        </tr>
      </thead>
      <tbody>
      <tr v-for="(data, index) in dadosImpressao" :key="data._id?.$oid || index">
        <td v-for="campo in lsNomesCampos" :key="campo._id">
          <!-- Verifica se é uma data formatável -->
          <span v-if="isData(data[campo.nm_campo])">
            {{ formatDate(data[campo.nm_campo]?.$date || data[campo.nm_campo]) }}
          </span>
          <span v-else>
            {{ data[campo.nm_campo] }}
          </span>
        </td>
        <td>
          <button @click="editUser(index)">Editar</button>
          <button @click="deleteUser(index)">Deletar</button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      valor_busca: '',
      resultadoGet: [], // Dados carregados do banco
      dadosImpressao: [], // Dados filtrados
      lsNomesCampos: [],
    }
  },
  props:{endPontDados: String, endPointNomesCampos: String, tipo_exibicao: String},
  methods: {
    isData(valor) {
      if (!valor) return false
      if (typeof valor === 'object' && '$date' in valor) return true
      if (typeof valor === 'string') {
        const d = new Date(valor)
        return !isNaN(d)
      }
      return false
    },

    filtrar() {
      const filtro = this.valor_busca.toLowerCase().trim()

      if (!filtro) {
        this.dadosImpressao = [...this.dadosImpressao] // Restaura a lista original
        return
      }
      this.dadosImpressao = this.resultadoGet.filter((dat) => {
        return Object.values(dat).some((value) => {
          if (value && typeof value === 'string') {
            return value.toLowerCase().includes(filtro)
          }
        })
      })
    },
    async carregarDados(){
      await this.exibir_cad_prof()
      await this.listarCadastros()
    },
    async listarCadastros() {
      try {
        const response = await fetch(this.endPontDados, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',  // importante!
        })
        const data = await response.json()
        console.log(data)
        this.resultadoGet = data
        this.dadosImpressao = [...data] // Inicializa profissionais com os dados originais
      } catch (error) {
        console.error('Erro ao listar cadastros:', error)
      }
    },
    async exibir_cad_prof() {
      try {
        const response = await fetch(this.endPointNomesCampos, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body:JSON.stringify({ tipo_exibicao: this.tipo_exibicao}),
          credentials: 'include',  // importante!
        })
        const data = await response.json()
        console.log(data)
        this.lsNomesCampos = data
      } catch (error) {
        console.error('Erro ao listar cadastros:', error)
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString() // Formata a data de maneira legível
    },

    editUser(index) {
      console.log(`Editando usuário com índice ${index}`)
    },

    deleteUser(index) {
      console.log(`Deletando usuário com índice ${index}`)
    },
  },
  //mounted() {
  //  carregarDados()
  //},
}
</script>

<style scoped>
/* Seus estilos aqui */
</style>
