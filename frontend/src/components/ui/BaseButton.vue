<template>
  <button
    :class="['base-btn', `base-btn--${variant}`, `base-btn--${size}`, { 'base-btn--loading': loading }]"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span v-if="loading" class="spinner"></span>
    <slot v-else></slot>
  </button>
</template>

<script setup lang="ts">
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value: string) => ['primary', 'secondary', 'danger', 'ghost'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value: string) => ['sm', 'md', 'lg'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const handleClick = (event: MouseEvent) => {
  emit('click', event)
}
</script>

<style scoped>
.base-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-base);
  font-family: inherit;
  letter-spacing: 0.01em;
}

.base-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

.base-btn:active:not(:disabled) {
  transform: scale(0.98);
}

/* Variants */
.base-btn--primary {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
}
.base-btn--primary:hover:not(:disabled) {
  box-shadow: 0 6px 10px -1px rgba(99, 102, 241, 0.4);
  transform: translateY(-1px);
}

.base-btn--secondary {
  background: linear-gradient(135deg, var(--secondary) 0%, var(--secondary-hover) 100%);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.3);
}
.base-btn--secondary:hover:not(:disabled) {
  box-shadow: 0 6px 10px -1px rgba(16, 185, 129, 0.4);
  transform: translateY(-1px);
}

.base-btn--danger {
  background: linear-gradient(135deg, var(--danger) 0%, var(--danger-hover) 100%);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(244, 63, 94, 0.3);
}
.base-btn--danger:hover:not(:disabled) {
  box-shadow: 0 6px 10px -1px rgba(244, 63, 94, 0.4);
  transform: translateY(-1px);
}

.base-btn--ghost {
  background-color: transparent;
  color: var(--text-muted);
}
.base-btn--ghost:hover:not(:disabled) {
  background-color: var(--background);
  color: var(--text-main);
}

/* Sizes */
.base-btn--sm {
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: 0.875rem;
}

.base-btn--md {
  padding: var(--spacing-sm) var(--spacing-lg);
  font-size: 1rem;
}

.base-btn--lg {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: 1.125rem;
}

/* Loading State */
.base-btn--loading {
  position: relative;
  pointer-events: none;
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
