<template>
  <div class="account-card" :style="{ borderLeftColor: accountColorVar }">
    <div class="account-header">
      <div>
        <h3>{{ account.name }}</h3>
        <span class="account-type">{{ getAccountTypeLabel(account.type) }}</span>
      </div>
      <div class="action-buttons">
        <button class="action-btn" @click="$emit('edit', account)" title="수정">
          ✏️
        </button>
        <button class="action-btn action-btn--delete" @click="$emit('delete', account)" title="삭제">
          🗑️
        </button>
      </div>
    </div>
    
    <div class="account-balance">
      {{ formatCurrency(account.balance) }}
    </div>
    
    <div class="account-footer">
      <span class="institution">{{ account.institution }}</span>
      <span class="date">{{ formatShortDate(account.updated_at) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Account } from '@/types'
import { useFormatter } from '@/composables/useFormatter'

interface Props {
  account: Account
}

const props = defineProps<Props>()
const emit = defineEmits<{
  edit: [account: Account]
  delete: [account: Account]
}>()

const { formatCurrency, formatShortDate, getAccountTypeLabel } = useFormatter()

// CSS 변수로 계좌 타입별 색상 매핑
const accountColorVar = computed(() => {
  const colorMap: Record<string, string> = {
    checking: 'var(--account-checking)',
    savings: 'var(--account-savings)',
    investment: 'var(--account-investment)',
    cma: 'var(--account-credit)', // CMA를 credit 색상으로 매핑
    credit: 'var(--account-credit)',
    loan: 'var(--account-loan)'
  }
  return colorMap[props.account.type] || 'var(--account-other)'
})
</script>

<style scoped>
.account-card {
  background: var(--surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border-left: 4px solid;
  transition: var(--transition-base);
  border: 1px solid var(--border-light);
}

.account-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--border);
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-md);
}

.account-header h3 {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-lg);
  font-weight: var(--font-semibold);
  color: var(--text-main);
  letter-spacing: -0.01em;
}

.account-type {
  background: var(--background);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-full);
  font-size: var(--font-xs);
  color: var(--text-muted);
  font-weight: var(--font-medium);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-sm);
}

.action-btn {
  background: none;
  border: none;
  font-size: var(--font-xl);
  cursor: pointer;
  padding: var(--spacing-xs);
  transition: var(--transition-base);
  border-radius: var(--radius-sm);
}

.action-btn:hover {
  transform: scale(1.15);
  background: var(--background);
}

.action-btn--delete:hover {
  filter: brightness(0.8);
}

.account-balance {
  font-size: var(--font-3xl);
  font-weight: var(--font-bold);
  color: var(--text-main);
  margin: var(--spacing-md) 0;
}

.account-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--font-sm);
  color: var(--text-light);
}
</style>
