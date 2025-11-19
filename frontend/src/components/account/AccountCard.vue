<template>
  <div class="account-card" :style="{ borderLeftColor: accountColorVar }">
    <div class="account-header">
      <div>
        <h3>{{ account.name }}</h3>
        <span class="account-type">{{ getAccountTypeLabel(account.type) }}</span>
      </div>
      <div class="action-buttons">
        <button
          class="action-btn action-btn--edit"
          @click="$emit('edit', account)"
          aria-label="계좌 수정"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </button>
        <button
          class="action-btn action-btn--delete"
          @click="$emit('delete', account)"
          aria-label="계좌 삭제"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            <line x1="10" y1="11" x2="10" y2="17"></line>
            <line x1="14" y1="11" x2="14" y2="17"></line>
          </svg>
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
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: 1px solid transparent;
  cursor: pointer;
  padding: var(--spacing-xs);
  transition: var(--transition-base);
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  width: 32px;
  height: 32px;
}

.action-btn:hover {
  background: var(--background);
  color: var(--text-main);
  transform: translateY(-1px);
}

.action-btn:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

.action-btn--edit:hover {
  background: var(--primary-light);
  color: var(--primary);
}

.action-btn--delete:hover {
  background: var(--danger-light);
  color: var(--danger);
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
