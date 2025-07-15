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
          <th v-for="campo in lsNomesCampos" :key="campo.nm_campo">
            {{ campo.nm_campo }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(data, index) in dadosImpressao" :key="data._id.$oid">
          <td>{{ data._id.$oid }}</td>
          <td>{{ data.nm_pessoa_fisica }}</td>
          <td>{{ formatDate(data.data_nascimento.$date) }}</td>
          <td>{{ data.ie_sexo }}</td>
          <td>{{ data.whatsapp }}</td>
          <td>{{ data.email }}</td>
          <td>{{ data.estadoCivil }}</td>
          <td>{{ data.nm_mae }}</td>
          <td>{{ data.whatsapp_mae }}</td>
          <td>{{ data.nm_pai }}</td>
          <td>{{ data.whatsapp_pai }}</td>
          <td>{{ data.cd_pis }}</td>
          <td>{{ data.cd_ctps }}</td>
          <td>{{ data.cd_eleitor }}</td>
          <td>{{ data.cpf }}</td>
          <td>{{ data.registro_geral }}</td>
          <td>{{ data.ie_qualificacao }}</td>
          <td>{{ data.endereco_natural }}</td>
          <td>{{ data.endereco_logradouro }}</td>
          <td>{{ formatDate(data.data_cadastro_original) }}</td>
          <td>{{ formatDate(data.data_contratacao) }}</td>
          <td>{{ formatDate(data.data_ult_alteracao) }}</td>
          <td>{{ data.nr_seq_prof_ult_alter }}</td>
          <td>{{ data.nr_seq_prof_cadastro }}</td>
          <td>{{ data.nr_seq_prof_contratacao }}</td>
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
  methods: {
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
        const response = await fetch('/usuario', {
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
        const response = await fetch('/exibicao', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',  // importante!
        })
        const data = await response.json()
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
