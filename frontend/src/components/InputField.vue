<template>
  <div class="form-group">
    <label :for="id" class="form-label">{{ label }}</label>

    <!-- Input de texto, email ou data -->
    <input
      v-if="type === 'text' || type === 'email' || type === 'date'"
      :value="modelValue"
      @input="updateModelValue($event.target.value)"
      :type="type"
      :id="id"
      :name="name"
      :placeholder="placeholder"
      :required="required"
      class="form-input"
    />

    <!-- Select -->
    <select
      v-if="type === 'select'"
      :value="modelValue"
      @input="updateModelValue($event.target.value)"
      :id="id"
      type="select"
      :name="name"
      :required="required"
      class="form-input"
    >
      <option v-for="(option, index) in options" :key="index" :value="option">
        {{ option }}
      </option>
    </select>

    <div v-if="type === 'radio'" class="radio-btn">
      <div v-for="(option, index) in options" :key="index">
        <input
          :value="option"
          :checked="modelValue === option"
          @change="updateModelValue(option)"
          type="radio"
          :id="option"
          class="form-new-input"
        />
        <label :for="option" class="radio-label">
          <span class="radio-btn-icon"></span> {{ option }}
        </label>
      </div>
    </div>

    <!-- Button -->
    <button
      v-if="type === 'button'"
      :id="id"
      :name="name"
      @click="handleButtonClick(name)"
      :class="buttonClass"
    >
      {{ name }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'InputField',
  props: {
    modelValue: {
      type: [String, Number, Boolean],
      default: '',
    },
    label: {
      type: String,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      default: 'text',
    },
    placeholder: {
      type: String,
      default: '',
    },
    required: {
      type: Boolean,
      default: false,
    },
    options: {
      type: Array,
      default: () => [],
    },
    buttonClass: {
      // Adicionando a propriedade para receber a classe do botão
      type: String,
      default: '', // Caso não passe nenhuma classe, o valor será uma string vazia
    },
  },
  methods: {
    // Emitir o valor atualizado para o parent
    updateModelValue(value) {
      this.$emit('update:modelValue', value)
    },
    // Função para lidar com o clique no botão
    handleButtonClick(name) {
      this.$emit('button-click', name)
    },
  },
}
</script>

<style scoped>
/* Estilo básico de form-group para o InputField */
.form-group {
  margin: 0 auto;
  margin-bottom: 20px;
  position: relative;
  max-width: 90%;
  background-color: #fdfdfd;
}

.form-label {
  display: block;
  margin-bottom: 5px;
}

.form-input {
  width: 100%;
  padding: 8px 15px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
  background-color: #fdfdfd;
}

.radio-btn {
  display: flex;
  flex-direction: column;
}

.radio-btn .radio-label {
  cursor: pointer;
}

.radio-btn .radio-btn-icon {
  display: inline-block;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid #aaa;
  margin-right: 10px;
  vertical-align: middle;
}

.radio-btn input[type='radio']:checked + .radio-label .radio-btn-icon {
  background-color: #6fcffb;
}

/* Estilo para o botão */
.form-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.form-button:hover {
  background-color: #0056b3;
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

.form-new-input {
  opacity: 0;
}
</style>
