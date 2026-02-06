import api from './api'
import type { User } from '@/types/user'

export interface StaffUser {
  id: number
  user: User
  position: string
  department: string
  created_at: string
  updated_at: string
}

export interface CreateStaffParams {
  user: {
    username: string
    password?: string
    real_name: string
    phone: string
    email?: string
    role: 'staff'
    gender?: string
  }
  position: string
  department: string
}

export async function getStaffList(): Promise<StaffUser[]> {
  const res = await api.get('/staff-users/')
  if (Array.isArray(res)) {
    return res
  }
  if (res && typeof res === 'object') {
    if (Array.isArray((res as any).data)) return (res as any).data
    if (Array.isArray((res as any).results)) return (res as any).results
  }
  return []
}

export async function createStaff(data: CreateStaffParams): Promise<StaffUser> {
  const res = await api.post('/staff-users/', data)
  return res as unknown as StaffUser
}

export async function updateStaff(id: number, data: Partial<CreateStaffParams>): Promise<StaffUser> {
  const res = await api.put(`/staff-users/${id}/`, data)
  return res as unknown as StaffUser
}

export async function deleteStaff(id: number): Promise<void> {
  await api.delete(`/staff-users/${id}/`)
}
