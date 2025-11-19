import axios, { AxiosInstance } from 'axios'
import type {
  Account,
  AccountFormData,
  Transaction,
  TransactionFormData,
  RecurringTransaction,
  RecurringFormData,
  Summary
} from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8500/api/v1'

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Accounts API
export const accountsAPI = {
  getAll: () => api.get<Account[]>('/accounts/'),
  getById: (id: number) => api.get<Account>(`/accounts/${id}`),
  create: (data: AccountFormData) => api.post<Account>('/accounts/', data),
  update: (id: number, data: Partial<AccountFormData>) => 
    api.patch<Account>(`/accounts/${id}`, data),
  delete: (id: number) => api.delete(`/accounts/${id}`)
}

// Transactions API
export const transactionsAPI = {
  getAll: (accountId?: number, limit = 100) => {
    const params: Record<string, any> = { limit }
    if (accountId) params.account_id = accountId
    return api.get<Transaction[]>('/transactions/', { params })
  },
  create: (data: TransactionFormData) => api.post<Transaction>('/transactions/', data),
  delete: (id: number) => api.delete(`/transactions/${id}`)
}

// Recurring Transactions API
export const recurringAPI = {
  getAll: (accountId?: number) => {
    const params = accountId ? { account_id: accountId } : {}
    return api.get<RecurringTransaction[]>('/recurring/', { params })
  },
  create: (data: RecurringFormData) => 
    api.post<RecurringTransaction>('/recurring/', data),
  update: (id: number, data: Partial<RecurringFormData>) => 
    api.patch<RecurringTransaction>(`/recurring/${id}`, data),
  deactivate: (id: number) => api.post(`/recurring/${id}/deactivate`)
}

// Summary API
export const summaryAPI = {
  getFullSummary: () => api.get<Summary>('/summary/'),
  getTotalAssets: () => api.get<{ total_assets: number }>('/summary/total-assets'),
  getMonthlyExpenses: () =>
    api.get<{ monthly_fixed_expenses: number }>('/summary/monthly-expenses'),
  getMonthlyIncome: () =>
    api.get<{ monthly_fixed_income: number }>('/summary/monthly-income'),
  getNetWorthTrend: (months: number = 6) =>
    api.get<{ labels: string[], data: number[] }>('/summary/net-worth-trend', { params: { months } })
}

export default api
