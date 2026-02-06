import api from '@/services/api'
import type { User } from '@/types/user'

export async function getUsers(): Promise<User[]> {
  const res = await api.get('/users/')
  if (Array.isArray(res)) return res
  if (res && typeof res === 'object') {
    if (Array.isArray((res as any).data)) return (res as any).data
    if (Array.isArray((res as any).results)) return (res as any).results
  }
  return []
}

export async function createUser(payload: Partial<User> & { password?: string }): Promise<User> {
  const res = await api.post('/users/', payload)
  return res as unknown as User
}

export async function updateUser(id: string, payload: Partial<User>): Promise<User> {
  const res = await api.patch(`/users/${id}/`, payload)
  return res as unknown as User
}

export async function deleteUser(id: string): Promise<void> {
  await api.delete(`/users/${id}/`)
}

