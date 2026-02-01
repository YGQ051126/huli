import { defineStore } from 'pinia'
import { ref, readonly } from 'vue'
import type { Announcement } from '@/types/announcement'
import { getAnnouncements } from '@/services/announcements'

export const useAnnouncementsStore = defineStore('announcements', () => {
  const items = ref<Announcement[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 获取公告列表
  const fetchAnnouncements = async () => {
    loading.value = true
    error.value = null
    try {
      console.log('开始获取公告列表...')
      const data = await getAnnouncements()
      console.log('获取到公告数据:', data)
      items.value = data
      console.log('公告获取完成，数量:', items.value.length)
    } catch (err) {
      console.error('获取公告失败:', err)
      error.value = err instanceof Error ? err.message : '获取公告失败'
    } finally {
      loading.value = false
    }
  }

  return {
    items: readonly(items),
    loading: readonly(loading),
    error: readonly(error),
    fetchAnnouncements
  }
})