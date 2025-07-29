<template>
  <div class="container-back">
    <UiAlert :show="showAlert" :message="alertMessage" :type="alertType" @close="showAlert = false" />
    <div class="form-wrapper">
      <h1 class="titulo">{{ titulo }}</h1>
      <form @submit.prevent="submitForm(formData)">
        <div v-for="(field, index) in formFields" :key="index" class="form-group">
          <InputField
            v-model="formData[field.model]"
            :label="field.label"
            :id="field.id"
            :name="field.name"
            :type="field.type"
            :placeholder="field.placeholder"
            :required="field.required"
            :options="field.options || []"
            :buttonClass="field.buttonClass"
            @button-click="handleButtonClick($event)"
          />
        </div>
        <div class="botoes">
          <button type="submit" class="btn btn-save">Salvar</button>
          <button type="button" class="btn btn-cancel" @click="limparCampos">Limpar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import InputField from './reutilizaveis/entrada_dados.vue'
import UiAlert from './UiAlert.vue'
export default {
  components: {
    InputField,
    UiAlert
  },
  props: {
    titulo: String,
    tipo_exibicao: String,
    endPointDados: String,
    endpointExibicao: {
      type: String,
      default: '/exibicao'
    },
  },
  data() {
    return {
      formData: {
        turno: '',
        anovalidade: '',
        mesvalidade: '',
        semanavalidade: '',
        intervaloalmoco: '',
        registroantecedencia: '',
        registroatraso: '',
        prevchegada:'',
        prevsaidaalm:'',
        prevreturnoalm:'',
        prevsaida:'',
      },
      formFields: [],
      popupOpen: false,
      stream: null,
      showAlert: false,
      alertMessage: '',
      alertType: 'info'
    }
  },
  methods: {
    limparCampos() {
      this.formData = {
        turno: '',
        anovalidade: '',
        mesvalidade: '',
        semanavalidade: '',
        intervaloalmoco: '',
        registroantecedencia: '',
        registroatraso: '',
        prevchegada:'',
        prevsaidaalm:'',
        prevreturnoalm:'',
        prevsaida:'',
      }
    },
    async cadastrar(data_cadastrar) {
      try {
        console.log('Dados a cadastrar:', data_cadastrar)
        const payload = [
          data_cadastrar,
          {acao: 'inserir'}
          ]
        const endpoint = this.endpointCadastrar || '/turnos'
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
        let data = {}
        const text = await response.text()
        if (text) {
          data = JSON.parse(text)
        }
        if (!response.ok){
          this.showUiAlert(data.error || 'Erro ao cadastrar', 'error')
          return false
        }
        this.showUiAlert(data.return_post || 'Cadastro realizado com sucesso!', 'success')
        return true
      } catch (error) {
        console.error('Erro ao cadastrar:', error)
        this.showUiAlert('Erro ao cadastrar', 'error')
        return false
      }
    },
    async atualizarTurno(turnoAlterado) {
      try {
        const payload = {
          ...turnoAlterado,
          acao: 'atualizar'
        }
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
    async exibir_cad_prof() {
      try {
        const response = await fetch(this.endpointExibicao, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ tipo_exibicao: this.tipo_exibicao }),
          credentials: 'include',
        })
        const data = await response.json()
        this.formFields = data
      } catch (error) {
        console.error('Erro ao listar cadastros:', error)
        this.showUiAlert('Erro ao listar campos', 'error')
      }
    },
    showUiAlert(msg, type = 'info') {
      this.alertMessage = msg
      this.alertType = type
      this.showAlert = true
    },
    async submitForm(data) {
      const retorno = await this.cadastrar(data)
      if (retorno){
        this.limparCampos()
      }
    },
    async carregarDados() {
      await this.exibir_cad_prof()
    },
    onMounted() {
      this.exibir_cad_prof()
    }
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
  max-width: 700px;
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.form-wrapper {
  width: 100%;
}
.titulo {
  color: var(--primary, #4f46e5);
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
}
.form-group {
  margin-bottom: 1.5rem;
}
.botoes {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}
.btn {
  padding: 0.6rem 1.4rem;
  border-radius: 6px;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}
.btn-save {
  background: var(--primary, #4f46e5);
  color: #fff;
}
.btn-cancel {
  background: #dc2626;
  color: #fff;
}
.btn-save:hover {
  background: #3730a3;
}
.btn-cancel:hover {
  background: #a31d1d;
}
@media (max-width: 700px) {
  .container-back {
    padding: 1rem;
    min-height: unset;
  }
  .form-wrapper {
    padding: 0;
  }
  .titulo {
    font-size: 1.3rem;
  }
  .btn {
    font-size: 0.95rem;
    padding: 0.5rem 1rem;
  }
}
</style>
