<template>
  <div class="container-back">
    <div class="p-4 container">
      <UiAlert :show="showAlert" :message="alertMessage" :type="alertType" @close="showAlert = false" />

      <h1 class="titulo">{{ titulo || 'Escalas Semanais' }}</h1>
      <div class="mb-4">
        <input
          type="text"
          v-model="filtroTexto"
          @input="aplicarFiltro"
          class="input-filtro"
          placeholder="Buscar por turno, ano ou mês..."
        />
      </div>
      <div v-if="escalaFiltrada.length === 0" class="sem-dados">
        Nenhuma escala encontrada.
      </div>
      <div
        v-for="(escala, index) in escalaFiltrada"
        :key="index"
        class="mb-8 border border-gray-300 rounded-lg shadow"
      >
        <div class="flex justify-between items-center bg-gray-100 p-4 rounded-t-lg">
          <div v-if="editandoTurnoIndex === index">
            <input v-model="escala.turno" class="input-edit" />
            <input v-model="escala.ano" type="number" class="input-edit w-20" />
            <input v-model="escala.mes" type="number" class="input-edit w-20" />
          </div>
          <div v-else>
            <h2 class="text-xl font-semibold text-primary">Turno: {{ escala.turno || 'Desconhecido' }}</h2>
            <p class="text-sm text-gray-600">Ano: {{ escala.ano }} | Mês: {{ escala.mes }}</p>
          </div>

          <div class="space-x-2">
            <button
              class="btn"
              @click="toggleExpand(index)"
            >
              {{ expandedTurnos.includes(index) ? 'Ocultar Detalhes' : 'Mostrar Detalhes' }}
            </button>

            <button
              v-if="editandoTurnoIndex === index"
              class="btn btn-save"
              @click="salvarEdicaoTurno(index)"
            >
              Salvar
            </button>
            <button
              v-if="editandoTurnoIndex === index"
              class="btn btn-cancel"
              @click="cancelarEdicaoTurno()"
            >
              Cancelar
            </button>
            <button
              v-else
              class="btn btn-edit"
              @click="iniciarEdicaoTurno(index)"
            >
              Editar Info-Turno
            </button>
          </div>
        </div>

        <transition name="fade">
          <div v-if="expandedTurnos.includes(index)" class="p-4 bg-white">
            <div
              v-for="(dias, semanaKey) in getSemanas(escala)"
              :key="semanaKey"
              class="mb-6 border p-4 rounded-lg shadow-sm"
            >
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-lg font-semibold capitalize text-primary">
                  {{ semanaKey.replace('_', ' ') }}
                </h3>
                <div class="space-x-2">
                  <button
                    v-if="isEditandoSemana(index, semanaKey)"
                    class="text-sm text-green-600 hover:underline"
                    @click="salvarEdicaoSemana(index, semanaKey)"
                  >
                    Salvar
                  </button>
                  <button
                    class="text-sm text-indigo-600 hover:underline"
                    @click="toggleEdicaoSemana(index, semanaKey)"
                  >
                    {{ isEditandoSemana(index, semanaKey) ? 'Cancelar' : 'Editar Semana' }}
                  </button>
                </div>
              </div>


              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-gray-200 text-sm">
                    <th class="p-2">Dia</th>
                    <th class="p-2">Chegada</th>
                    <th class="p-2">Saída Almoço</th>
                    <th class="p-2">Retorno Almoço</th>
                    <th class="p-2">Saída</th>
                    <th class="p-2">Intervalo</th>
                    <th class="p-2">Tol. Antes</th>
                    <th class="p-2">Tol. Atraso</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(diaObj, idx) in dias"
                    :key="idx"
                    class="hover:bg-gray-50 text-sm border-t"
                  >
                    <td class="p-2 font-medium capitalize">
                      {{ Object.keys(diaObj)[0] }}
                    </td>

                    <td class="p-2">
                      <input
                        v-if="isEditandoSemana(index, semanaKey)"
                        v-model="diaObj[Object.keys(diaObj)[0]].prev_hr_chegada"
                        class="input-edit w-full"
                      />
                      <span v-else>{{ formatDate(diaObj[Object.keys(diaObj)[0]].prev_hr_chegada) }}</span>
                    </td>

                    <td class="p-2">
                      <input
                        v-if="isEditandoSemana(index, semanaKey)"
                        v-model="diaObj[Object.keys(diaObj)[0]].prev_hr_saida_alm"
                        class="input-edit w-full"
                      />
                      <span v-else>{{ formatDate(diaObj[Object.keys(diaObj)[0]].prev_hr_saida_alm) }}</span>
                    </td>

                    <td class="p-2">
                      <input
                        v-if="isEditandoSemana(index, semanaKey)"
                        v-model="diaObj[Object.keys(diaObj)[0]].prev_hr_ret_alm"
                        class="input-edit w-full"
                      />
                      <span v-else>{{ formatDate(diaObj[Object.keys(diaObj)[0]].prev_hr_ret_alm) }}</span>
                    </td>

                    <td class="p-2">
                      <input
                        v-if="isEditandoSemana(index, semanaKey)"
                        v-model="diaObj[Object.keys(diaObj)[0]].prev_hr_saida"
                        class="input-edit w-full"
                      />
                      <span v-else>{{ formatDate(diaObj[Object.keys(diaObj)[0]].prev_hr_saida) }}</span>
                    </td>

                    <td class="p-2">
                      <input
                        v-if="isEditandoSemana(index, semanaKey)"
                        v-model="diaObj[Object.keys(diaObj)[0]].min_intervalo"
                        class="input-edit w-full"
                      />
                      <span v-else>{{ diaObj[Object.keys(diaObj)[0]].min_intervalo }}</span>
                    </td>

                    <td class="p-2">
                      <input
                        v-if="isEditandoSemana(index, semanaKey)"
                        v-model="diaObj[Object.keys(diaObj)[0]].min_tolerancia_anteced"
                        class="input-edit w-full"
                      />
                      <span v-else>{{ diaObj[Object.keys(diaObj)[0]].min_tolerancia_anteced }}</span>
                    </td>

                    <td class="p-2">
                      <input
                        v-if="isEditandoSemana(index, semanaKey)"
                        v-model="diaObj[Object.keys(diaObj)[0]].min_tolerancia_atraso"
                        class="input-edit w-full"
                      />
                      <span v-else>{{ diaObj[Object.keys(diaObj)[0]].min_tolerancia_atraso }}</span>
                    </td>
                  </tr>
                </tbody>

              </table>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import UiAlert from './UiAlert.vue'
export default {
  name: 'EscalaSemanal',
  components: { UiAlert },
  props: {
    endPointDados: String,
    endPointNomesCampos: String,
    tipo_exibicao: String,
    titulo: String,
  },
  data() {
    return {
      escalaData: [],
      escalaFiltrada: [],
      expandedTurnos: [],
      editandoTurnoIndex: null,
      editandoSemana: {},
      backupSemanas: {},
      filtroTexto: '',
      showAlert: false,
      alertMessage: '',
      alertType: 'info'
    }
  },
  methods: {
    async atualizarTurno(turnoAlterado) {
      console.log('Atualizando turno:', turnoAlterado)
      try {
        const payload = [
          turnoAlterado,
          {
           _id: turnoAlterado._id,
          acao: 'atualizar'
          }]
        const response = await fetch('/turnos', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          credentials: 'include'
        })
        const data = await response.json()
        if (!response.ok) {
          this.showUiAlert(data.error || 'Erro ao atualizar turno', 'error')
          return false
        }
        this.showUiAlert(data.return_post || 'Turno atualizado com sucesso!', 'success')
        return true
      } catch (error) {
        console.error('Erro ao atualizar turno:', error)
        this.showUiAlert('Erro ao atualizar turno', 'error')
        return false
      }
    },
    showUiAlert(msg, type = 'info') {
      this.alertMessage = msg
      this.alertType = type
      this.showAlert = true
    },
    salvarEdicaoSemana(index, semanaKey) {
      console.log('Salvando semana:', semanaKey, 'do turno:', this.escalaData[index])
      const semanas = this.editandoSemana[index] // Remove o modo edição
      if (semanas) {
        const pos = semanas.indexOf(semanaKey)
        if (pos > -1) semanas.splice(pos, 1)
      }
      if (this.backupSemanas[index]) {// Limpa o backup
        delete this.backupSemanas[index][semanaKey]
        if (Object.keys(this.backupSemanas[index]).length === 0) {
          delete this.backupSemanas[index]
        }
      }
      this.atualizarTurno(this.escalaData[index])// Emitir um evento ou atualizar no backend aqui
    },
    aplicarFiltro() {
    const texto = this.filtroTexto.toLowerCase().trim()
    if (!texto) {
      this.escalaFiltrada = [...this.escalaData]
      return
    }
    this.escalaFiltrada = this.escalaData.filter((escala) => {
      return (
        (escala.turno && escala.turno.toLowerCase().includes(texto)) ||
        String(escala.ano).includes(texto) ||
        String(escala.mes).includes(texto)
      )
    })
  },
  async listarCadastros() {
    try {
      const response = await fetch(this.endPointDados, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
      })
      const data = await response.json()
      this.showUiAlert('Dados carregados com sucesso!', 'success')
      if (!response.ok) {
        this.showUiAlert(data.error || 'Erro ao listar cadastros', 'error')
        return
      }
      this.escalaData = [...data]
      this.escalaFiltrada = [...data]
    } catch (error) {
      this.showUiAlert('Erro ao listar cadastros:', error)
    }
  },
    toggleExpand(index) {
      if (this.expandedTurnos.includes(index)) {
        this.expandedTurnos = this.expandedTurnos.filter(i => i !== index)
      } else {
        this.expandedTurnos.push(index)
      }
    },
    getSemanas(escala) {
      const semanas = {}
      for (const [key, value] of Object.entries(escala)) {
        if (key.startsWith('semana_')) {
          semanas[key] = value
        }
      }
      return semanas
    },
    toggleEdicaoSemana(index, semanaKey) {
      if (!this.editandoSemana[index]) this.editandoSemana[index] = []

      const semanas = this.editandoSemana[index]
      const pos = semanas.indexOf(semanaKey)

      if (pos > -1) {
        // Se já está em edição e vai cancelar => restaura os dados do backup
        if (this.backupSemanas[index]?.[semanaKey]) {
          this.escalaData[index][semanaKey] = JSON.parse(
            JSON.stringify(this.backupSemanas[index][semanaKey])
          )
        }

        semanas.splice(pos, 1)
      } else {
        // Se vai começar a editar, cria backup
        if (!this.backupSemanas[index]) this.backupSemanas[index] = {}
        this.backupSemanas[index][semanaKey] = JSON.parse(
          JSON.stringify(this.escalaData[index][semanaKey])
        )

        semanas.push(semanaKey)
      }
    },
    isEditandoSemana(index, semanaKey) {
      return this.editandoSemana[index]?.includes(semanaKey)
    },
    iniciarEdicaoTurno(index) {
      this.editandoTurnoIndex = index
    },
    salvarEdicaoTurno(index) {
      this.atualizarTurno(this.escalaData[index])
      this.editandoTurnoIndex = null
      // Aqui você pode implementar chamada à API
      console.log('Salvou edição do turno', this.escalaData[index])
    },
    cancelarEdicaoTurno() {
      this.editandoTurnoIndex = null
      // Idealmente aqui você recarregaria os dados originais do servidor
    },
    formatDate(data) {
      if (!data) return ''
      const d = new Date(data)
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    },
    async carregarDados() {
      await this.listarCadastros()
      console.log(this.escalaFiltrada)
    },
  },
  mounted() {
    this.carregarDados()
  },
}
</script>

<style scoped>
:root {
  --primary: #4f46e5;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-700: #374151;
  --gray-900: #111827;
}
h3{
  margin: 3rem 0rem 1rem 1rem;
  font-size: 1.2rem;
}
.mb-8{
  box-shadow: 0 2px 8px rgba(0, 53, 28, 0.199);
  padding: 2%;
  border-radius: 10px;
}
.container-back {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 2rem;
  margin: 2rem auto;
  max-width: 1100px;
  min-width: 80vw;
}
.titulo {
  color: var(--primary, #4f46e5);
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-align: center;
}

.sem-dados {
  text-align: center;
  color: #888;
  margin: 2rem 0 1rem 0;
  font-size: 1.1rem;
}

.text-primary {
  color: var(--primary);
}

.bg-primary {
  background-color: var(--primary);
}

button {
  cursor: pointer;
}

.container {
  max-width: 100%;
  margin: 0 auto;
}

/* Transição suave */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

h1 {
  color: var(--gray-900);
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 1rem;
  text-transform: capitalize;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

thead {
  background-color: var(--gray-100);
}

th {
  padding: 0.75rem;
  text-align: left;
  font-size: 0.875rem;
  color: var(--gray-700);
  font-weight: 600;
  border-bottom: 1px solid var(--gray-200);
}

td {
  padding: 0.75rem;
  font-size: 0.875rem;
  color: var(--gray-900);
  border-bottom: 1px solid var(--gray-100);
}

tbody tr:hover {
  background-color: var(--gray-50);
  transition: background-color 0.2s ease;
}

.input-edit {
  border: 1px solid var(--gray-200);
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 0.875rem;
  margin-right: 0.25rem;
  color: var(--gray-900);
}

.btn {
  background-color: var(--gray-200);
  color: var(--gray-700);
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.btn-edit {
  background-color: var(--primary);
  color: rgb(3, 71, 20);
}

.btn-save {
  background-color: #059669; /* green-600 */
  color: white;
}

.btn-cancel {
  background-color: #dc2626; /* red-600 */
  color: white;
}

@media (max-width: 768px) {
  table,
  thead,
  tbody,
  th,
  td,
  tr {
    display: block;
  }

  thead {
    display: none;
  }

  tr {
    margin-bottom: 1rem;
    border: 1px solid var(--gray-200);
    border-radius: 0.5rem;
    padding: 1rem;
    background-color: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }

  td {
    border-bottom: none;
    padding: 0.5rem 0;
    position: relative;
  }

  td::before {
    content: attr(data-label);
    font-weight: 600;
    text-transform: capitalize;
    display: block;
    margin-bottom: 0.25rem;
    color: var(--gray-700);
  }
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
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
}

@media (max-width: 700px) {
  .container-back {
    padding: 1rem;
  }
  .container {
    padding: 1rem;
  }
  table,
  thead,
  tbody,
  th,
  td,
  tr {
    font-size: 0.95rem;
  }
}
</style>
