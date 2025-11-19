<template>
  <div :class="['toast', `toast--${type}`]" role="alert" @click="$emit('close')">
    <div class="toast-icon">
      <span v-if="type === 'success'">✓</span>
      <span v-else-if="type === 'error'">✕</span>
      <span v-else-if="type === 'warning'">⚠</span>
      <span v-else-if="type === 'info'">ℹ</span>
    </div>
    <div class="toast-message">{{ message }}</div>
    <button
      class="toast-close"
      @click.stop="$emit('close')"
      aria-label="알림 닫기"
    >
      ✕
    </button>
  </div>
</template>

<script setup lang="ts">
import type { ToastType } from '@/stores/toastStore'

interface Props {
  type: ToastType
  message: string
}

defineProps<Props>()
defineEmits(['close'])
</script>

<style scoped>
.toast {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  border: 1px solid;
  min-width: 300px;
  max-width: 500px;
  cursor: pointer;
  transition: var(--transition-base);
  animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast:hover {
  transform: translateX(-4px);
  box-shadow: var(--shadow-xl);
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.toast-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: var(--font-sm);
  font-weight: var(--font-bold);
  flex-shrink: 0;
}

.toast-message {
  flex: 1;
  font-size: var(--font-sm);
  font-weight: var(--font-medium);
  line-height: var(--leading-normal);
}

.toast-close {
  background: none;
  border: none;
  font-size: var(--font-lg);
  cursor: pointer;
  color: inherit;
  opacity: 0.6;
  padding: var(--spacing-xs);
  border-radius: var(--radius-sm);
  transition: var(--transition-fast);
  flex-shrink: 0;
  line-height: 1;
}

.toast-close:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.05);
}

/* Success Variant */
.toast--success {
  border-color: var(--secondary);
  background: var(--secondary-light);
}

.toast--success .toast-icon {
  background: var(--secondary);
  color: white;
}

.toast--success .toast-message {
  color: var(--secondary-hover);
}

/* Error Variant */
.toast--error {
  border-color: var(--danger);
  background: var(--danger-light);
}

.toast--error .toast-icon {
  background: var(--danger);
  color: white;
}

.toast--error .toast-message {
  color: var(--danger-hover);
}

/* Warning Variant */
.toast--warning {
  border-color: var(--warning);
  background: #fef3c7; /* Amber 100 */
}

.toast--warning .toast-icon {
  background: var(--warning);
  color: white;
}

.toast--warning .toast-message {
  color: #b45309; /* Amber 700 */
}

/* Info Variant */
.toast--info {
  border-color: var(--primary);
  background: var(--primary-light);
}

.toast--info .toast-icon {
  background: var(--primary);
  color: white;
}

.toast--info .toast-message {
  color: var(--primary-hover);
}
</style>
