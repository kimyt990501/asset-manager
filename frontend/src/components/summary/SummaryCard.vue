<template>
  <div class="summary-card" :class="`summary-card--${type}`">
    <div class="summary-icon">{{ icon }}</div>
    <div class="summary-content">
      <h3>{{ title }}</h3>
      <p class="summary-amount">{{ formatCurrency(amount) }}</p>
      <span v-if="subtitle" class="summary-subtitle">{{ subtitle }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useFormatter } from '../../composables/useFormatter'
import { computed } from 'vue'

interface Props {
  title: string
  amount: number
  type: 'assets' | 'income' | 'expense' | 'cashflow'
  subtitle?: string
}

const props = defineProps<Props>()

const { formatCurrency } = useFormatter()

const icon = computed(() => {
  switch (props.type) {
    case 'assets': return '💰'
    case 'income': return '📈'
    case 'expense': return '📉'
    case 'cashflow': return '💵'
    default: return '📊'
  }
})
</script>

<style scoped>
.summary-card {
  background: var(--surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.summary-icon {
  font-size: 2.5rem;
  width: 4rem;
  height: 4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
  background: var(--background);
}

.summary-content h3 {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-sm);
  color: var(--text-muted);
  font-weight: normal;
}

.summary-amount {
  font-size: var(--font-3xl);
  font-weight: var(--font-bold);
  margin: 0;
  color: var(--text-main);
}

.summary-card--income .summary-amount {
  color: var(--secondary);
}

.summary-card--expense .summary-amount {
  color: var(--danger);
}

.summary-subtitle {
  font-size: var(--font-xs);
  color: var(--text-light);
}
</style>
