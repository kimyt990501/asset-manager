// API 응답 타입
export type AccountType = 'checking' | 'savings' | 'investment' | 'cma'
export type TransactionType = 'income' | 'expense' | 'transfer'
export type FrequencyType = 'daily' | 'weekly' | 'monthly' | 'yearly'

export interface Account {
  id: number
  user_id: number
  name: string
  type: AccountType
  balance: number
  institution?: string
  account_number?: string
  created_at: string
  updated_at: string
}

export interface Transaction {
  id: number
  account_id: number
  type: TransactionType
  category: string
  amount: number
  description?: string
  transaction_date: string
  is_recurring: boolean
  created_at: string
}

export interface RecurringTransaction {
  id: number
  account_id: number
  type: TransactionType
  category: string
  amount: number
  description?: string
  frequency: FrequencyType
  day_of_month?: number
  is_active: boolean
  start_date: string
  end_date?: string
  created_at: string
  updated_at: string
}

export interface Summary {
  total_assets: number
  net_worth: number
  monthly_fixed_expenses: number
  monthly_variable_expenses: number
  monthly_income: number
  net_monthly_cashflow: number
  accounts: Account[]
}

// Form 타입
export interface AccountFormData {
  name: string
  type: AccountType
  balance: number
  institution?: string
  account_number?: string
}

export interface TransactionFormData {
  account_id: number
  type: TransactionType
  category: string
  amount: number
  description?: string
  transaction_date: string
  is_recurring?: boolean
}

export interface RecurringFormData {
  account_id: number
  type: TransactionType
  category: string
  amount: number
  description?: string
  frequency: FrequencyType
  day_of_month?: number
  start_date: string
  end_date?: string
  is_active?: boolean
}

// UI 상태 타입
export interface NotificationOptions {
  type: 'success' | 'error' | 'info' | 'warning'
  message: string
  duration?: number
}
