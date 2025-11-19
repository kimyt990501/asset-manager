<template>
  <div class="transaction-skeleton">
    <div class="skeleton-left">
      <BaseSkeleton circle width="40px" height="40px" />
      <div class="skeleton-info">
        <BaseSkeleton width="140px" height="1rem" />
        <BaseSkeleton width="100px" height="0.875rem" style="margin-top: 0.25rem;" />
      </div>
    </div>
    <div class="skeleton-right">
      <BaseSkeleton width="100px" height="1.25rem" />
      <BaseSkeleton width="80px" height="0.875rem" style="margin-top: 0.25rem;" />
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseSkeleton from '../ui/BaseSkeleton.vue'
</script>

<style scoped>
.transaction-skeleton {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background: var(--surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
  margin-bottom: var(--spacing-sm);
}

.skeleton-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.skeleton-info {
  display: flex;
  flex-direction: column;
}

.skeleton-right {
  text-align: right;
}
</style>
