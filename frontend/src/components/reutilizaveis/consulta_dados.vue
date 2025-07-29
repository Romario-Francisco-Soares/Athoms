<template>
  <div class="container-back">
    <UiAlert :show="showAlert" :message="alertMessage" :type="alertType" @close="showAlert = false" />
    <h1 class="titulo">{{ titulo }}</h1>
    <input
      id="input"
      class="truncate input-filtro"
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
    <div class="tabela-wrapper">
      <table class="tabela-dados">
        <thead>
          <tr>
            <th v-for="campo in lsNomesCampos" :key="campo._id">
              {{ campo.nm_campo }}
            </th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) in dadosImpressao" :key="data._id?.$oid || index">
            <td v-for="campo in lsNomesCampos" :key="campo._id">
              <template v-if="editandoIndex === index">
                <input
                  v-model="editBuffer[campo.nm_campo]"
                  class="input-edit"
                  :placeholder="campo.nm_campo"
                />
              </template>
              <template v-else>
                <span v-if="isData(data[campo.nm_campo])">
                  {{ formatDate(data[campo.nm_campo]?.$date || data[campo.nm_campo]) }}
                </span>
                <span v-else>
                  {{ data[campo.nm_campo] ?? '-' }}
                </span>
              </template>
            </td>
            <td>
              <template v-if="editandoIndex === index">
                <button class="btn btn-save" @click="salvarEdicao(index)">Salvar</button>
                <button class="btn btn-cancel" @click="cancelarEdicao(index)">Cancelar</button>
              </template>
              <template v-else>
                <button class="btn btn-edit" @click="iniciarEdicao(index)">Editar</button>
                <button class="btn btn-delete" @click="deleteUser(index)">Deletar</button>
              </template>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="dadosImpressao.length === 0" class="sem-dados">
        Nenhum dado encontrado.
      </div>
    </div>
  </div>
</template>

<script>
import UiAlert from '../UiAlert.vue'
export default {
  components: { UiAlert },
  data() {
    return {
      valor_busca: '',
      resultadoGet: [],
      dadosImpressao: [],
      lsNomesCampos: [],
      showAlert: false,
      alertMessage: '',
      alertType: 'info',
      editandoIndex: null,
      editBuffer: {},
      backupBuffer: {},
    }
  },
  props: {
    endPointDados: String,
    endPointNomesCampos: String,
    tipo_exibicao: String,
    titulo: String,
  },
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
        this.dadosImpressao = [...this.resultadoGet]
        return
      }
      this.dadosImpressao = this.resultadoGet.filter((dat) => {
        return Object.values(dat).some((value) => {
          if (value == null) return false
          if (typeof value === 'object' && '$date' in value) {
            return String(value.$date).toLowerCase().includes(filtro)
          }
          return String(value).toLowerCase().includes(filtro)
        })
      })
    },
    async carregarDados() {
      await this.exibir_cad_prof()
      await this.listarCadastros()
    },
    async listarCadastros() {
      try {
        const response = await fetch(this.endPointDados, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
        })
        const data = await response.json()
        this.resultadoGet = data
        this.dadosImpressao = [...data]
        this.showUiAlert('Dados carregados com sucesso!', 'success')
      } catch (error) {
        console.error('Erro ao listar cadastros:', error)
        this.showUiAlert('Erro ao listar cadastros', 'error')
      }
    },
    async exibir_cad_prof() {
      try {
        const response = await fetch(this.endPointNomesCampos, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ tipo_exibicao: this.tipo_exibicao }),
          credentials: 'include',
        })
        const data = await response.json()
        this.lsNomesCampos = data
      } catch (error) {
        console.error('Erro ao listar cadastros:', error)
        this.showUiAlert('Erro ao listar campos', 'error')
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return isNaN(date) ? '-' : date.toLocaleDateString()
    },
    iniciarEdicao(index) {
      this.editandoIndex = index
      // Cria um buffer com os dados atuais para edição
      this.editBuffer = { ...this.dadosImpressao[index] }
      // Backup para restaurar se cancelar
      this.backupBuffer = { ...this.dadosImpressao[index] }
    },
    cancelarEdicao(index) {
      // Restaura os dados originais
      this.dadosImpressao[index] = { ...this.backupBuffer }
      this.editandoIndex = null
      this.editBuffer = {}
      this.backupBuffer = {}
    },
    async salvarEdicao(index) {
      const usuarioEditado = { ...this.editBuffer }
      try {
        const response = await fetch(this.endPointDados, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify([
            usuarioEditado,
            {
            acao: 'atualizar',
            _id: usuarioEditado._id
          }]),
          credentials: 'include'
        })
        const data = await response.json()
        if (!response.ok) {
          this.showUiAlert(data.error || 'Erro ao atualizar usuário', 'error')
          return
        }
        this.dadosImpressao[index] = { ...usuarioEditado }
        this.showUiAlert(data.return_post || 'Usuário atualizado com sucesso!', 'success')
        this.editandoIndex = null
        this.editBuffer = {}
        this.backupBuffer = {}
      } catch (error) {
        console.error('Erro ao atualizar usuário:', error)
        this.showUiAlert('Erro ao atualizar usuário', 'error')
      }
    },
    async deleteUser(index) {
      const usuario = this.dadosImpressao[index]
      if (!confirm('Tem certeza que deseja deletar este usuário?')) return
      try {
        const response = await fetch(this.endPointDados, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify([
            ...usuario,
            {
            _id: usuario._id,
            acao: 'deletar'
          }]),
          credentials: 'include'
        })
        const data = await response.json()
        if (!response.ok) {
          this.showUiAlert(data.error || 'Erro ao deletar usuário', 'error')
          return
        }
        this.dadosImpressao.splice(index, 1)
        this.resultadoGet = this.resultadoGet.filter(u => u._id !== usuario._id)
        this.showUiAlert(data.return_post || 'Usuário deletado com sucesso!', 'success')
      } catch (error) {
        console.error('Erro ao deletar usuário:', error)
        this.showUiAlert('Erro ao deletar usuário', 'error')
      }
    },
    showUiAlert(msg, type = 'info') {
      this.alertMessage = msg
      this.alertType = type
      this.showAlert = true
    },
  },
  mounted() {
    this.carregarDados()
  },
}
</script>

<style scoped>
.container-back {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 2rem;
  margin: 2rem auto;
  max-width: 1100px;
}
.titulo {
  color: var(--primary, #4f46e5);
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-align: center;
}
.input-filtro {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  font-size: 1rem;
  border: 1px solid var(--gray-200, #e5e7eb);
  background-color: var(--gray-50, #f9fafb);
  color: var(--gray-900, #111827);
  margin-bottom: 1.5rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  transition: border 0.2s, box-shadow 0.2s;
}
.input-filtro:focus {
  outline: none;
  border-color: var(--primary, #4f46e5);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
}
.tabela-wrapper {
  overflow-x: auto;
}
.tabela-dados {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}
.tabela-dados th, .tabela-dados td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--gray-100, #f3f4f6);
  text-align: left;
}
.tabela-dados th {
  background: var(--gray-100, #f3f4f6);
  color: var(--gray-700, #374151);
  font-weight: 600;
}
.tabela-dados tr:last-child td {
  border-bottom: none;
}
.btn {
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-size: 0.95rem;
  border: none;
  margin-right: 0.3rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-edit {
  background: var(--primary, #4f46e5);
  color: #fff;
}
.btn-delete {
  background: #dc2626;
  color: #fff;
}
.btn-edit:hover, .btn-delete:hover {
  opacity: 0.85;
}
.sem-dados {
  text-align: center;
  color: #888;
  margin: 2rem 0 1rem 0;
  font-size: 1.1rem;
}
.input-edit {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--gray-300, #d1d5db);
  border-radius: 4px;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
  transition: border-color 0.2s;
}
.input-edit:focus {
  outline: none;
  border-color: var(--primary, #4f46e5);
}
.btn-save {
  background: #4caf50;
  color: #fff;
}
.btn-cancel {
  background: #f44336;
  color: #fff;
}
.btn-save:hover {
  background: #45a049;
}
.btn-cancel:hover {
  background: #e53935;
}
@media (max-width: 700px) {
  .container-back {
    padding: 1rem;
  }
  .tabela-dados th, .tabela-dados td {
    padding: 0.5rem 0.4rem;
    font-size: 0.95rem;
  }
}
</style>
