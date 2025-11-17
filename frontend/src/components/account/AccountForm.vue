<template>
  <form @submit.prevent="handleSubmit" class="account-form">
    <div class="form-group">
      <label for="name">계좌명 *</label>
      <input
        id="name"
        v-model="formData.name"
        type="text"
        placeholder="신한은행 입출금"
        required
      />
    </div>

    <div class="form-group">
      <label for="type">계좌 유형 *</label>
      <select id="type" v-model="formData.type" required>
        <option value="checking">입출금</option>
        <option value="savings">저축</option>
        <option value="investment">투자</option>
        <option value="cma">CMA</option>
      </select>
    </div>

    <div class="form-group">
      <label for="balance">잔액 *</label>
      <input
        id="balance"
        v-model.number="formData.balance"
        type="number"
        placeholder="0"
        step="1"
        required
      />
    </div>

    <div class="form-group">
      <label for="institution">금융기관</label>
      <input
        id="institution"
        v-model="formData.institution"
        type="text"
        placeholder="신한은행"
      />
    </div>

    <div class="form-group">
      <label for="account_number">계좌번호</label>
      <input
        id="account_number"
        v-model="formData.account_number"
        type="text"
        placeholder="110-123-456789"
      />
    </div>

    <div class="form-actions">
      <Button variant="secondary" type="button" @click="$emit('cancel')">
        취소
      </Button>
      <Button variant="primary" type="submit" :loading="loading">
        {{ isEdit ? '수정' : '생성' }}
      </Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { reactive, watch } from 'vue'
import type { Account, AccountFormData } from '../../types'
import Button from '../common/Button.vue'

interface Props {
  account?: Account
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const emit = defineEmits<{
  submit: [data: AccountFormData]
  cancel: []
}>()

const isEdit = computed(() => !!props.account)

const formData = reactive<AccountFormData>({
  name: '',
  type: 'checking',
  balance: 0,
  institution: '',
  account_number: ''
})

watch(() => props.account, (account) => {
  if (account) {
    formData.name = account.name
    formData.type = account.type
    formData.balance = account.balance
    formData.institution = account.institution || ''
    formData.account_number = account.account_number || ''
  }
}, { immediate: true })

const handleSubmit = () => {
  emit('submit', { ...formData })
}
</script>

<style scoped>
.account-form {
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
.form-group select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}
</style>
