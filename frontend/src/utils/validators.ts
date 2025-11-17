export const validateAmount = (value: number): string | null => {
  if (value <= 0) return '금액은 0보다 커야 합니다'
  if (value > 1000000000) return '금액이 너무 큽니다'
  return null
}

export const validateAccountName = (name: string): string | null => {
  if (!name || name.trim().length === 0) return '계좌명을 입력해주세요'
  if (name.length > 50) return '계좌명은 50자 이내여야 합니다'
  return null
}

export const validateDate = (date: string): string | null => {
  if (!date) return '날짜를 입력해주세요'
  const selectedDate = new Date(date)
  if (isNaN(selectedDate.getTime())) return '올바른 날짜 형식이 아닙니다'
  return null
}
