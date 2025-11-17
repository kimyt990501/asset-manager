import { defineStore } from 'pinia'
import { ref } from 'vue'
import { recurringAPI } from '../services/api'
import type { RecurringTransaction, RecurringFormData } from '../types'

export const useRecurringStore = defineStore('recurring', () => {
  const recurringTransactions = ref<RecurringTransaction[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchRecurring = async (accountId?: number) => {
    loading.value = true
    error.value = null
    try {
      const response = await recurringAPI.getAll(accountId)
      recurringTransactions.value = response.data
    } catch (err: any) {
      error.value = err.message || '정기 거래를 불러오는데 실패했습니다'
      throw err
    } finally {
      loading.value = false
    }
  }

  const createRecurring = async (recurringData: RecurringFormData) => {
    try {
      const response = await recurringAPI.create(recurringData)
      recurringTransactions.value.push(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.message || '정기 거래 생성에 실패했습니다'
      throw err
    }
  }

  const updateRecurring = async (id: number, recurringData: Partial<RecurringFormData>) => {
    try {
      const response = await recurringAPI.update(id, recurringData)
      const index = recurringTransactions.value.findIndex(r => r.id === id)
      if (index !== -1) {
        recurringTransactions.value[index] = response.data
      }
      return response.data
    } catch (err: any) {
      error.value = err.message || '정기 거래 수정에 실패했습니다'
      throw err
    }
  }

  const deactivateRecurring = async (id: number) => {
    try {
      await recurringAPI.deactivate(id)
      const item = recurringTransactions.value.find(r => r.id === id)
      if (item) {
        item.is_active = false
      }
    } catch (err: any) {
      error.value = err.message || '정기 거래 비활성화에 실패했습니다'
      throw err
    }
  }

  return {
    recurringTransactions,
    loading,
    error,
    fetchRecurring,
    createRecurring,
    updateRecurring,
    deactivateRecurring
  }
})
