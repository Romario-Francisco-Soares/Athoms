<template>
  <div class="container-back">
    <div class="container-form">
      <div class="out">
        <h1>Novo Profissional</h1>
        <form @submit.prevent="submitForm">
          <div v-for="(field, index) in formFields" :key="index" class="form-group">
            <!--<label :for="field.id" class="form-label">{{ field.label }}</label>-->
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

          <div v-if="popupOpen" class="popup-overlay">
            <div class="popup-content">
              <h2>Capturar Foto</h2>
              <video ref="video" id="video" autoplay></video>
              <canvas ref="canvas" id="canvas" style="display: none"></canvas>
              <button type="button" @click="capturePhoto" id="capture">Capturar</button>
              <button type="button" @click="uploadImage" id="upload">Upload Foto</button>
              <button type="button" @click="closePopup">Fechar</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import InputField from './InputField.vue' // Componente reutilizável de input

export default {
  components: {
    InputField,
  },
  data() {
    return {
      formData: {
        nome: '',
        dataNascimento: '',
        sexo: '',
        whatsapp: '',
        email: '',
        estadoCivil: '',
        nm_mae: '',
        whatsapp_mae: '',
        nm_pai: '',
        whatsapp_pai: '',
        cd_pis: '',
        cd_ctps: '',
        cd_eleitor: '',
        cd_cpf: '',
        cd_rg: '',
        ie_qualificacao: '',
        endereco_natural: '',
        endereco_logradouro: '',
        matrix_face: '',
        matrix_digi: '',
        matrix_retina: '',
        matrix_senh: '',
        data_cadastro_original: '',
        data_contratacao: '',
        data_ult_alteracao: '',
        nr_seq_prof_ult_alter: '',
        nr_seq_prof_cadastro: '',
        nr_seq_prof_contratacao: '',
      },
      formFields: [
        {
          label: 'Nome',
          model: 'nome',
          id: 'nome',
          type: 'text',
          placeholder: 'Nome',
          required: true,
        },
        {
          label: 'Data de Nascimento',
          model: 'dataNascimento',
          id: 'datanascimento',
          type: 'date',
          required: true,
        },
        {
          label: 'Sexo biológico',
          model: 'sexo',
          id: 'sexo',
          component: 'input-radio',
          type: 'radio',
          required: true,
          options: ['Masculino', 'Feminino'],
        },
        {
          label: 'Whatsapp',
          model: 'whatsapp',
          id: 'whatsapp',
          type: 'text',
          placeholder: '(31)99989-0000',
          required: true,
        },
        {
          label: 'E-mail',
          model: 'email',
          id: 'email',
          type: 'email',
          placeholder: 'seuemail@email.com',
          required: true,
        },
        {
          label: 'Estado civil',
          model: 'estadoCivil',
          id: 'estadocivil',
          component: 'select',
          type: 'select',
          options: ['Selecione', 'Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)'],
          required: true,
        },
        {
          label: 'Nome Mãe',
          model: 'nm_mae',
          id: 'nm_mae',
          type: 'text',
          placeholder: 'Maria Marta Silva',
          required: true,
        },
        {
          label: 'Whatsapp Mãe',
          model: 'whatsapp_mae',
          id: 'whatsapp_mae',
          type: 'text',
          placeholder: '(31)99989-0000',
          required: true,
        },
        {
          label: 'Nome Pai',
          model: 'nm_pai',
          id: 'nm_pai',
          type: 'text',
          placeholder: 'Maria Marta Silva',
          required: true,
        },
        {
          label: 'Whatsapp Pai',
          model: 'whatsapp_pai',
          id: 'whatsapp_pai',
          type: 'text',
          placeholder: '(31)99989-0000',
          required: true,
        },
        {
          label: 'Pis',
          model: 'cd_pis',
          id: 'cd_pis',
          type: 'text',
          placeholder: '000.00000.00-0',
          required: true,
        },
        {
          label: 'Ctps',
          model: 'cd_ctps',
          id: 'cd_ctps',
          type: 'text',
          placeholder: '000.00000.00-0',
          required: true,
        },
        {
          label: 'Titulo de Eleitor',
          model: 'cd_eleitor',
          id: 'cd_eleitor',
          type: 'text',
          placeholder: '0000000000123',
          required: true,
        },
        {
          label: 'Cpf',
          model: 'cd_cpf',
          id: 'cd_cpf',
          type: 'text',
          placeholder: '000.000.000.23',
          required: true,
        },
        {
          label: 'Rg',
          model: 'cd_rg',
          id: 'cd_rg',
          type: 'text',
          placeholder: '00-000.008',
          required: true,
        },
        {
          label: 'Classificação Profissional',
          model: 'ie_qualificacao',
          id: 'ie_qualificacao',
          type: 'text',
          placeholder: '0000000000123',
          required: true,
        },
        {
          label: 'Capturar Face',
          type: 'button',
          buttonClass: 'send_btn',
          name: 'Matrix Face',
        },
        {
          label: 'Cadastrar',
          type: 'button',
          buttonClass: 'send_btn',
          name: 'Cadastrar',
        },
      ],
      popupOpen: false,
      stream: null,
    }
  },
  methods: {
    async cadastrar(usuario) {
      try {
        const response = await fetch('http://localhost:5000/usuario', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(usuario),
        })

        const data = await response.json()
        this.resultadoPost = JSON.stringify(data, null, 2)
      } catch (error) {
        console.error('Erro ao cadastrar:', error)
      }
    },

    handleButtonClick(event) {
      if (event === 'Matrix Face') {
        this.openPopup()
      }
      if (event === 'Matrix Digital') {
        this.openPopup()
      }
      if (event === 'Matrix Senha') {
        this.openPopup()
      }
    },
    openPopup() {
      this.popupOpen = true
      this.startCamera()
    },
    closePopup() {
      this.popupOpen = false
      if (this.stream) {
        this.stream.getTracks().forEach((track) => track.stop())
      }
    },
    startCamera() {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          this.stream = stream
          this.$refs.video.srcObject = stream
        })
        .catch((err) => {
          console.error('Erro ao acessar a câmera', err)
        })
    },
    capturePhoto() {
      const canvas = this.$refs.canvas
      const video = this.$refs.video
      const context = canvas.getContext('2d')
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      context.drawImage(video, 0, 0, canvas.width, canvas.height)
    },
    uploadImage() {
      const canvas = this.$refs.canvas
      const img = canvas.toDataURL('image/jpeg') // Gera o base64
      console.log(img) // Mostra a string base64 no console
      this.formData.matrix_face = img // Atribui a string base64 à variável
      this.closePopup() // Fecha o popup
    },
    submitForm() {
      console.log(this.formData)
      this.cadastrar(this.formData)
    },
  },
}
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background: white;
  padding: 20px;
  text-align: center;
  border-radius: 8px;
  width: 80%;
  max-width: 500px;
}

.popup-content video {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

button,
.send_btn {
  margin-top: 10px;
  padding: 10px;
  background-color: #6fcffb;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
}

button:hover,
.send_btn:hover {
  background-color: #444444;
}

.containet_back {
  background-color: #2221525d;
}
.container_form {
  width: 700px;
  margin: auto;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  box-shadow: 1px 0px 1.2px 0px #e3e3e3;
  border-radius: 3px;
  padding: 1em;
}

.container_form h1 {
  font-family: 'open_sansregular';
  font-size: 2.3em;
  color: #00dae0;
  border-bottom: 1px #f0eded solid;
  margin-bottom: 10px;
  padding-bottom: 10px;
}

.form_grupo {
  width: 90%;
  margin: 0 auto;
  margin-bottom: 30px;
  position: relative;
}

.form_grupo .legenda {
  width: 100%;
  float: left;
  margin-top: 15px;
  margin-bottom: 15px;
  font-weight: bold;
}

/* SUBMIT */

.submit {
  width: 100%;
  float: left;
}

.submit_btn {
  float: left;
  display: block;
  padding: 5px 30px;
  border: none;
  outline: none;
  background-color: #6fcffb;
  color: #fff;
  text-shadow: 0 0 5px rgb(0, 0, 0);
  font-family: inherit;
  font-size: 25px;
  font-family: 'open_sansregular';
  border-radius: 6px;
  margin: 20px auto;
  cursor: pointer;
  transition: all 0.3s;
}

.submit_btn:hover {
  background-color: #444444;
  transform: scale(1.03);
}

.dropdown {
  display: block;
  margin: 0 auto;
  font-size: 16px;
  font-family: inherit;
  color: #222222;
  border-radius: 4px;
  border: 1px #f2f2f2 solid;
  background: #fdfdfd;
  outline: none;
  padding-left: 10px;
  width: 100%;
}

.form_new_input {
  /*display: hidden;*/
  opacity: 0;
}

.radio_label,
.check_label {
  float: left;
  width: 100%;
  padding-left: 30px;
  cursor: pointer;
  margin-bottom: 8px;
}

.radio_new_btn {
  position: absolute;
  left: 0;
  transform: translateY(3px);
  height: 20px;
  width: 20px;
  border-radius: 50%;
  border: 0.2em solid #4c4c4c;
}

.radio_new_btn::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #6fcffb;
  visibility: hidden;
}

.check_new_btn {
  position: absolute;
  left: 0;
  height: 20px;
  width: 20px;
  border: 0.2em solid #4c4c4c;
}

.check_new_btn::after {
  content: '';
  height: 8px;
  width: 8px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #6fcffb;
  visibility: hidden;
}

.form_new_input:checked ~ .radio_label .radio_new_btn::after,
.form_new_input:checked ~ .check_label .check_new_btn::after {
  visibility: visible;
}

.form_new_input:checked ~ .radio_label,
.form_new_input:checked ~ .check_label {
  color: #6fcffb;
}

.form_grupo {
  width: 100%;
  margin-bottom: 20px;
  position: relative;
}

.form_input {
  font-size: 16px;
  font-family: inherit;
  padding: 8px 15px;
  border-radius: 4px;
  border: 1px #f2f2f2 solid;
  background: #fdfdfd;
  outline: none;
  width: 100%;
  transition: all 0.3s;
}

.form_message,
.form_message .message_input {
  width: 100%;
  float: left;
}

.form_message_label {
  width: 100%;
  float: left;
  margin-top: 15px;
  margin-bottom: 15px;
  font-weight: bold;
}
.container-back {
  position: relative;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.container-form {
  display: flex;
  justify-content: center;
  width: 100%;
}

.out {
  width: 70%;
  box-shadow: 0vw 0vh 2vh 1vh rgba(0, 0, 0, 0.2);
}
</style>
