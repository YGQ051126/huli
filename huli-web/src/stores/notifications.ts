import { defineStore } from 'pinia'
import { ref, readonly, computed } from 'vue'
import type { Notification } from '@/types/message'
import { getNotifications, markNotificationRead, clearNotifications } from '@/services/notifications'
import { useUserStore } from './user'

export const useNotificationsStore = defineStore('notifications', () => {
  const items = ref<Notification[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const unreadCount = computed(
    () => items.value.filter(n => n.status === 'unread').length
  )

  const fetchNotifications = async () => {
    loading.value = true
    error.value = null
    try {
      const userStore = useUserStore()
      const userId = String(userStore.user?.id || '')
      items.value = await getNotifications(userId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取通知失败'
    } finally {
      loading.value = false
    }
  }

  const markRead = async (id: string) => {
    try {
      await markNotificationRead(id)
      const item = items.value.find(n => n.id === id)
      if (item) {
        item.status = 'read'
      }
    } catch {
      // ignore
    }
  }

  const clearAll = async () => {
    try {
      await clearNotifications()
      items.value = []
    } catch {
      // ignore
    }
  }

  return {
    items: readonly(items),
    loading: readonly(loading),
    error: readonly(error),
    unreadCount,
    fetchNotifications,
    markRead,
    clearAll
  }
})
