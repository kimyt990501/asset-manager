<template>
  <form @submit.prevent="handleSubmit" class="transaction-form">
    <div class="form-group">
      <label for="account_id">계좌 *</label>
      <select id="account_id" v-model.number="formData.account_id" required>
        <option :value="0" disabled>계좌를 선택하세요</option>
        <option v-for="account in accounts" :key="account.id" :value="account.id">
          {{ account.name }} ({{ formatCurrency(account.balance) }})
        </option>
      </select>
    </div>

    <div class="form-group">
      <label for="type">거래 유형 *</label>
      <select id="type" v-model="formData.type" required>
        <option value="income">수입</option>
        <option value="expense">지출</option>
      </select>
    </div>

    <div class="form-group">
      <label for="category">카테고리 *</label>
      <select id="category" v-model="formData.category" required>
        <option v-for="cat in availableCategories" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label for="amount">금액 *</label>
      <input
        id="amount"
        v-model.number="formData.amount"
        type="number"
        placeholder="0"
        step="1"
        min="1"
        required
      />
    </div>

    <div class="form-group">
      <label for="transaction_date">날짜 *</label>
      <input
        id="transaction_date"
        v-model="formData.transaction_date"
        type="date"
        required
      />
    </div>

    <div class="form-group">
      <label for="description">메모</label>
      <textarea
        id="description"
        v-model="formData.description"
        rows="3"
        placeholder="거래 메모를 입력하세요"
      ></textarea>
    </div>

    <div class="form-actions">
      <Button variant="secondary" type="button" @click="$emit('cancel')">
        취소
      </Button>
      <Button variant="primary" type="submit" :loading="loading">
        추가
      </Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import type { Account, TransactionFormData } from '@/types'
import { CATEGORIES } from '@/utils/constants'
import { useFormatter } from '@/composables/useFormatter'
import Button from '@/components/common/Button.vue'

interface Props {
  accounts: Account[]
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const emit = defineEmits<{
  submit: [data: TransactionFormData]
  cancel: []
}>()

const { formatCurrency } = useFormatter()

const formData = reactive<TransactionFormData>({
  account_id: 0,
  type: 'expense',
  category: '',
  amount: 0,
  description: '',
  transaction_date: new Date().toISOString().split('T')[0]
})

const availableCategories = computed(() => {
  return formData.type === 'income' ? CATEGORIES.income : CATEGORIES.expense
})

const handleSubmit = () => {
  if (formData.account_id === 0) {
    alert('계좌를 선택해주세요')
    return
  }
  emit('submit', { ...formData })
}
</script>

<style scoped>
.transaction-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.form-group label {
  font-weight: 600;
  color: var(--text-main);
  font-size: 0.9rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-family: inherit;
  background-color: var(--surface);
  color: var(--text-main);
  transition: var(--transition-base);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.form-group textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: flex-end;
  margin-top: var(--spacing-md);
}
</style>
