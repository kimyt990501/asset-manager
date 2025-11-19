<template>
  <div class="recurring-page">
    <div class="page-header">
      <h1>고정 지출 목록</h1>
      <Button variant="primary" @click="openCreateModal">
        + 고정 지출 추가
      </Button>
    </div>

    <Loading v-if="loading && recurringTransactions.length === 0" />

    <div v-else-if="recurringTransactions.length === 0" class="empty-state">
      <p>등록된 고정 지출이 없습니다.</p>
      <Button variant="primary" @click="openCreateModal">
        첫 고정 지출 추가하기
      </Button>
    </div>

    <div v-else class="recurring-list">
      <div v-for="recurring in recurringTransactions" :key="recurring.id" class="recurring-item">
        <div class="recurring-info">
          <div class="recurring-main">
            <span class="recurring-category">{{ recurring.category }}</span>
            <span class="recurring-frequency">{{ getFrequencyLabel(recurring.frequency) }}</span>
            <span v-if="!recurring.is_active" class="inactive-badge">비활성</span>
          </div>
          <p v-if="recurring.description" class="recurring-description">
            {{ recurring.description }}
          </p>
          <p class="recurring-schedule">
            매월 {{ recurring.day_of_month }}일
          </p>
        </div>
        <div class="recurring-actions">
          <div class="recurring-amount" :class="`transaction-${recurring.type}`">
            {{ recurring.type === 'income' ? '+' : '-' }}{{ formatCurrency(recurring.amount) }}
          </div>
          <Button 
            v-if="recurring.is_active"
            variant="danger" 
            @click="handleDeactivate(recurring.id)"
          >
            비활성화
          </Button>
        </div>
      </div>
    </div>

    <!-- Create Modal -->
    <Modal
      :is-open="isModalOpen"
      title="정기 거래 추가"
      @close="closeModal"
    >
      <RecurringForm
        :accounts="accounts"
        :loading="formLoading"
        @submit="handleSubmit"
        @cancel="closeModal"
      />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAccountStore } from '@/stores/accountStore'
import { useRecurringStore } from '@/stores/recurringStore'
import { useModal } from '@/composables/useModal'
import { useNotification } from '@/composables/useNotification'
import { useFormatter } from '@/composables/useFormatter'
import { FREQUENCY_LABELS } from '@/utils/constants'
import type { RecurringFormData } from '@/types'
import RecurringForm from '@/components/recurring/RecurringForm.vue'
import Modal from '@/components/ui/BaseModal.vue'
import Button from '@/components/ui/BaseButton.vue'
import Loading from '@/components/common/Loading.vue'

const accountStore = useAccountStore()
const recurringStore = useRecurringStore()
const { accounts } = storeToRefs(accountStore)
const { recurringTransactions, loading } = storeToRefs(recurringStore)
const { isOpen: isModalOpen, open: openModal, close: closeModal } = useModal()
const { success, error } = useNotification()
const { formatCurrency } = useFormatter()

const formLoading = ref(false)

onMounted(async () => {
  await Promise.all([
    accountStore.fetchAccounts(),
    recurringStore.fetchRecurring()
  ])
})

const getFrequencyLabel = (frequency: string) => {
  return FREQUENCY_LABELS[frequency] || frequency
}

const openCreateModal = () => {
  openModal()
}

const handleSubmit = async (formData: RecurringFormData) => {
  formLoading.value = true
  try {
    await recurringStore.createRecurring(formData)
    success('정기 거래가 추가되었습니다.')
    closeModal()
  } catch (err) {
    error('정기 거래 추가에 실패했습니다.')
  } finally {
    formLoading.value = false
  }
}

const handleDeactivate = async (id: number) => {
  if (!confirm('이 정기 거래를 비활성화하시겠습니까?')) {
    return
  }
  
  try {
    await recurringStore.deactivateRecurring(id)
    success('정기 거래가 비활성화되었습니다.')
  } catch (err) {
    error('비활성화에 실패했습니다.')
  }
}
</script>

<style scoped>
.recurring-page {
  min-height: calc(100vh - 64px - 4rem);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.page-header h1 {
  margin: 0;
  color: var(--text-main);
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.recurring-list {
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  border: 1px solid var(--border-light);
}

.recurring-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border);
  transition: var(--transition-base);
}

.recurring-item:hover {
  background: var(--background);
}

.recurring-item:last-child {
  border-bottom: none;
}

.recurring-info {
  flex: 1;
}

.recurring-main {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.recurring-category {
  font-weight: 600;
  color: var(--text-main);
  font-size: 1rem;
}

.recurring-frequency {
  font-size: 0.85rem;
  color: var(--text-muted);
  background: var(--border-light);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
  font-weight: 500;
}

.inactive-badge {
  font-size: 0.75rem;
  color: var(--danger);
  background: var(--danger-light);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
  font-weight: 600;
}

.recurring-description {
  margin: var(--spacing-sm) 0;
  font-size: 0.9rem;
  color: var(--text-muted);
}

.recurring-schedule {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-light);
}

.recurring-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--spacing-md);
}

.recurring-amount {
  font-size: 1.25rem;
  font-weight: 700;
}

.transaction-income {
  color: var(--secondary);
}

.transaction-expense {
  color: var(--danger);
}

.empty-state {
  text-align: center;
  padding: var(--spacing-2xl);
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.empty-state p {
  color: var(--text-muted);
  margin-bottom: var(--spacing-lg);
  font-size: 1.1rem;
}
</style>
