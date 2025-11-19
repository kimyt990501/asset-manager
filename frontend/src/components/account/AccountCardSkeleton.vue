<template>
  <div class="account-card-skeleton">
    <div class="skeleton-header">
      <div>
        <BaseSkeleton width="120px" height="1.25rem" />
        <BaseSkeleton width="80px" height="0.875rem" style="margin-top: 0.5rem;" />
      </div>
      <div class="skeleton-actions">
        <BaseSkeleton circle width="32px" height="32px" />
        <BaseSkeleton circle width="32px" height="32px" />
      </div>
    </div>

    <BaseSkeleton width="180px" height="2.25rem" style="margin: 1rem 0;" />

    <div class="skeleton-footer">
      <BaseSkeleton width="100px" height="0.875rem" />
      <BaseSkeleton width="80px" height="0.875rem" />
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseSkeleton from '../ui/BaseSkeleton.vue'
</script>

<style scoped>
.account-card-skeleton {
  background: var(--surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.skeleton-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-md);
}

.skeleton-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.skeleton-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
