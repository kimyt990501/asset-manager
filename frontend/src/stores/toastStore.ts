import { defineStore } from 'pinia'
import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface Toast {
  id: number
  type: ToastType
  message: string
  duration?: number
}

export const useToastStore = defineStore('toast', () => {
  const toasts = ref<Toast[]>([])
  let nextId = 0

  const addToast = (toast: Omit<Toast, 'id'>) => {
    const id = nextId++
    const newToast: Toast = {
      id,
      ...toast,
      duration: toast.duration || 3000
    }

    toasts.value.push(newToast)

    // 자동으로 토스트 제거
    setTimeout(() => {
      removeToast(id)
    }, newToast.duration)

    return id
  }

  const removeToast = (id: number) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  const success = (message: string, duration?: number) => {
    return addToast({ type: 'success', message, duration })
  }

  const error = (message: string, duration?: number) => {
    return addToast({ type: 'error', message, duration })
  }

  const warning = (message: string, duration?: number) => {
    return addToast({ type: 'warning', message, duration })
  }

  const info = (message: string, duration?: number) => {
    return addToast({ type: 'info', message, duration })
  }

  const clear = () => {
    toasts.value = []
  }

  return {
    toasts,
    addToast,
    removeToast,
    success,
    error,
    warning,
    info,
    clear
  }
})
