import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { accountsAPI, summaryAPI } from '../services/api'
import type { Account, Summary, AccountFormData } from '../types'

export const useAccountStore = defineStore('account', () => {
  // State
  const accounts = ref<Account[]>([])
  const summary = ref<Summary | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const totalAssets = computed(() => summary.value?.total_assets || 0)
  const monthlyIncome = computed(() => summary.value?.monthly_fixed_income || 0)
  const monthlyExpenses = computed(() => summary.value?.monthly_fixed_expenses || 0)
  const netCashflow = computed(() => summary.value?.net_monthly_cashflow || 0)

  const getAccountById = computed(() => {
    return (id: number) => accounts.value.find(acc => acc.id === id)
  })

  // Actions
  const fetchAccounts = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await accountsAPI.getAll()
      accounts.value = response.data
    } catch (err: any) {
      error.value = err.message || '계좌 목록을 불러오는데 실패했습니다'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchSummary = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await summaryAPI.getFullSummary()
      summary.value = response.data
      accounts.value = response.data.accounts
    } catch (err: any) {
      error.value = err.message || '요약 정보를 불러오는데 실패했습니다'
      throw err
    } finally {
      loading.value = false
    }
  }

  const createAccount = async (accountData: AccountFormData) => {
    try {
      const response = await accountsAPI.create(accountData)
      accounts.value.push(response.data)
      await fetchSummary()
      return response.data
    } catch (err: any) {
      error.value = err.message || '계좌 생성에 실패했습니다'
      throw err
    }
  }

  const updateAccount = async (id: number, accountData: Partial<AccountFormData>) => {
    try {
      const response = await accountsAPI.update(id, accountData)
      const index = accounts.value.findIndex(acc => acc.id === id)
      if (index !== -1) {
        accounts.value[index] = response.data
      }
      await fetchSummary()
      return response.data
    } catch (err: any) {
      error.value = err.message || '계좌 수정에 실패했습니다'
      throw err
    }
  }

  const deleteAccount = async (id: number) => {
    try {
      await accountsAPI.delete(id)
      accounts.value = accounts.value.filter(acc => acc.id !== id)
      await fetchSummary()
    } catch (err: any) {
      error.value = err.message || '계좌 삭제에 실패했습니다'
      throw err
    }
  }

  return {
    // State
    accounts,
    summary,
    loading,
    error,
    // Getters
    totalAssets,
    monthlyIncome,
    monthlyExpenses,
    netCashflow,
    getAccountById,
    // Actions
    fetchAccounts,
    fetchSummary,
    createAccount,
    updateAccount,
    deleteAccount
  }
})
