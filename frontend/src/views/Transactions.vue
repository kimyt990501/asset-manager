<template>
  <div class="transactions-page">
    <div class="page-header">
      <h1>출입금내역</h1>
      <Button variant="primary" @click="openCreateModal">
        + 내역 추가
      </Button>
    </div>

    <!-- Filters -->
    <div class="filters">
      <div class="filter-group">
        <label for="account-filter">계좌 필터</label>
        <select id="account-filter" v-model="selectedAccountId" @change="handleFilterChange">
          <option :value="undefined">전체 계좌</option>
          <option v-for="account in accounts" :key="account.id" :value="account.id">
            {{ account.name }}
          </option>
        </select>
      </div>

      <div class="filter-group">
        <label for="start-date">시작 날짜</label>
        <input
          id="start-date"
          type="date"
          v-model="startDate"
          @change="handleFilterChange"
        />
      </div>

      <div class="filter-group">
        <label for="end-date">종료 날짜</label>
        <input
          id="end-date"
          type="date"
          v-model="endDate"
          @change="handleFilterChange"
        />
      </div>

      <Button
        v-if="startDate || endDate"
        variant="ghost"
        size="sm"
        @click="clearDateFilters"
        class="clear-filter-btn"
      >
        날짜 필터 초기화
      </Button>
    </div>

    <div v-if="loading && transactions.length === 0" class="transactions-skeleton">
      <TransactionItemSkeleton v-for="i in 5" :key="i" />
    </div>

    <BaseEmptyState
      v-else-if="transactions.length === 0"
      title="출입금 내역이 없습니다"
      description="첫 번째 거래를 기록하여 자산 흐름을 추적하세요."
      action="거래 추가하기"
      @action="openCreateModal"
    >
      <template #icon>
        <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="1" x2="12" y2="23"></line>
          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
        </svg>
      </template>
    </BaseEmptyState>

    <div v-else class="transactions-container">
      <div class="transactions-list">
        <TransactionItem
          v-for="(transaction, index) in transactions"
          :key="transaction.id"
          :transaction="transaction"
          :account-name="getAccountById(transaction.account_id)?.name || '알 수 없음'"
          :style="{ animationDelay: `${index * 0.03}s` }"
          class="transaction-item-animate"
          @click="handleTransactionClick(transaction)"
          @edit="openEditModal(transaction)"
          @delete="handleDelete(transaction)"
        />
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <Modal
      :is-open="isModalOpen"
      :title="editingTransaction ? '거래 수정' : '거래 추가'"
      @close="closeModal"
    >
      <TransactionForm
        :accounts="accounts"
        :loading="formLoading"
        :initial-data="editingTransaction"
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
import { useTransactionStore } from '@/stores/transactionStore'
import { useModal } from '@/composables/useModal'
import { useNotification } from '@/composables/useNotification'
import type { Transaction, TransactionFormData } from '@/types'
import TransactionItem from '@/components/transaction/TransactionItem.vue'
import TransactionForm from '@/components/transaction/TransactionForm.vue'
import TransactionItemSkeleton from '@/components/transaction/TransactionItemSkeleton.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import Modal from '@/components/ui/BaseModal.vue'
import Button from '@/components/ui/BaseButton.vue'

const accountStore = useAccountStore()
const transactionStore = useTransactionStore()
const { accounts, getAccountById } = storeToRefs(accountStore)
const { transactions, loading } = storeToRefs(transactionStore)
const { isOpen: isModalOpen, open: openModal, close: closeModal } = useModal()
const { success, error } = useNotification()

const formLoading = ref(false)
const selectedAccountId = ref<number | undefined>(undefined)
const startDate = ref<string>('')
const endDate = ref<string>('')
const editingTransaction = ref<Transaction | null>(null)

onMounted(async () => {
  await Promise.all([
    accountStore.fetchAccounts(),
    transactionStore.fetchTransactions()
  ])
})

const handleFilterChange = async () => {
  await transactionStore.fetchTransactions(
    selectedAccountId.value,
    100,
    startDate.value || undefined,
    endDate.value || undefined
  )
}

const clearDateFilters = async () => {
  startDate.value = ''
  endDate.value = ''
  await handleFilterChange()
}

const openCreateModal = () => {
  editingTransaction.value = null
  openModal()
}

const openEditModal = (transaction: Transaction) => {
  editingTransaction.value = transaction
  openModal()
}

const handleSubmit = async (formData: TransactionFormData) => {
  if (editingTransaction.value) {
    await handleUpdate(formData)
  } else {
    await handleCreate(formData)
  }
}

const handleCreate = async (formData: TransactionFormData) => {
  formLoading.value = true
  try {
    await transactionStore.createTransaction(formData)
    success('거래가 추가되었습니다.')
    closeModal()
  } catch (err) {
    error('거래 추가에 실패했습니다.')
  } finally {
    formLoading.value = false
  }
}

const handleUpdate = async (formData: TransactionFormData) => {
  if (!editingTransaction.value) return

  formLoading.value = true
  try {
    await transactionStore.updateTransaction(editingTransaction.value.id, formData)
    success('거래가 수정되었습니다.')
    closeModal()
  } catch (err) {
    error('거래 수정에 실패했습니다.')
  } finally {
    formLoading.value = false
  }
}

const handleDelete = async (transaction: Transaction) => {
  if (!confirm('정말 이 거래를 삭제하시겠습니까?')) return

  try {
    await transactionStore.deleteTransaction(transaction.id)
    success('거래가 삭제되었습니다.')
  } catch (err) {
    error('거래 삭제에 실패했습니다.')
  }
}

const handleTransactionClick = (transaction: Transaction) => {
  // 향후 거래 상세 보기 기능 추가 가능
  console.log('Transaction clicked:', transaction)
}
</script>

<style scoped>
.transactions-page {
  min-height: calc(100vh - 64px - 4rem);
  animation: fadeIn 0.6s ease-out;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.page-header h1 {
  font-size: var(--font-display);
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: var(--tracking-tighter);
  background: linear-gradient(180deg, var(--text-main) 0%, var(--text-muted) 150%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-lg);
  align-items: flex-end;
  background: var(--surface);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--spacing-xl);
  border: 1px solid var(--border);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  flex: 0 1 auto;
}

.filter-group label {
  font-weight: 600;
  color: var(--text-muted);
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.filter-group select,
.filter-group input[type="date"] {
  padding: 0.75rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  min-width: 200px;
  background-color: var(--surface);
  color: var(--text-main);
  transition: var(--transition-base);
  cursor: pointer;
}

.filter-group select:hover,
.filter-group input[type="date"]:hover {
  border-color: var(--primary);
}

.filter-group select:focus,
.filter-group input[type="date"]:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.clear-filter-btn {
  align-self: flex-end;
  white-space: nowrap;
}

.transactions-container {
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  overflow: hidden;
}

.transactions-list {
  overflow: hidden;
}

.empty-state {
  text-align: center;
  padding: var(--spacing-2xl);
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
}

.empty-state p {
  color: var(--text-muted);
  margin-bottom: var(--spacing-lg);
  font-size: 1.1rem;
}

.transaction-item-animate {
  animation: listItemSlide 0.4s ease-out both;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
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

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }
  
  .page-header h1 {
    font-size: 2rem;
  }

  .filter-group select {
    max-width: 100%;
  }
}
</style>

