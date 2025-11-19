<template>
  <div class="summary-grid">
    <BaseCard class="summary-card">
      <div class="card-label">총 자산</div>
      <div class="card-value text-primary">{{ formatCurrency(assets) }}</div>
    </BaseCard>
    
    <BaseCard class="summary-card">
      <div class="card-label">부채</div>
      <div class="card-value text-danger">{{ formatCurrency(liabilities) }}</div>
    </BaseCard>
    
    <BaseCard class="summary-card">
      <div class="card-label">순자산</div>
      <div class="card-value text-success">{{ formatCurrency(assets - liabilities) }}</div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import BaseCard from '../ui/BaseCard.vue'

defineProps({
  assets: { type: Number, default: 0 },
  liabilities: { type: Number, default: 0 }
})

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(value)
}
</script>

<style scoped>
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.summary-card {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.card-label {
  font-size: 0.875rem;
  color: var(--text-muted);
  font-weight: 500;
}

.card-value {
  font-size: 1.5rem;
  font-weight: 700;
}

.text-primary { color: var(--primary); }
.text-danger { color: var(--danger); }
.text-success { color: var(--secondary); }
</style>
