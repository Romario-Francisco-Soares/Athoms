<template>
  <div class="form-group">
    <label v-if="type != 'button'" :for="id" class="form-label">{{ label }}</label>

    <!-- Input de texto, email ou data -->
    <input
      v-if="type === 'text' || type === 'email' ||
            type === 'date' || type === 'datetime-local' ||
            type === 'time'"
      :value="modelValue"
      @input="updateModelValue($event.target.value)"
      :type="type"
      :id="id"
      :name="name"
      :placeholder="placeholder"
      :required="required"
      class="form-input"
      :aria-label="label"
    />

    <!-- Select -->
    <select
      v-if="type === 'select'"
      :value="modelValue"
      @input="updateModelValue($event.target.value)"
      :id="id"
      :name="name"
      :required="required"
      class="form-input"
      :aria-label="label"
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

  </div>
  <div class="form-group">
    <!-- Button -->
    <button
      v-if="type === 'button'"
      :id="id"
      :name="name"
      @click="handleButtonClick(name)"
      :class="['form-button', buttonClass]"
      :aria-label="name"
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
  margin: 0 auto 20px auto;
  position: relative;
  max-width: 95%;
  background-color: #fdfdfd;
}

.form-label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

.form-input {
  width: 100%;
  padding: 8px 15px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  background-color: #fdfdfd;
  margin-bottom: 0.5rem;
}

.form-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 2px #a5b4fc44;
}

.radio-btn {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.radio-label {
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
}

.radio-btn-icon {
  display: inline-block;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid #aaa;
  margin-right: 10px;
  vertical-align: middle;
  background: #fff;
}

.form-new-input:checked + .radio-label .radio-btn-icon {
  background-color: #6fcffb;
}

/* Estilo para o botão */
.form-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 10px;
  transition: background 0.2s;
}

.form-button:hover {
  background-color: #3730a3;
}
</style>
