import { useToastStore } from '@/stores/toastStore'

/**
 * Toast 알림을 사용하기 위한 composable
 * Toast Store를 래핑하여 편리하게 사용할 수 있도록 합니다.
 */
export const useNotification = () => {
  const toastStore = useToastStore()

  const success = (message: string, duration?: number) => {
    return toastStore.success(message, duration)
  }

  const error = (message: string, duration?: number) => {
    return toastStore.error(message, duration)
  }

  const warning = (message: string, duration?: number) => {
    return toastStore.warning(message, duration)
  }

  const info = (message: string, duration?: number) => {
    return toastStore.info(message, duration)
  }

  return {
    success,
    error,
    warning,
    info
  }
}
