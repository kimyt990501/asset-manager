export const ACCOUNT_TYPE_LABELS: Record<string, string> = {
  checking: '입출금',
  savings: '저축',
  investment: '투자',
  cma: 'CMA'
}

export const TRANSACTION_TYPE_LABELS: Record<string, string> = {
  income: '수입',
  expense: '지출',
  transfer: '이체'
}

export const FREQUENCY_LABELS: Record<string, string> = {
  daily: '매일',
  weekly: '매주',
  monthly: '매월',
  yearly: '매년'
}

export const CATEGORIES = {
  income: ['급여', '부수입', '이자', '배당', '기타수입'],
  expense: ['식비', '교통비', '문화생활', '쇼핑', '통신비', '청년도약', 'ETF', 'CMA', '기타지출']
}

export const ACCOUNT_TYPE_COLORS: Record<string, string> = {
  checking: '#3498db',
  savings: '#2ecc71',
  investment: '#9b59b6',
  cma: '#f39c12'
}
