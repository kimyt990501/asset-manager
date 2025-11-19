<template>
  <div class="summary-card-skeleton">
    <BaseSkeleton width="80px" height="0.875rem" />
    <BaseSkeleton width="140px" height="1.75rem" style="margin-top: 0.5rem;" />
  </div>
</template>

<script setup lang="ts">
import BaseSkeleton from '../ui/BaseSkeleton.vue'
</script>

<style scoped>
.summary-card-skeleton {
  background: var(--surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
}
</style>
