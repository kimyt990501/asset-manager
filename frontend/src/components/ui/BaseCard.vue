<template>
  <div class="base-card">
    <slot></slot>
  </div>
</template>

<style scoped>
.base-card {
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-lg);
  border: 1px solid var(--border-light);
  transition: var(--transition-base);
}

.base-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--border);
}
</style>
