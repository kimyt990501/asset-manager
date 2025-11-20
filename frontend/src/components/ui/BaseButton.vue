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
  background: var(--primary);
  color: white;
  border: 1px solid transparent;
  box-shadow: var(--shadow-sm);
}

.base-btn--primary:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* Electric Variant for Call to Actions */
.base-btn--primary.electric {
  background: var(--accent);
  background: var(--accent-gradient);
  box-shadow: var(--shadow-glow-primary);
}

.base-btn--primary.electric:hover:not(:disabled) {
  filter: brightness(1.1);
  box-shadow: var(--shadow-glow-primary), var(--shadow-md);
}

.base-btn--secondary {
  background: var(--surface);
  color: var(--text-main);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.base-btn--secondary:hover:not(:disabled) {
  background: var(--surface-hover);
  border-color: var(--border-dark);
  color: var(--text-main);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.base-btn--danger {
  background: var(--danger);
  color: white;
  border: 1px solid transparent;
  box-shadow: var(--shadow-sm);
}

.base-btn--danger:hover:not(:disabled) {
  background: var(--danger-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
  box-shadow: var(--shadow-glow-danger);
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
