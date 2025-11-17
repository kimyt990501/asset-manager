<template>
  <div class="transaction-item">
    <div class="transaction-info">
      <div class="transaction-main">
        <span class="transaction-category">{{ transaction.category }}</span>
        <span class="transaction-account">{{ accountName }}</span>
      </div>
      <p v-if="transaction.description" class="transaction-description">
        {{ transaction.description }}
      </p>
      <p class="transaction-date">
        {{ formatDate(transaction.transaction_date) }}
      </p>
    </div>
    <div class="transaction-amount" :class="`transaction-${transaction.type}`">
      {{ transaction.type === 'income' ? '+' : '-' }}{{ formatCurrency(transaction.amount) }}
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Transaction } from '@/types'
import { useFormatter } from '@/composables/useFormatter'

interface Props {
  transaction: Transaction
  accountName: string
}

const props = defineProps<Props>()

const { formatCurrency, formatDate } = useFormatter()
</script>

<style scoped>
.transaction-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #ecf0f1;
  transition: background 0.2s ease;
}

.transaction-item:hover {
  background: #f8f9fa;
}

.transaction-item:last-child {
  border-bottom: none;
}

.transaction-info {
  flex: 1;
}

.transaction-main {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 0.5rem;
}

.transaction-category {
  font-weight: 600;
  color: #2c3e50;
}

.transaction-account {
  font-size: 0.85rem;
  color: #95a5a6;
  background: #ecf0f1;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
}

.transaction-description {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.transaction-date {
  margin: 0;
  font-size: 0.85rem;
  color: #95a5a6;
}

.transaction-amount {
  font-size: 1.25rem;
  font-weight: bold;
  margin-left: 1rem;
}

.transaction-income {
  color: #27ae60;
}

.transaction-expense {
  color: #e74c3c;
}

@media (max-width: 768px) {
  .transaction-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .transaction-amount {
    margin-left: 0;
    align-self: flex-end;
  }
}
</style>
