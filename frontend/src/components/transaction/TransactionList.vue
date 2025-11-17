<template>
  <div class="transaction-list">
    <TransactionItem
      v-for="transaction in transactions"
      :key="transaction.id"
      :transaction="transaction"
      :account-name="getAccountName(transaction.account_id)"
      @click="handleTransactionClick(transaction)"
    />
  </div>
</template>

<script setup lang="ts">
import type { Transaction, Account } from '@/types'
import TransactionItem from './TransactionItem.vue'

interface Props {
  transactions: Transaction[]
  accounts: Account[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  transactionClick: [transaction: Transaction]
}>()

const getAccountName = (accountId: number): string => {
  const account = props.accounts.find(acc => acc.id === accountId)
  return account?.name || '알 수 없음'
}

const handleTransactionClick = (transaction: Transaction) => {
  emit('transactionClick', transaction)
}
</script>

<style scoped>
.transaction-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}
</style>
