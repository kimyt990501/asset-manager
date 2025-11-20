<template>
  <div class="base-card">
    <slot></slot>
  </div>
</template>

<style scoped>
.base-card {
  background: var(--surface);
  border-radius: var(--radius-xl); /* Bento Radius */
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-lg);
  border: 1px solid var(--border);
  transition: var(--transition-base);
  position: relative;
  overflow: hidden;
}

.base-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--border-dark);
}
</style>
