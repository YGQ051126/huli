import api from './api'
import type { Notification } from '@/types/message'

export async function getNotifications(userId?: string): Promise<Notification[]> {
  const res = await api.get('/notifications/', { params: { user_id: userId } })
  return res.data.results || res.data
}

export async function markNotificationRead(id: string | number): Promise<void> {
  await api.post(`/notifications/${id}/read/`)
}

export async function clearNotifications(): Promise<void> {
  await api.post('/notifications/clear/')
}
