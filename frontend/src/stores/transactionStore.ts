import { defineStore } from 'pinia'
import { ref } from 'vue'
import { transactionsAPI } from '@/services/api'
import type { Transaction, TransactionFormData } from '@/types'
import { useAccountStore } from '@/stores/accountStore'


export const useTransactionStore = defineStore('transaction', () => {
  const transactions = ref<Transaction[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const accountStore = useAccountStore()

  const fetchTransactions = async (accountId?: number, limit = 100) => {
    loading.value = true
    error.value = null
    try {
      const response = await transactionsAPI.getAll(accountId, limit)
      transactions.value = response.data
    } catch (err: any) {
      error.value = err.message || '거래 내역을 불러오는데 실패했습니다'
      throw err
    } finally {
      loading.value = false
    }
  }

  const createTransaction = async (transactionData: TransactionFormData) => {
    try {
      console.log('Creating transaction:', transactionData)
      const response = await transactionsAPI.create(transactionData)
      console.log('Create transaction response:', response)
      transactions.value.unshift(response.data)
      // 계좌 잔액 업데이트를 위해 summary 다시 불러오기
      await accountStore.fetchSummary()
      return response.data
    } catch (err: any) {
      console.error('Create transaction error:', err)
      console.error('Error response:', err.response?.data)
      error.value = err.response?.data?.detail || err.message || '거래 생성에 실패했습니다'
      throw err
    }
  }

  const deleteTransaction = async (id: number) => {
    try {
      console.log('Deleting transaction with id:', id)
      await transactionsAPI.delete(id)
      transactions.value = transactions.value.filter(tx => tx.id !== id)
      // 계좌 잔액 업데이트
      await accountStore.fetchSummary()
    } catch (err: any) {
      console.error('Delete transaction error:', err)
      console.error('Error response:', err.response?.data)
      error.value = err.response?.data?.detail || err.message || '거래 삭제에 실패했습니다'
      throw err
    }
  }

  return {
    transactions,
    loading,
    error,
    fetchTransactions,
    createTransaction,
    deleteTransaction
  }
})
