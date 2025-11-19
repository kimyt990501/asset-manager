<template>
  <div class="recurring-page">
    <div class="page-header">
      <h1>고정 지출 목록</h1>
      <Button variant="primary" @click="openCreateModal">
        + 고정 지출 추가
      </Button>
    </div>

    <BaseEmptyState
      v-if="recurringTransactions.length === 0"
      title="고정 지출이 없습니다"
      description="정기적으로 발생하는 지출을 등록하여 예산 관리를 더 효율적으로 하세요."
      action="고정 지출 추가하기"
      @action="openCreateModal"
    >
      <template #icon>
        <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
      </template>
    </BaseEmptyState>

    <div v-else class="recurring-list">
      <div
        v-for="(recurring, index) in recurringTransactions"
        :key="recurring.id"
        :style="{ animationDelay: `${index * 0.03}s` }"
        class="recurring-item recurring-item-animate"
      >
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
          <div class="action-buttons">
            <button class="action-btn edit-btn" @click="openEditModal(recurring)">
              수정
            </button>
            <button class="action-btn delete-btn" @click="handleDelete(recurring.id)">
              삭제
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <Modal
      :is-open="isModalOpen"
      :title="editingRecurring ? '정기 거래 수정' : '정기 거래 추가'"
      @close="closeModal"
    >
      <RecurringForm
        :accounts="accounts"
        :loading="formLoading"
        :initial-data="editingRecurring"
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
import type { RecurringFormData, RecurringTransaction } from '@/types'
import RecurringForm from '@/components/recurring/RecurringForm.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import Modal from '@/components/ui/BaseModal.vue'
import Button from '@/components/ui/BaseButton.vue'

const accountStore = useAccountStore()
const recurringStore = useRecurringStore()
const { accounts } = storeToRefs(accountStore)
const { recurringTransactions, loading } = storeToRefs(recurringStore)
const { isOpen: isModalOpen, open: openModal, close: closeModal } = useModal()
const { success, error } = useNotification()
const { formatCurrency } = useFormatter()

const formLoading = ref(false)
const editingRecurring = ref<RecurringTransaction | null>(null)

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
  editingRecurring.value = null
  openModal()
}

const openEditModal = (recurring: RecurringTransaction) => {
  editingRecurring.value = recurring
  openModal()
}

const handleSubmit = async (formData: RecurringFormData) => {
  if (editingRecurring.value) {
    await handleUpdate(formData)
  } else {
    await handleCreate(formData)
  }
}

const handleCreate = async (formData: RecurringFormData) => {
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

const handleUpdate = async (formData: RecurringFormData) => {
  if (!editingRecurring.value) return

  formLoading.value = true
  try {
    await recurringStore.updateRecurring(editingRecurring.value.id, formData)
    success('정기 거래가 수정되었습니다.')
    closeModal()
  } catch (err) {
    error('정기 거래 수정에 실패했습니다.')
  } finally {
    formLoading.value = false
  }
}

const handleDelete = async (id: number) => {
  if (!confirm('정말 이 정기 거래를 삭제하시겠습니까?')) return

  try {
    await recurringStore.deleteRecurring(id)
    success('정기 거래가 삭제되었습니다.')
  } catch (err) {
    error('정기 거래 삭제에 실패했습니다.')
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
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.recurring-item::before {
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

.recurring-item:hover {
  background: var(--background);
  transform: translateX(4px);
}

.recurring-item:hover::before {
  transform: scaleY(1);
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
  align-items: center;
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

.action-buttons {
  display: flex;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.recurring-item:hover .action-buttons {
  opacity: 1;
}

.action-btn {
  padding: 0.4rem 0.8rem;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--border);
  transition: all 0.2s ease;
  background: var(--surface);
  color: var(--text-main);
}

.edit-btn:hover {
  background: var(--primary-light);
  border-color: var(--primary);
  color: var(--primary);
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.delete-btn {
  background: transparent;
  border-color: var(--danger);
  color: var(--danger);
}

.delete-btn:hover {
  background: var(--danger);
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
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

.recurring-item-animate {
  animation: listItemSlide 0.4s ease-out both;
}

@keyframes listItemSlide {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
