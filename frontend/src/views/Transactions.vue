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
    </div>

    <Loading v-if="loading && transactions.length === 0" />

    <div v-else-if="transactions.length === 0" class="empty-state">
      <p>등록된 출입금 내역이 없습니다.</p>
      <Button variant="primary" @click="openCreateModal">
        첫 내역 추가하기
      </Button>
    </div>

    <div v-else class="transactions-container">
      <div class="transactions-list">
        <TransactionItem
          v-for="transaction in transactions"
          :key="transaction.id"
          :transaction="transaction"
          :account-name="getAccountById(transaction.account_id)?.name || '알 수 없음'"
          @click="handleTransactionClick(transaction)"
        />
      </div>
    </div>

    <!-- Create Modal -->
    <Modal
      :is-open="isModalOpen"
      title="거래 추가"
      @close="closeModal"
    >
      <TransactionForm
        :accounts="accounts"
        :loading="formLoading"
        @submit="handleCreate"
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
import Modal from '@/components/common/Modal.vue'
import Button from '@/components/common/Button.vue'
import Loading from '@/components/common/Loading.vue'

const accountStore = useAccountStore()
const transactionStore = useTransactionStore()
const { accounts, getAccountById } = storeToRefs(accountStore)
const { transactions, loading } = storeToRefs(transactionStore)
const { isOpen: isModalOpen, open: openModal, close: closeModal } = useModal()
const { success, error } = useNotification()

const formLoading = ref(false)
const selectedAccountId = ref<number | undefined>(undefined)

onMounted(async () => {
  await Promise.all([
    accountStore.fetchAccounts(),
    transactionStore.fetchTransactions()
  ])
})

const handleFilterChange = async () => {
  await transactionStore.fetchTransactions(selectedAccountId.value)
}

const openCreateModal = () => {
  openModal()
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

const handleTransactionClick = (transaction: Transaction) => {
  // 향후 거래 상세 보기나 수정 기능 추가 가능
  console.log('Transaction clicked:', transaction)
}
</script>

<style scoped>
.transactions-page {
  min-height: calc(100vh - 64px - 4rem);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.page-header h1 {
  color: var(--text-main);
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.filters {
  background: var(--surface);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--spacing-lg);
  border: 1px solid var(--border-light);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.filter-group label {
  font-weight: 600;
  color: var(--text-main);
  font-size: 0.9rem;
}

.filter-group select {
  padding: 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 1rem;
  max-width: 300px;
  background-color: var(--surface);
  color: var(--text-main);
  transition: var(--transition-base);
}

.filter-group select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.transactions-container {
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
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
  border: 1px solid var(--border-light);
}

.empty-state p {
  color: var(--text-muted);
  margin-bottom: var(--spacing-lg);
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }

  .filter-group select {
    max-width: 100%;
  }
}
</style>

