import api from './api'

export interface BackendTask {
  id: number | string
  type: string
  title: string
  description: string
  patient?: {
    id: number | string
    name: string
  } | null
  due_date: string
  due_time?: string | null
  status: 'pending' | 'in_progress' | 'completed' | 'delayed' | 'cancelled'
  priority: 'low' | 'medium' | 'high'
  completed_at?: string | null
  created_at?: string
  updated_at?: string
}

export async function getTasks(staffId?: string): Promise<BackendTask[]> {
  const res: any = await api.get('/tasks', { params: staffId ? { staffId } : undefined })
  if (Array.isArray(res)) return res as BackendTask[]
  if (res && Array.isArray(res.results)) return res.results as BackendTask[]
  return []
}

export async function completeTask(id: string): Promise<void> {
  await api.post(`/tasks/${id}/complete`)
}

export async function delayTask(id: string, reason: string): Promise<void> {
  await api.post(`/tasks/${id}/delay`, { reason })
}

export async function getDashboardData(): Promise<any> {
  const res = await api.get('/staff/dashboard/')
  return res
}
