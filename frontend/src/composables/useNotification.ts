import { ref } from 'vue'
import type { NotificationOptions } from '../types'

const notifications = ref<Array<NotificationOptions & { id: number }>>([])
let notificationId = 0

export const useNotification = () => {
  const show = (options: NotificationOptions) => {
    const id = notificationId++
    const notification = { ...options, id }
    notifications.value.push(notification)

    const duration = options.duration || 3000
    setTimeout(() => {
      remove(id)
    }, duration)
  }

  const remove = (id: number) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const success = (message: string) => {
    show({ type: 'success', message })
  }

  const error = (message: string) => {
    show({ type: 'error', message })
  }

  const info = (message: string) => {
    show({ type: 'info', message })
  }

  return {
    notifications,
    show,
    remove,
    success,
    error,
    info
  }
}
