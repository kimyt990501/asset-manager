<template>
  <div class="base-input-wrapper">
    <label v-if="label" class="base-input-label">{{ label }}</label>
    <input
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      class="base-input"
      :class="{ 'base-input--error': error }"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <span v-if="error" class="base-input-error">{{ error }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  placeholder: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.base-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
}

.base-input-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-main);
}

.base-input {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 1rem;
  transition: var(--transition-base);
  background: var(--surface);
  color: var(--text-main);
}

.base-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1);
}

.base-input--error {
  border-color: var(--danger);
}

.base-input-error {
  font-size: 0.75rem;
  color: var(--danger);
}
</style>
