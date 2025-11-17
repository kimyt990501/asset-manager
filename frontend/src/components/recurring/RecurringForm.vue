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
        추가
      </Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import type { Account, RecurringFormData } from '../../types'
import { CATEGORIES } from '../../utils/constants'
import Button from '../common/Button.vue'

interface Props {
  accounts: Account[]
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
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
.recurring-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3498db;
}

.form-group textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}
</style>
