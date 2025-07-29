<template>
  <transition name="fade">
    <div v-if="show" class="ui-alert" :class="type">
      <span class="msg">{{ message }}</span>
      <button class="close-btn" @click="closeAlert">&times;</button>
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    show: Boolean,
    message: String,
    type: {
      type: String,
      default: 'info' // info, success, error, warning
    }
  },
  watch: {
    show(val) {
      if (val) {
        clearTimeout(this._timer)
        this._timer = setTimeout(() => {
          this.closeAlert()
        }, 4000)
      }
    }
  },
  methods: {
    closeAlert() {
      this.$emit('close')
    }
  },
  beforeUnmount() {
    clearTimeout(this._timer)
  }
}
</script>

<style scoped>
.ui-alert {
  position: fixed;
  top: 32px;
  left: 50%;
  transform: translateX(-50%);
  min-width: 320px;
  max-width: 90vw;
  padding: 1rem 2.5rem 1rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.13);
  font-size: 1.1rem;
  font-weight: 500;
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: slideDown 0.3s;
}
.ui-alert.info { background: #e0e7ff; color: #3730a3; border-left: 6px solid #6366f1; }
.ui-alert.success { background: #dcfce7; color: #166534; border-left: 6px solid #22c55e; }
.ui-alert.error { background: #fee2e2; color: #991b1b; border-left: 6px solid #ef4444; }
.ui-alert.warning { background: #fef9c3; color: #92400e; border-left: 6px solid #f59e42; }
.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: inherit;
  cursor: pointer;
  margin-left: auto;
  padding: 0 0.5rem;
}
@keyframes slideDown {
  from { opacity: 0; transform: translate(-50%, -30px);}
  to { opacity: 1; transform: translate(-50%, 0);}
}
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
