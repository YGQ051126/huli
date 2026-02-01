import api from '@/services/api'

export type AdminService = {
  id: string
  name: string
  description?: string
  price?: number
  active?: boolean
}

export async function getServices(): Promise<AdminService[]> {
  const res = await api.get('/admin/services/')
  return Array.isArray(res) ? res : []
}

export async function createService(payload: Partial<AdminService>): Promise<AdminService> {
  const res = await api.post('/admin/services/', payload)
  return res as unknown as AdminService
}

export async function updateService(id: string, payload: Partial<AdminService>): Promise<AdminService> {
  const res = await api.put(`/admin/services/${id}/`, payload)
  return res as unknown as AdminService
}

export async function deleteService(id: string): Promise<void> {
  await api.delete(`/admin/services/${id}/`)
}

