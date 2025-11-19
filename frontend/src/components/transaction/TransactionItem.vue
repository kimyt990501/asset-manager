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
  border-bottom: 1px solid var(--border-light);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.transaction-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--primary);
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.transaction-item:hover {
  background: var(--background);
  transform: translateX(4px);
}

.transaction-item:hover::before {
  transform: scaleY(1);
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
  color: var(--text-main);
}

.transaction-account {
  font-size: 0.85rem;
  color: var(--text-muted);
  background: var(--border-light);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
}

.transaction-description {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: var(--text-muted);
}

.transaction-date {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-light);
}

.transaction-amount {
  font-size: 1.25rem;
  font-weight: bold;
  margin-left: 1rem;
}

.transaction-income {
  color: var(--secondary);
}

.transaction-expense {
  color: var(--danger);
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
