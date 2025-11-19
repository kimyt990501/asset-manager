<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-backdrop" @click="$emit('close')">
        <div class="modal-container" @click.stop>
          <header class="modal-header">
            <h3 class="modal-title">{{ title }}</h3>
            <button class="close-btn" @click="$emit('close')">&times;</button>
          </header>
          
          <div class="modal-body">
            <slot></slot>
          </div>
          
          <footer v-if="$slots.footer" class="modal-footer">
            <slot name="footer"></slot>
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: ''
  }
})

defineEmits(['close'])
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-container {
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-main);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.close-btn:hover {
  color: var(--text-main);
}

.modal-body {
  padding: var(--spacing-lg);
}

.modal-footer {
  padding: var(--spacing-lg);
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: translateY(20px);
}
</style>
