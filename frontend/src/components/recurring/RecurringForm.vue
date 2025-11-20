<template>
  <form @submit.prevent="handleSubmit" class="recurring-form">
    <div class="form-group">
      <label for="account_id">계좌 *</label>
      <select id="account_id" v-model.number="formData.account_id" required>
        <option :value="0" disabled>계좌를 선택하세요</option>
        <option v-for="account in accounts" :key="account.id" :value="account.id">
          {{ account.name }}
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
      <label for="frequency">주기 *</label>
      <select id="frequency" v-model="formData.frequency" required>
        <option value="monthly">매월</option>
        <option value="weekly">매주</option>
        <option value="yearly">매년</option>
      </select>
    </div>

    <div v-if="formData.frequency === 'monthly'" class="form-group">
      <label for="day_of_month">매월 몇 일? *</label>
      <input
        id="day_of_month"
        v-model.number="formData.day_of_month"
        type="number"
        placeholder="1"
        min="1"
        max="31"
        required
      />
    </div>

    <div class="form-group">
      <label for="start_date">시작일 *</label>
      <input
        id="start_date"
        v-model="formData.start_date"
        type="date"
        required
      />
    </div>

    <div class="form-group">
      <label for="end_date">종료일 (선택)</label>
      <input
        id="end_date"
        v-model="formData.end_date"
        type="date"
      />
    </div>

    <div class="form-group">
      <label for="description">메모</label>
      <textarea
        id="description"
        v-model="formData.description"
        rows="3"
        placeholder="메모를 입력하세요"
      ></textarea>
    </div>

    <div class="form-actions">
      <Button variant="secondary" type="button" @click="$emit('cancel')">
        취소
      </Button>
      <Button variant="primary" type="submit" :loading="loading">
        {{ isEditMode ? '수정' : '추가' }}
      </Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, computed, watch } from 'vue'
import type { Account, RecurringFormData, RecurringTransaction } from '../../types'
import { CATEGORIES } from '../../utils/constants'
import Button from '../ui/BaseButton.vue'

interface Props {
  accounts: Account[]
  loading?: boolean
  initialData?: RecurringTransaction | null
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  initialData: null
})

const emit = defineEmits<{
  submit: [data: RecurringFormData]
  cancel: []
}>()

const formData = reactive<RecurringFormData>({
  account_id: 0,
  type: 'expense',
  category: '',
  amount: 0,
  description: '',
  frequency: 'monthly',
  day_of_month: 1,
  start_date: new Date().toISOString().split('T')[0],
  end_date: undefined,
  is_active: true
})

// initialData가 변경될 때 formData 업데이트
watch(() => props.initialData, (newData) => {
  if (newData) {
    formData.account_id = newData.account_id
    formData.type = newData.type
    formData.category = newData.category
    formData.amount = newData.amount
    formData.description = newData.description || ''
    formData.frequency = newData.frequency
    formData.day_of_month = newData.day_of_month || 1
    formData.start_date = newData.start_date
    formData.end_date = newData.end_date || undefined
    formData.is_active = newData.is_active ?? true
  } else {
    // 초기화
    formData.account_id = 0
    formData.type = 'expense'
    formData.category = ''
    formData.amount = 0
    formData.description = ''
    formData.frequency = 'monthly'
    formData.day_of_month = 1
    formData.start_date = new Date().toISOString().split('T')[0]
    formData.end_date = undefined
    formData.is_active = true
  }
}, { immediate: true })

// type 변경 시 카테고리 자동 선택
watch(() => formData.type, (newType) => {
  const categories = newType === 'income' ? CATEGORIES.income : CATEGORIES.expense
  if (!categories.includes(formData.category)) {
    formData.category = categories[0]
  }
})

const availableCategories = computed(() => {
  return formData.type === 'income' ? CATEGORIES.income : CATEGORIES.expense
})

const isEditMode = computed(() => props.initialData !== null)

const handleSubmit = () => {
  if (formData.account_id === 0) {
    alert('계좌를 선택해주세요')
    return
  }
  emit('submit', { ...formData })
}
</script>

<style scoped>
.recurring-form {
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
