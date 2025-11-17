<template>
  <div class="account-card" :style="{ borderLeftColor: accountColor }">
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
import { ACCOUNT_TYPE_COLORS } from '@/utils/constants'


interface Props {
  account: Account
}

const props = defineProps<Props>()
const emit = defineEmits<{
  edit: [account: Account]
  delete: [account: Account]
}>()

const { formatCurrency, formatShortDate, getAccountTypeLabel } = useFormatter()

const accountColor = computed(() => ACCOUNT_TYPE_COLORS[props.account.type] || '#95a5a6')
</script>

<style scoped>
.account-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-left: 4px solid;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.account-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.account-header h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.account-type {
  background: #ecf0f1;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  color: #7f8c8d;
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  transition: transform 0.2s ease;
}

.action-btn:hover {
  transform: scale(1.2);
}

.action-btn--delete:hover {
  filter: brightness(0.8);
}

.account-balance {
  font-size: 1.75rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 1rem 0;
}

.account-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: #95a5a6;
}
</style>
