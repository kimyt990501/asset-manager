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
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 1rem;
  align-items: center;
}

.summary-icon {
  font-size: 2.5rem;
  width: 4rem;
  height: 4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: #f8f9fa;
}

.summary-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #7f8c8d;
  font-weight: normal;
}

.summary-amount {
  font-size: 1.75rem;
  font-weight: bold;
  margin: 0;
  color: #2c3e50;
}

.summary-card--income .summary-amount {
  color: #27ae60;
}

.summary-card--expense .summary-amount {
  color: #e74c3c;
}

.summary-subtitle {
  font-size: 0.8rem;
  color: #95a5a6;
}
</style>
