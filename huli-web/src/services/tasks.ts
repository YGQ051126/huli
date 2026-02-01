import api from './api'
import type { CareTask } from '@/types/task'

export async function getTasks(staffId?: string): Promise<CareTask[]> {
  const res = await api.get('/tasks', { params: { staffId } })
  return res.data
}

export async function completeTask(id: string): Promise<void> {
  await api.post(`/tasks/${id}/complete`)
}

export async function delayTask(id: string, reason: string): Promise<void> {
  await api.post(`/tasks/${id}/delay`, { reason })
}

export async function getDashboardData(): Promise<any> {
  const res = await api.get('/staff/dashboard/')
  return res.data || res
}
