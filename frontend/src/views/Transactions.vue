<template>
  <div class="transactions-page">
    <div class="page-header">
      <h1>거래 내역</h1>
      <Button variant="primary" @click="openCreateModal">
        + 거래 추가
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
      <p>등록된 거래 내역이 없습니다.</p>
      <Button variant="primary" @click="openCreateModal">
        첫 거래 추가하기
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
  margin-bottom: 2rem;
}

.page-header h1 {
  color: #2c3e50;
  font-size: 2rem;
}

.filters {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
}

.filter-group select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  max-width: 300px;
}

.filter-group select:focus {
  outline: none;
  border-color: #3498db;
}

.transactions-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.transactions-list {
  overflow: hidden;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.empty-state p {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .filter-group select {
    max-width: 100%;
  }
}
</style>
