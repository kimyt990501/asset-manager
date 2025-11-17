import { ACCOUNT_TYPE_LABELS, TRANSACTION_TYPE_LABELS } from '@/utils/constants'

export const useFormatter = () => {
  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW'
    }).format(amount)
  }

  const formatNumber = (num: number): string => {
    return new Intl.NumberFormat('ko-KR').format(num)
  }

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date)
  }

  const formatShortDate = (dateString: string): string => {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('ko-KR', {
      month: '2-digit',
      day: '2-digit'
    }).format(date)
  }

  const getAccountTypeLabel = (type: string): string => {
    return ACCOUNT_TYPE_LABELS[type] || type
  }

  const getTransactionTypeLabel = (type: string): string => {
    return TRANSACTION_TYPE_LABELS[type] || type
  }

  return {
    formatCurrency,
    formatNumber,
    formatDate,
    formatShortDate,
    getAccountTypeLabel,
    getTransactionTypeLabel
  }
}
